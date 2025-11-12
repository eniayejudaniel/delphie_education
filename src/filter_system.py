import requests, os, json, traceback, time
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

service_account_info = 'src\service_account.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
QUALIFIED_SHEET_ID = '1cBvieZ8oUQMR8puqgAAMriCGxhSsCPOVofawHpZR4Qc'
UNQUALIFIED_SHEET_ID = '1cBvieZ8oUQMR8puqgAAMriCGxhSsCPOVofawHpZR4Qc'

try:
    creds = Credentials.from_service_account_file(service_account_info, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
except Exception:
    print(traceback.format_exc())

def append_to_sheet(sheet_id, sheet_name, data_dict):
    values = [list(data_dict.values())]
    body = {'values': values}
    
    for attempt in range(3):
        try:
            service.spreadsheets().values().append(
                spreadsheetId=sheet_id,
                range=f'{sheet_name}!A:A',
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            print(f"Successfully appended leads to {sheet_name}")
            break
        except HttpError as e:
            print(f"Google Sheets API Error... Retry{attempt + 1}/3: {e}")
        except Exception:
            print(traceback.format_exc())
            if attempt == 2:
                print("All Retries Failed for Google Sheets API")
            else:
                time.sleep(2)

def clean_phone_number(phone):
    phone = phone.strip()
    if phone.startswith("p:"):
        phone = phone.replace("p:", "")
    phone = phone.strip()

    if not phone.startswith("+234"):
        phone = "+234" + phone[1:]
    return phone


def filter_system(lead_fields):

    funding_type = lead_fields.get("how_are_you_looking_to_fund_your_studies_abroad?", "").strip().lower()

    email = lead_fields.get("email")
    phone = lead_fields.get("phone_number")
    clean_phone = clean_phone_number(phone)

    if funding_type == "full_scholarship":
        append_to_sheet(UNQUALIFIED_SHEET_ID, "Unqualify Leads", lead_fields)
    else:
        append_to_sheet(QUALIFIED_SHEET_ID, "Qualify Leads", lead_fields)
        return {"email": email, "phone": clean_phone}