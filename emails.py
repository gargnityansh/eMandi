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
	sub = "eMandi Registration"
	body = """<p>Thank you for registering with eMandi! We are glad to have you.</p><p>Visit our website for more details.</p>"""		   
	if mailSend(fromaddr,toaddr,sub,body) == 200:
		return 200, "OK"
	else:
		print("mail error")
		return 400 ,"error"

def gradeCropFarmerMail(reciever_address, details):
	fromaddr = "emandi0786@gmail.com"
	toaddr = reciever_address 
	sub = "Crop has been graded"
	body = """<p>Your crop [name, type] has been graded. If you are not satisfied with the grade, please feel free to raise a complaint.</p>"""		   
	if mailSend(fromaddr,toaddr,sub,body) == 200:
		return 200, "OK"
	else:
		print("mail error")
		return 400 ,"error"

def farmerCropRegister(reciever_address,details):
	fromaddr = "emandi0786@gmail.com"
	toaddr = reciever_address 
	sub = "Crop Registration"
	body = """<p>Thank you for choosing us.</p> 
	<p>As a part of the next step please send a 200-500gm sample of crop to grading center. 
	Address of center is []. Please label the sample with the following [cropId]</p>"""
	if mailSend(fromaddr,toaddr,sub,body) == 200:
		return 200, "OK"
	else:
		print("mail error")
		return 400 ,"error"

def auditorCropGrade(reciever_address,details):
	fromaddr = "emandi0786@gmail.com"
	toaddr = reciever_address 
	sub = "New Crop Added"
	body = """<p>A new crop has been added for grading.</p>
	<p>Please grade the crop and attach a grading report and set the minimum bidding price as early as possible.</p>"""
	if mailSend(fromaddr,toaddr,sub,body) == 200:
		return 200, "OK"
	else:
		print("mail error")
		return 400 ,"error"
	
if __name__ == "__main__":
	complaintMail('emandi@gmail.com',{})