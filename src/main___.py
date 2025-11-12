import os
import requests
from dotenv import load_dotenv
from filter_system import filter_system
from send_whatsapp_message import send_whatsapp_message
from send_email_message import send_email_message
from delphi_ai_assistant import ask_groq
from twilio.twiml.messaging_response import MessagingResponse
from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse

app = FastAPI()
load_dotenv()

VERIFY_TOKEN = os.getenv("facebook_verify_token")
PAGE_ACCESS_TOKEN = os.getenv("facebook_page_access_token")

@app.get("/webhook")
async def verify_facebook_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge, status_code=200)
    else:
        return PlainTextResponse("Forbidden", status_code=403)
    

@app.post("/webhook")
async def receive_lead_from_facebook(request: Request):
    data = await request.json()
    print("Raw webhook data:", data)

    # Extract Leads
    try:
        leadgen_id = data["entry"][0]["changes"][0]["value"]["leadgen_id"]
        lead_url = f"https://graph.facebook.com/v24.0/{leadgen_id}?access_token={PAGE_ACCESS_TOKEN}"

        response = requests.get(lead_url)
        lead_details = response.json()

    except Exception as e:
        print("Error extracting lead:", e)
        return {"status": "error", "details": str(e)}

    # Filter System
    leads_filter = filter_system(lead_details)

    # Send Automated Whatsapp Message x Email Message
    if leads_filter:
        phone_number = leads_filter.get("phone")
        email_address = leads_filter.get("email")

        if phone_number:
            send_whatsapp_message(phone_number)
        if email_address:
            send_email_message(email_address)

   
@app.post("/reply_whatsapp")
async def reply_whatsapp(request: Request):
    data = await request.form()
    incoming_message = data.get("Body", "").strip()
    #sender = data.get("From", "")

    try:
        ai_reply = ask_groq(incoming_message)
    except Exception as e:
        print("Error calling Groq model:", e)
        ai_reply = "Sorry, I’m having trouble responding right now. Please try again later."

    # Create a new Twilio MessagingResponse
    resp = MessagingResponse()
    resp.message(ai_reply)

    # Return the TwiML (as XML) response
    return Response(str(resp), media_type='text/xml')


@app.post("/status_callback")
async def track_and_follow_up():
    pass

