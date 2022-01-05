import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
   

def sendMail(reciever_address, contactDetails=None):
	fromaddr = "emandi@gmail.com"
	toaddr = reciever_address
	try:   
		if contactDetails == None:
			msg = MIMEMultipart() 
			  
			msg['From'] = fromaddr 
			msg['To'] = toaddr 
			msg['Subject'] = "Update Game"
			body = "A game that you have purchased is recently being updated. Please download the updated version of the game from the website.\n-Regards\nFameGame"
			msg.attach(MIMEText(body, 'plain')) 
			  
			s = smtplib.SMTP('smtp.gmail.com', 587) 
			s.starttls()
			s.login(fromaddr, "")
			text = msg.as_string() 
			s.sendmail(fromaddr, toaddr, text) 
			s.quit()
		else:
			msg = MIMEMultipart() 
			  
			msg['From'] = fromaddr 
			msg['To'] = fromaddr
			msg['Subject'] = contactDetails['subject']
			body = "Query from "+contactDetails["name"]+"\n "+contactDetails['email'] +"\n"+contactDetails['message']
			   
			msg.attach(MIMEText(body, 'plain')) 
			s = smtplib.SMTP('smtp.gmail.com', 587) 
			s.starttls()
			s.login(fromaddr, "")
			text = msg.as_string() 
			s.sendmail(fromaddr, toaddr, text) 
			s.quit()
			print("mail sent successfully")
	except Exception as e:
		print(e)
		return 500, "mail not send"

	print("mail sent")		
	return 200, "mail sent"

if __name__ == "__main__":
	sendMail('emandi@gmail.com')