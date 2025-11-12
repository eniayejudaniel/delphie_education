import requests
import json


ACCESS_TOKEN = "EAATLhUJ8CFABP3t5ZAuedPe70ro2EphgmokLzi1Qz18ScsGWEUM4MjOSadVDVhHPuGCYwVSh4fOf6ZCKO1NaBzaQvjdDOAsRIjnKxhBZBamsp13Fat9HbT1VanLNnBCYraji2AbIDC2zpoTH1mpepTIZAoWdJieVk3kzL2QZAYZBJoZAPORGf5XSjsAwDCNq2vyZAQZDZD"
PAGE_ID = "113413837915309" 
GRAPH_URL = "https://graph.facebook.com/v24.0"

def get_lead_forms():
    url = f"{GRAPH_URL}/{PAGE_ID}/leadgen_forms"
    params = {"access_token": ACCESS_TOKEN}
    
    response = requests.get(url, params=params)
    print(response.text)


    response.raise_for_status()

    
    data = response.json()
    forms = data.get("data", [])
    
    print(f"Found {len(forms)} form(s):")
    for form in forms:
        print(f"- Name: {form.get('name')} | ID: {form.get('id')}")
    
    # Optionally save to file for reference
    with open("lead_forms.json", "w", encoding="utf-8") as f:
        json.dump(forms, f, indent=2)
    print("Saved lead form details to 'lead_forms.json'")

if __name__ == "__main__":
    get_lead_forms()
