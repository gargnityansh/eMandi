import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def mailSend(fromEmail, toEmail, subject, body):
	try:
		msg = MIMEMultipart() 
		msg['From'] = fromEmail 
		msg['To'] = toEmail
		msg['Subject'] = subject
		body = body
		msg.attach(MIMEText(body, 'html'))   
		s = smtplib.SMTP('in-v3.mailjet.com', 587) 
		s.starttls()
		s.login("f0fee6a334f2fad14a901429ddfdc1a5", "8f04c0ba92e4d7fbef85897d54306ef0")
		text = msg.as_string()
		s.sendmail(fromEmail, toEmail, text) 
		s.quit()
		return 200
	except:
		return 400

def complaintMail(reciever_address, contactDetails):
	fromaddr = "emandi0786@gmail.com"
	toaddr = reciever_address 
	sub = contactDetails['subject']
	body = "Query from "+contactDetails["name"]+"\n "+contactDetails['email'] +"\n"+contactDetails['message']		   
	if mailSend(fromaddr,toaddr,sub,body) == 200:
		return 200, "OK"
	else:
		print("mail error")
		return 400 ,"error"

def registerMail(reciever_address,details):
	fromaddr = "emandi0786@gmail.com"
	toaddr = reciever_address 
	sub = "Thanks for Registering on eMandi"
	body = """<p>we are glad to have on board on eMandi.</p><p>Visit our website for participating in auctions</p>"""		   
	if mailSend(fromaddr,toaddr,sub,body) == 200:
		return 200, "OK"
	else:
		print("mail error")
		return 400 ,"error"

def gradeCropFarmerMail(reciever_address,details):
	fromaddr = "emandi0786@gmail.com"
	toaddr = reciever_address 
	sub = "Crop with id is graded"
	body = """<p>Your crop with the following cropid has been graded. If you found any mismatch please feel free to raise a complaint.</p>"""		   
	if mailSend(fromaddr,toaddr,sub,body) == 200:
		return 200, "OK"
	else:
		print("mail error")
		return 400 ,"error"

def farmerCropRegister(reciever_address,details):
	fromaddr = "emandi0786@gmail.com"
	toaddr = reciever_address 
	sub = "Thanks for Registering on eMandi"
	body = """<p>Please send a 200-500gm sample of crop to the nearest grading sample. Address of sample is. Please label the samplw with the following cropId</p>"""
	if mailSend(fromaddr,toaddr,sub,body) == 200:
		return 200, "OK"
	else:
		print("mail error")
		return 400 ,"error"

def auditorCropGrade(reciever_address,details):
	fromaddr = "emandi0786@gmail.com"
	toaddr = reciever_address 
	sub = "Thanks for Registering on eMandi"
	body = """<p>following are the details of crop which is recently added to be grade.</p>"""
	if mailSend(fromaddr,toaddr,sub,body) == 200:
		return 200, "OK"
	else:
		print("mail error")
		return 400 ,"error"
	
if __name__ == "__main__":
	complaintMail('emandi@gmail.com',{})