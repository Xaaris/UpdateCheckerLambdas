import os
import smtplib
import ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "updatecheckermailer@gmail.com"
password = os.environ["MAIL_PASSWORD"]

context = ssl.create_default_context()


def send_update_info_mail(receiver_email: str, product_name: str, old_version: str, new_version: str,
                          release_notes_link: str):
    subject = f"Subject: Update available for {product_name}\n\n"
    body = f"There is an update from {old_version} to {new_version} available! " \
           f"You can find the release notes here: {release_notes_link}"
    message = subject + body
    _send_email(receiver_email, message)


def _send_email(receiver_email: str, message: str):
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
