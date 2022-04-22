"""
Module to send emails from the application.

Classes
-------
    None

Functions
---------
    send_email:
        Tries to send an email with the info provided.

Misc Variables
--------------
    None

"""

import os
import ssl
import smtplib

from email import encoders
from typing import Optional, Union
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(
    subject: str,
    email_body: str,
    sender_email: str,
    sender_server: str,
    receiver_email: str,
    sender_password: str,
    salutation: Optional[str] = "Hello",
    file_path: Optional[Union[None, str]] = None,
) -> bool:
    """
    Tries to send an email with the info provided.

    Parameters
    ----------

        sender_email (str):
            The sender email address.
        sender_password (str):
            The sender email password.
        sender_server:
            The sender email's server address.
        receiver_email (str):
            The reciever's email address.
        subject (str):
            The subject of the email.
        salutation (Optional[str]):
            The email salutation, will default to 'Hello' if absent.
        email_body (str):
            The email text.
        file_path (Optional[str]):
            A file path to an attachment if needed.

    Returns
    -------
        bool:
            True if the email was successfully sent, False if otherwise.

    Raises
    ------
        SMTPAuthenticationError:
            When the authentication details provided are incorrect.
        FileNotFoundError:
            If the file path provided is invalid.
        Exception:
            When there are unexpected errors e.g email server is down.
    """

    try:
        
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Create the plain-text and HTML version of your message
        text = f"""\
            {salutation},
            {email_body}
            This is an automated email, Do not reply to this email.
        """

        html = f"""\
            <html>
            <body>
                <p><strong>{salutation}</strong>, <br>
                {email_body}
                </p>
                <br>

                <p>
                    This is an automated email, Do not reply to this email.
                </p>
            </body>
            </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        if os.getenv("EMAIL_PORT") and \
            int(os.getenv("EMAIL_PORT")) == 587:
            with smtplib.SMTP(sender_server, 587) as server:

                context = ssl.create_default_context()
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                
                server.login(sender_email, sender_password)

                server.sendmail(sender_email, receiver_email, message.as_string())

                return True

        if file_path:
            # Open file in binary mode
            with open(file_path, "rb") as attachment:
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {file_path}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)

        text = message.as_string()
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(sender_server, 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(
                sender_email, receiver_email, text
            )

    except smtplib.SMTPAuthenticationError as error:
        message = "Incorrect authentication details! Please check then retry."
        print(message)
        return False
    except FileNotFoundError as error:
        print(error)
        return False
    except Exception as error:
        print(error)
        return False

    return True
