import ijson
import datetime

myAliases = {"+18019013723", "Nathan M"}
aliases = {
	"+14352323482": "Allie Merrill",
	"+18018360667": "Tonya Merrill",
	"+18018152744": "Dallin Merrill",
	"9073439586": "Erik Suckow",
	"(970) 988-8855": "Andy Merrill",
	"+18016021897": "Jessie Gwilliam",
}

unknown = set()

def call(filename, start, end):
	with open(filename, 'r', encoding='utf8') as json:
		conversations = ijson.items(json, 'conversations.item')
		for conversation in conversations:
			participants = dict()
			for participant in conversation['conversation']['conversation']['participant_data']:
				participant_id = participant['id']['gaia_id']
				if 'fallback_name' in participant:
					name = participant['fallback_name']
				else:
					name = participant_id
				participants[participant_id] = name
			other_participants = i for i in participants.values() if i not in myAliases
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
				participant = chat['sender_id']['gaia_id']
				senderParticipant = participants[participant]
				if senderParticipant in myAliases:
					action = 'sent'
				else:
					action = 'received'
				yield {
					'id' : chat['event_id'],
					'message' : full_message,
					'action' : action,
					'participants' : other_participants,
					'timestamp' : timestamp,
				}