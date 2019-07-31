import ijson
import datetime
from models import ChatHistory, Person, ChatReciept

aliases = {
    "Tee M"     : "Nathan",
    "Nathan M"  : "Nathan",
    "8019013723": "Nathan",
    "4352323482": "Allie",
    "8018360667": "Tonya",
    "Dallin Merrill": "Nikki",
    "8018152744": "Dallin",
    "8016696360": "Nikki",
    "9073439586": "Erik Suckow",
    "9709888855": "Andy Merrill",
    "8016021897": "Jessie Gwilliam",
}

def formatNumber(number):
    formatted = "".join(a for a in number if a.isdigit()) or number.strip()
    if len(formatted) == 11 and formatted[0] == '1':
        formatted = formatted[1:]
    return aliases.get(formatted) or formatted

def call(filename, start, end):
    with open(filename, 'r', encoding='utf8') as json:
        conversations = ijson.items(json, 'conversations.item')
        for conversation in conversations:
            participants = dict()
            for participant in conversation['conversation']['conversation']['participant_data']:
                participant_id = participant['id']['gaia_id']
                participants[participant_id] = formatNumber(participant.get('fallback_name') or participant_id)
            
            for chat in conversation['events']:
                if 'chat_message' not in chat:
                    continue
                timestamp = datetime.datetime.fromtimestamp(int(chat['timestamp'])//1000000)
                if not start < timestamp < end: 
                    continue
                message_content = chat['chat_message']['message_content']
                if 'segment' not in message_content:
                    continue
                full_message = ''
                for message in message_content['segment']:
                    if 'text' not in message:
                        continue
                    full_message += message['text']
                if full_message == '':
                    continue
                sender = chat['sender_id']['gaia_id']
                chat_model = ChatHistory(
                    event_id=chat['event_id'],
                    sender=Person(
                        name=participants[sender]
                    ),
                    message=full_message,
                    timestamp=timestamp,
                )
                
                for reciever, reciever_name in participants.items():
                    if reciever == sender:
                        continue
                    yield ChatReciept(
                        chat=chat_model,
                        reciever=Person(
                            name=reciever_name
                        ),
                    )