import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
   

def sendMail(reciever_address, contactDetails=None):
	fromaddr = "famegamecorp2020@gmail.com"
	toaddr = reciever_address
	try:   
		if contactDetails == None:
			msg = MIMEMultipart() 
			  
			msg['From'] = fromaddr 
			msg['To'] = toaddr 
			msg['Subject'] = "Reset FameGame Password"
			body = "Click on the below link to reset your FameGame account Password"
			   
			msg.attach(MIMEText(body, 'plain')) 
			  
			s = smtplib.SMTP('smtp.gmail.com', 587) 
			s.starttls()
			s.login(fromaddr, "FameGame2020")
			text = msg.as_string() 
			s.sendmail(fromaddr, toaddr, text) 
			s.quit()
		else:
			msg = MIMEMultipart() 
			  
			msg['From'] = fromaddr 
			msg['To'] = toaddr
			msg['Subject'] = contactDetails['subject']
			body = "Query from "+contactDetails["name"]+" "+contactDetails['email'] +"\n"+contactDetails['message']
			   
			msg.attach(MIMEText(body, 'plain')) 
			  
			s = smtplib.SMTP('smtp.gmail.com', 587) 
			s.starttls()
			s.login(fromaddr, "FameGame2020")
			text = msg.as_string() 
			s.sendmail(fromaddr, toaddr, text) 
			s.quit()
		
	except:
		print("mail")
		return 500, "mail not send"

	print("mail sent")		
	return 200, "mail sent"

#sendMail('famegamecorp2020@gmail.com')