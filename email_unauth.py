import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def email_unauth(reciever, img_link, sender="straightouttakengeri@gmail.com"):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "ALERT: Unauthorized Person Detected"
    msg['From'] = sender
    msg['To'] = reciever

    text = "Do you recognize this person?"
    html = """\
    <html>
      <head></head>
      <body>
        <p>Kalla!<br>
           StraightOuttaKengeri<sup>TM</sup> <br>
           Here is the <img src=\"""" +img_link+ """\">link</img> you wanted.
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "wthiskengeri")
    response = server.sendmail(sender, reciever, msg.as_string())
    print response
    server.quit()


# Create the body of the message (a plain-text and an HTML version).

# Record the MIME types of both parts - text/plain and text/html.

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.

# Send the message via local SMTP server.
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
