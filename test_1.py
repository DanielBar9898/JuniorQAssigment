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



