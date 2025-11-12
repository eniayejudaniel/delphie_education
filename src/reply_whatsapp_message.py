from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Set Up AI-Agent Assistants

message = '''I hope you are well.
Thanks for registering to attend our webinar!
🎯 Book a free 1-on-1 consultation and explore your study abroad loan options today.

Please fill out this form so we can check your eligibility and schedule a call:
1. Name
2. Age
3. Job Title
4. Degree
5. Destination Country
6. How much are you budgeting for your education?  
7. Sponsor
8. Civil Status
9. Traveling Solo or with Dependent
10. Will you be able to pay a deposit?
We’re here to guide you every step of the way. Feel free to reach out anytime!

Best,

Delphi Team.'''

@app.route("/reply_whatsapp", methods=['POST'])
def reply_whatsapp():
	# Create a new Twilio MessagingResponse
	resp = MessagingResponse()
	resp.message(message)

	# Return the TwiML (as XML) response
	return Response(str(resp), mimetype='text/xml')

if __name__ == "__main__":
	app.run(port=3000)