import logging

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

def extract_user_id(request_body):
    message = extract_message(request_body)
    return message.get('from').get('id')


def handle_message(commander, cmd, request_body, params):
    if commander.has_command(cmd):
        return [commander.execute(cmd, request_body, params)]
    else:
        text = ' '.join(params)
        replies = commander.execute_other(request_body, cmd + text)
        logging.info('Replies: {}'.format(replies))
        real_replies = [ x for x in replies if x is not '' ]
        if len(real_replies) == 0:
            return ['I got your message! (but I do not know how to answer)']
        else:
            return real_replies
