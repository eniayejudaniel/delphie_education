import sendgrid
import os, time, traceback
from dotenv import load_dotenv
from sendgrid.helpers.mail import Mail, Email, To, Content


load_dotenv()
api_key = os.getenv("sendgrid_api_key")

message = '''Hi 👋 and welcome to Delphi Education!
Thank you for your interest in studying abroad with us. 🌍

To get started and help us understand your goals, please fill out this quick form so we can check your eligibility and schedule a call with one of our advisors:

Please reply with the following details:
1️⃣ Full Name
2️⃣ Age
3️⃣ Current Job Title
4️⃣ Highest Degree Completed
5️⃣ Destination Country
6️⃣ Estimated Education Budget (£ / $ / €)
7️⃣ Sponsor (Self / Family / Other)
8️⃣ Marital Status
9️⃣ Traveling Alone or With Dependents
🔟 Will you be able to pay an initial deposit? (Yes / No / Not Sure Yet)

Once we receive your details, we’ll review your profile and get in touch.
Please also let us know a good time for us to call you 📞

We’re here to guide you every step of the way!
– The Delphi Education Team'''

email_addresses = [
    "gunwexy@gmail.com", "oyeneyetonia@gmail.com", "fadereraadebusuyi@gmail.com", 
    "seyifapohunda@yahoo.com", "cleversam2sharp@gmail.com", "zinitbiz2007@yahoo.com", 
    "jemsam7@gmail.com", "eniayejudaniel@yahoo.com", "delphieducationuk@gmail.com"

]

def send_email_message(email):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        from_email = Email("info@delphieducation.co.uk")
        to_email = To(email) 
        subject = "Welcome to Delphi Education! Let’s Start Your Study Abroad Journey 🌍"
        content = Content("text/plain", message)
        mail = Mail(from_email, to_email, subject, content)

        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)
        if response.status_code == 202:
            print(f"Successfully sent Automated Message to {email}")
    except Exception:
        print(traceback.format_exc())
