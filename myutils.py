def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def split_text(text):
    split_text = text.split()
    cmd, params = split_text[0], split_text[1:]
    return (cmd, params)

def extract_message(request_body):
    try:
        return request_body['message']
    except:
        return request_body['edited_message']

def extract_date(request_body):
    message = extract_message(request_body)
    return message.get('date')

def extract_user_first_name(request_body):
    message = extract_message(request_body)
    return message.get('from').get('first_name')
