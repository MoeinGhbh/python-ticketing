# python -m smtpd -c DebuggingServer -n localhost:1025
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendEmail:

    def __init__(self, receiver_email, reciver_name, startdate, event_name, unique_id):
        self.smtp_server = "smtp.office365.com"
        self.port = 587  # For starttls
        self.sender_email = "m.ghobbeh@vriday.net"
        self.receiver_email = receiver_email
        self.password = "Rose.Raeein@83"
        self.reciver_name = reciver_name
        self.startdate = startdate
        self.event_name = event_name
        self.unique_id = unique_id

        # # Create a secure SSL context
        # context = ssl.create_default_context()

        # # Try to log in to server and send email
        # try:
        #     server = smtplib.SMTP(smtp_server,port)
        #     server.ehlo() # Can be omitted
        #     server.starttls(context=context) # Secure the connection
        #     server.ehlo() # Can be omitted
        #     server.login(sender_email, password)
        #     # TODO: Send email here
        # except Exception as e:
        #     # Print any error messages to stdout
        #     print(e)
        # finally:
        #     server.quit()

    def send(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Invitation email for NexR seminar"
        message["From"] = self.sender_email
        message["To"] = self.receiver_email

        # Create the plain-text and HTML version of your message
        text = """\
        Hi Dear """+ self.reciver_name +""",
        You invited to join us in NexR Seminar.
        """


        html = """\
        <html>
        <body>
            <h3> THIS EMAIL SEND FROM THE WEBSITE OF NEXR SEMINAR FOR TEST FUNCTIONALITY </h3>
            <p>Hi Dear """+ self.reciver_name +""",<br><br>
            You invited to join us in NexR Seminar call " """+ self.event_name +""" " on """ + self.startdate + """.<br>
            <a href="https://nexr-seminar.com/">Nexr-seminar</a> 
            has many great experince.<br><br>
            this is your ID: """ + str(self.unique_id) + """<br><br>
           
            <br>
            <br>

            Best regards <br>
            NexR Seminar team
            </p>
        </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        # context="STARTTLS"
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email,
                            self.receiver_email, message.as_string())
