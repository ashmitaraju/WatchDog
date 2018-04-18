import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread

sender = "straightouttakengeri@gmail.com"


def send(reciever, img_link):
    t = Thread(target=sendemail, args=(reciever, img_link))
    t.start()


def sendemail(reciever, img_link):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "wthiskengeri")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "ALERT: Unauthorized Person Detected"
    msg['From'] = sender
    msg['To'] = reciever

    text = "Do you recognize this person?"
    html = """\
    <html>
      <head></head>
      <body>
        <p>WatchDog Alert!<br>
           <img src=\"""" +img_link+ """\">link</img>
           <h5> Deteced Object </h5>
           StraightOuttaKengeri<sup>TM</sup> <br>
        </p>
      </body>
    </html>
    """
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    t = server.sendmail(sender, reciever, msg.as_string())
    print "sent"

    server.quit()


# Create the body of the message (a plain-text and an HTML version).

# Record the MIME types of both parts - text/plain and text/html.

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.

# Send the message via local SMTP server.
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
