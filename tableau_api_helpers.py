import requests
import xml.etree.ElementTree as ET




def auth():
    url = "https://dub01.online.tableau.com/api/3.4/auth/signin"
    payload = {
        "credentials": {
            "personalAccessTokenName": "qa_test",
            "personalAccessTokenSecret": "Q158tjMuSnabQrauZbeH8Q==:b04yNQBpG3crJFkRzyy7XtQ3UnHMAAoE",
            "site": {
                "contentUrl": "consumerphysics"
            }
        }
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code!=200:
        raise Exception(f"Authentication failed: {response.status_code} - {response.text}")

    root = ET.fromstring(response.text)
    namespace = {'t': 'http://tableau.com/api'}

    token = root.find(".//t:credentials", namespace).attrib["token"]
    site_id = root.find(".//t:site", namespace).attrib["id"]

    return token, site_id

def get_workbook_id(token, site_id, workbook_name):
    url = f"https://dub01.online.tableau.com/api/3.4/sites/{site_id}/workbooks"
    headers = {
        "X-Tableau-Auth": token
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get workbooks: {response.status_code} - {response.text}")

    root = ET.fromstring(response.text)
    namespace = {'t': 'http://tableau.com/api'}
    for workbook in root.findall(".//t:workbook", namespace):
        name = workbook.attrib.get("name")
        if name == workbook_name:
            return workbook.attrib["id"]

    raise Exception(f'Workbook "{workbook_name}" not found')

def get_view_id(token, site_id, workbook_id, view_name=None):
    url = f"https://dub01.online.tableau.com/api/3.4/sites/{site_id}/workbooks/{workbook_id}/views"
    headers = { "X-Tableau-Auth": token }

    namespace = {'t': 'http://tableau.com/api'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get views: {response.status_code} - {response.text}")

    root = ET.fromstring(response.text)
    for view in root.findall(".//t:view", namespace):
        if view_name is None or view.attrib.get("name") == view_name:
            return view.attrib["id"]

    raise Exception(f'View "{view_name or "[any]"}" not found')

def get_view_data(token, site_id, view_id, filter_username=None):
    url = f"https://dub01.online.tableau.com/api/3.4/sites/{site_id}/views/{view_id}/data"
    if filter_username:
        url += f"?vf_Username={filter_username}"

    headers = {
        "X-Tableau-Auth": token
    }

    response = requests.get(url, headers=headers)
    return response


