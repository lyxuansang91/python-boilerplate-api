import boto3 
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional
import logging
from pydantic import EmailStr

from core.config import settings

logger = logging.getLogger(__name__)

def send_email(
    to: str | List[str],
    subject: str,
    body: str,
    html_content: Optional[str] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
) -> bool:
    """
    Send an email using configured SMTP server.
    
    Args:
        to: Recipient email address or list of addresses
        subject: Email subject
        body: Plain text email body
        html_content: Optional HTML content
        cc: Optional list of CC recipients
        bcc: Optional list of BCC recipients
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Create message container
        client = boto3.client('ses',
            region_name=settings.SMTP_SERVER,
            aws_access_key_id=settings.SMTP_ACCESS_KEY,
            aws_secret_access_key=settings.SMTP_SECRET_KEY
        )
        message = {}
        message['Subject'] = {'Data': subject}
        body_parts = {
            'Text': {'Data': body},
        }

        if html_content:
            body_parts['Html'] = {'Data': html_content}
        message['Body'] = body_parts

         # Convert single recipient to list
        recipients = [to] if isinstance(to, str) else to
        
        # Prepare the destination configuration
        destination = {
            'ToAddresses': recipients,
        }
        
        if cc:
            destination['CcAddresses'] = cc
        
        if bcc:
            destination['BccAddresses'] = bcc
        
        response = client.send_email(
            Source=settings.SMTP_SENDER,
            Destination=destination,
            Message=message
        )

        message_id = response['MessageId']
        logger.info(f"Email sent successfully to {recipients}. Message ID: {message_id}")
        return True
        
    except ClientError as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False
    except Exception as e:
        logger.error(f'failed to send email: {str(e)}')
        return False