from input_mobile import telegram


def test_send_message():
    r = telegram.send_message('Hello, Carlos!')
    assert r.status_code == 200
    print(r.json())


def test_read_last_message():
    text = telegram.read_last_message()
    print(f'text: {text}')
    assert text == '3'


def test_input():
    msg = telegram.input_('What is your name?', debug=True, alert_via_sms=False)
    assert msg == 'Carlos'
