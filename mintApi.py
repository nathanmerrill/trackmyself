import mintapi
import json
import datetime
from models import TransactionHistory, Merchant, BankAccount, TransactionType

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
        if date.year == '1900':
            date.year = datetime.date.today().year
        if date > end and not item['isEdited']:
            continue
        if item['isPending']:
            continue
        type = None
        if item['isTransfer']:
            type = TransactionType.Transfer
        elif item['isCheck']:
            if type:
                raise Exception(str(item))
            type = TransactionType.Check
        elif item['isDebit']:
            if type:
                raise Exception(str(item))
            type = TransactionType.Debit
        elif not type:
            type = TransactionType.Other
        
        formatted_amount = item['amount'].replace('$','').replace(',','')
        yield TransactionHistory(
            ref_id=item['id'],
            amount=round(float(formatted_amount)*100),
            merchant=Merchant(name=item['merchant']),
            bank_account = BankAccount(
                bank = item['fi'],
                name = item['account'],
            ),
            timestamp=date,
            category=item['mcategory'],
            type=type,
            note=item['note']
        )