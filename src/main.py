import os, traceback, json
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


app = FastAPI()
load_dotenv()
account_sid = os.getenv("twilio_account_sid")
auth_token = os.getenv("twilio_auth_token")
client = Client(account_sid, auth_token)

def send_email(subject, body):
    try:
        sg = SendGridAPIClient(os.getenv("sendgrid_api_key"))
        message = Mail(
            from_email="info@delphieducation.co.uk",
            to_emails="info@delphieducation.co.uk",
            subject=subject,
            plain_text_content=body
        )

        response = sg.send(message)
        print(f"Email sent with status {response.status_code}")

    except Exception:
        print("SendGrid email sending failed:")
        print(traceback.format_exc())


def send_whatsapp_message(first_name, phone_number):
    try:
        message = client.messages.create(
            from_='whatsapp:+447448195554',
            content_sid='HX378783ac964b9aa0e0f5de198f18b473',
            content_variables = json.dumps({"1": first_name}),
            to=f'whatsapp:{phone_number}',
            status_callback="https://delphi-education.onrender.com/whatsapp_status"
        )
        print(f"Successfully sent Automated mesage to {first_name} Whatsapp number: {phone_number} with message sid: {message.sid}")
    
    except TwilioRestException as e:
        if "not a valid WhatsApp user" in str(e):
            print(f"{phone_number} is not registered on WhatsApp.")
    
    except Exception:
        print(traceback.format_exc())


@app.post("/send_whatsapp")
async def send_whatsapp(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        print(data)
        first_name = data.get("first_name")
        phone_number = data.get("phone_number")

        if not phone_number:
            return JSONResponse({"error": "Phone number is required"}, status_code=400)

        background_tasks.add_task(send_whatsapp_message, first_name, phone_number)
        return JSONResponse({"status": "processing"}, status_code=200)

    except Exception:
        print(traceback.format_exc())
        return JSONResponse({"status": "error", "details": "Invalid request payload"}, status_code=400)

@app.post("/whatsapp_status")
async def whatsapp_status(request: Request, background_tasks: BackgroundTasks):
    try:
        form = await request.form()
        message_sid = form.get("MessageSid")
        message_status = form.get("MessageStatus")
        to_number = form.get("To")
        error_code = form.get("ErrorCode")

        log = f"""
        WHATSAPP STATUS UPDATE
        SID: {message_sid}
        Status: {message_status}
        To: {to_number}
        Error: {error_code}
        """

        print(log)

        # Send email notification
        background_tasks.add_task(
            send_email,
            subject=f"WhatsApp Message Status: {message_status}",
            body=log
        )

        return JSONResponse({"received": True})

    except Exception:
        print(traceback.format_exc())
        return JSONResponse({"error": "Status callback error"}, status_code=400)

@app.post("/whatsapp_inbound")
async def inbound_whatsapp(request: Request, background_tasks: BackgroundTasks):
    try:
        form = await request.form()
        from_number = form.get("From")
        body = form.get("Body")

        log = f"""
        NEW INBOUND WHATSAPP MESSAGE
        From: {from_number}
        Message: {body}
        """

        print(log)

        background_tasks.add_task(
            send_email,
            subject="New WhatsApp Message",
            body=log
        )

        return JSONResponse({"status": "received"})

    except Exception:
        print(traceback.format_exc())
        return JSONResponse({"status": "error"}, status_code=400)

    
@app.get("/")
def health_check():
    return {"status": "ok"}
