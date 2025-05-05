from flask import Flask, request
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAATaVudqKO4BOZCeWwkZBghUhJ6YbOkRXlAJa0GXmDHhx5IEvP1RHI0fIfzDGBxx8hZAqbgwhXvMb1HQu2ZAsEJeGVlkdwZAJ40aNR4Fo9FLZARXdyzn1GFJGy1Q4NZBuzoyBAqfwgqurwZBGJ9eCYQ3fhZATXRGCAtwhzudvhZBk9MxrZB7wXnfCaNfFwPjHomXSqnKAZDZD'
VERIFY_TOKEN = 'idriss123'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification token mismatch"
    
    data = request.get_json()
    for entry in data['entry']:
        for msg_event in entry['messaging']:
            sender = msg_event['sender']['id']
            if 'message' in msg_event:
                message_text = msg_event['message'].get('text')
                handle_message(sender, message_text)
    return "ok"

def handle_message(sender, message):
    if message.lower() == 'naruto':
        send_manga_details(sender)
    else:
        send_text(sender, "أرسل 'Naruto' لعرض معلومات المانجا.")

def send_text(sender, text):
    payload = {
        'recipient': {'id': sender},
        'message': {'text': text}
    }
    requests.post(f'https://graph.facebook.com/v13.0/me/messages?access_token={PAGE_ACCESS_TOKEN}', json=payload)

def send_manga_details(sender):
    payload = {
        'recipient': {'id': sender},
        'message': {
            'attachment': {
                'type': 'image',
                'payload': {
                    'url': 'https://link-to-naruto-cover.jpg',
                    'is_reusable': True
                }
            }
        }
    }
    requests.post(f'https://graph.facebook.com/v13.0/me/messages?access_token={PAGE_ACCESS_TOKEN}', json=payload)
    send_text(sender, "يمكنك قراءة مانجا ناروتو المترجمة من هنا: https://lekmanga.net/manga/naruto/")