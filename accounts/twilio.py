from ePalace.private import ACCOUNT_SID, AUTH_TOKEN

def send_sms(message, to_):
    from twilio.rest import Client

    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages.create(
            body = message,
            from_ = '+12402734022',
            to = to_,
        )
    print(message.sid)


def gen_otp():
    import math, random
    digits = '1234567890'
    OTP = ''
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP