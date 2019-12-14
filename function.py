import json
import base64
import os
from requests_toolbelt.multipart import decoder
from mailchimp3 import MailChimp
from mailchimp3.mailchimpclient import MailChimpError

username = os.environ['USERNAME']
list_id = os.environ['LIST_ID']
api_key = os.environ['API_KEY']

def parse_email(content_type, body):
    multipart_string = base64.b64decode(body)
    parts = decoder.MultipartDecoder(multipart_string, content_type).parts
    for part in parts:
        if 'name="email"' in str(part.headers[b'Content-Disposition']):
            return part.text
    return None

def my_handler(event, context):
    client = MailChimp(mc_api=api_key, mc_user=username)
    content_type = event['headers']['Content-Type']
    email = parse_email(content_type, event['body'])
    try:
        members = client.lists.members.create(list_id, {
            'email_address': email,
            'status': 'subscribed'
        })
    except MailChimpError as e:
        return {
            'status': 400
        }
    return {
        'status': 200
    }
