from tableau_api_helpers import auth, get_workbook_id, get_view_id, get_view_data
import xml.etree.ElementTree as ET
import csv
import io

def test_retrieve_data_from_view():
    token, site_id = auth()
    workbook_id = get_workbook_id(token, site_id, "Tableau Assignment")
    view_id = get_view_id(token, site_id, workbook_id)
    response = get_view_data(token, site_id, view_id)

    assert response.status_code == 200
    assert "Username" in response.text  # column name
    assert "," in response.text         # it's comma-separated
    assert "\n" in response.text        # multiple lines



def test_filter_data_by_user():
    token, site_id = auth()
    workbook_id = get_workbook_id(token, site_id, "Tableau Assignment")
    view_id = get_view_id(token, site_id, workbook_id)
    response = get_view_data(token, site_id, view_id, filter_username="john.corry@demorag.com")

    assert response.status_code == 200

    csv_file = io.StringIO(response.text)
    reader = csv.DictReader(csv_file)

    rows = list(reader)
    assert len(rows) > 0, "No rows found for the user"



def test_invalid_view_id_returns_error():
    token, site_id = auth()
    invalid_view_id = "DanielBaron123"

    response = get_view_data(token, site_id, invalid_view_id)

    # Check it's an error status (not 200)
    assert response.status_code != 200
    assert response.status_code in [400, 404], f"Unexpected status: {response.status_code}"

    # Optionally check XML contains an error tag or message
    assert "error" in response.text.lower() or "tsResponse" in response.text


