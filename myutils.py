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
