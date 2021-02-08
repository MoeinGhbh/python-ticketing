# python -m smtpd -c DebuggingServer -n localhost:1025
import smtplib
import ssl


class SendEmail:

    def __init__(self, receiver_email):
        self.smtp_server = "smtp.office365.com"
        self.port = 587  # For starttls
        self.sender_email = "m.ghobbeh@vriday.net"
        self.receiver_email = receiver_email
        self.password = "Rose.Raeein@83"

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
        message = """\
        Subject: Hi there

        This message is sent from Python."""

        context = ssl.create_default_context()
        # context="STARTTLS"
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, message)
