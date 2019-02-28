import mintapi
import json
import datetime

def call(request, start, end):
	mint = mintapi.Mint(
		request['username'], 
		request['password'],
		mfa_method='sms',  # Can be 'sms' (default) or 'email'
		headless=False,
		mfa_input_callback=None,
		session_path='./session',
	)
	items = mint.get_transactions_json(include_investment=False, skip_duplicates=True, start_date=start.strftime('%m/%d/%y'))
	for item in items:
		try:
			date = datetime.datetime.strptime(item['date'], '%b %d')
		except ValueError:
			date = datetime.datetime.strptime(item['date'], '%m/%d/%y')
		if date > end and not item['isEdited']:
			continue
		if item['isPending']:
			continue
		type = ''
		if item['isTransfer']:
			type = 'transfer'
		elif item['isCheck']:
			if type is not '':
				raise Exception(str(item))
			type = 'check'
		elif item['isDebit']:
			if type is not '':
				raise Exception(str(item))
			type = 'debit'
		yield {
			'id': item['id'],
			'date': date,
			'amount': float(item['amount'][1:]),
			'merchant': item['merchant'],
			'category': item['mcategory'],
			'note': item['note'],
			'bank': item['fi'],
			'account': item['account'],
			'type': type
		}