import csv, smtplib, ssl, time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

message = MIMEMultipart("alternative")
message["Subject"] = "MY SUBJECT"

from_address = "MYEMAIL@gmail.com"
password = 'MYPASSWORD'

message["From"] = from_address

# Normal text and HTML versions in case the recepient disabled HTML.
text = """\
Dear {name},

Hi how are you doing?

Thank you!

Regards,
Name
"""

html = """\
<html>
  <body>
    <p style="line-height: 0.5;">Dear {name},</p>
    <p style="line-height: 0.5;">
      <br>
    </p>
    <p style="line-height: 0.5;">Hi how are you doing?</p>
    <p style="line-height: 0.5;">
      <br>
    </p>
    <p style="line-height: 0.5;">Thank you!</p>
    <p style="line-height: 0.5;">
      <br>
    </p>
    <p style="line-height: 0.5;">Regards,</p>
    <p style="line-height: 0.5;">Name</p>
  </body>
</html>
"""

# Change to plain/html MIMEText objects
normalText = MIMEText(text, "plain")
htmlText = MIMEText(html, "html")

# Add to message
message.attach(normalText)
message.attach(htmlText)

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(from_address, password)
    with open("test.csv") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for email, name in reader:
            del message["To"]
            message["To"] = email
            server.sendmail(
                from_address,
                email,
                message.as_string().format(name=name)
            )
            print(email) # Track which email has been sent to
            time.sleep(10) # Add a short delay