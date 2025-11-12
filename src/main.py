import os, traceback, json
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
account_sid = os.getenv("twilio_account_sid")
auth_token = os.getenv("twilio_auth_token")
client = Client(account_sid, auth_token)

def send_whatsapp_message(first_name, phone_number):
    try:
        message = client.messages.create(
            from_='whatsapp:+447448195554',
            content_sid='HX378783ac964b9aa0e0f5de198f18b473',
            content_variables = json.dumps({"1": first_name}),
            to=f'whatsapp:{phone_number}'
        )
        print(f"Successfully sent Automated mesage to {first_name} Whatsapp number: {phone_number} with message sid: {message.sid}")
    
    except TwilioRestException as e:
        if "not a valid WhatsApp user" in str(e):
            print(f"{phone_number} is not registered on WhatsApp.")
    
    except Exception:
        print(traceback.format_exc())


@app.post("/send_whatsapp")
async def send_whatsapp(request: Request):
    try:
        data = await request.json()
        print(data)
        first_name = data.get("first_name")
        phone_number = data.get("phone_number")

        if not phone_number:
            return JSONResponse({"error": "Phone number is required"}, status_code=400)

        result = send_whatsapp_message(first_name, phone_number)
        return JSONResponse(result, status_code=200)

    except Exception:
        print(traceback.format_exc())
        return JSONResponse({"status": "error", "details": "Invalid request payload"}, status_code=400)
    
@app.get("/")
def health_check():
    return {"status": "ok"}
