def send_sms(message, to_):
    from twilio.rest import Client

    account_sid = 'AC18c664854e0518c87a3bd6e0d2e1c5a5'
    auth_token = '573907788e304ac17f1e5616438f4ffc'

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