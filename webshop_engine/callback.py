from twilio.rest import TwilioRestClient

account_sid = 'ACacf849d8ead30ecf404e6282a2842207'
auth_token = 'c348b6767f9805a5d73c81d88dc758ff'

client = TwilioRestClient(account=account_sid, token=auth_token)

message = client.messages.create(
        body='Hello from Case.by',
        to='375292016277',
        from_='375298070096'
    )

print message.sid
