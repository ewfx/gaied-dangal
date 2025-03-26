import requests

BASE_URL = "http://localhost:3000"

def get_response():
    response = requests.get(f"{BASE_URL}/process-emails")
    assert response.status_code == 200
    return response.json()

def test_emails_processing_results_not_empty():
    response_json = get_response()
    
    assert 'results' in response_json, "The key 'results' is not present in the response"
    assert isinstance(response_json['results'], list), f"Expected 'results' to be a list, but got {type(response_json['results'])}"

    for result in response_json['results']:
        assert isinstance(result, dict), f"Each result should be a dictionary, but got {type(result)}"

def test_emails_processing_result_structure():
    response_json = get_response()

    for result in response_json['results']:
        required_keys = ['Request Type', 'Sub-Request Type', 'Reason', 'Confidence', 'Extracted Fields', 'email', 'duplicate']
        for key in required_keys:
            assert key in result, f"The key '{key}' is not present in the result"

def test_emails_processing_result_values():
    response_json = get_response()

    for result in response_json['results']:
        assert result['Request Type'] == "Adjustment", f"Expected 'Request Type' to be 'Adjustment', but got {result['Request Type']}"
        assert result['Sub-Request Type'] in ["Decrease", "N/A", "Reallocation Fees"], f"Unexpected 'Sub-Request Type': {result['Sub-Request Type']}"
        assert isinstance(result['Confidence'], int), f"Expected 'Confidence' to be an integer, but got {type(result['Confidence'])}"
        assert 0 <= result['Confidence'] <= 100, f"Expected 'Confidence' to be between 0 and 100, but got {result['Confidence']}"
        assert result['email'].endswith(".eml"), f"Expected 'email' to end with '.eml', but got {result['email']}"
        assert isinstance(result['duplicate'], bool), f"Expected 'duplicate' to be a boolean, but got {type(result['duplicate'])}"

def test_emails_processing_extracted_fields():
    response_json = get_response()

    for result in response_json['results']:
        if result['Sub-Request Type'] == "Reallocation Fees":
            extracted_fields = result['Extracted Fields']
            required_keys = ['Deal Name', 'Amount', 'Disputed Charges']
            for key in required_keys:
                assert key in extracted_fields, f"The key '{key}' is not present in 'Extracted Fields'"
            
            assert extracted_fields['Deal Name'] == "Current Loan", f"Expected 'Deal Name' to be 'Current Loan', but got {extracted_fields['Deal Name']}"
            assert extracted_fields['Amount'] == "$3,500,000", f"Expected 'Amount' to be '$3,500,000', but got {extracted_fields['Amount']}"
            assert extracted_fields['Disputed Charges'] == "$15,000", f"Expected 'Disputed Charges' to be '$15,000', but got {extracted_fields['Disputed Charges']}"

def test_emails_processing_reason_field():
    response_json = get_response()

    for result in response_json['results']:
        assert isinstance(result['Reason'], str), f"Expected 'Reason' to be a string, but got {type(result['Reason'])}"