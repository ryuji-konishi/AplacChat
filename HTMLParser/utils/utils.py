
def split_jpn_sentence(sentence):
    """ Split a Japanese sentence into a list and return it"""
    return split_sentence(sentence, '。')

def split_sentence(sentence, delimiter):
    """ Split sentence into a list and return it"""
    result = [sentence]
    if delimiter in sentence:
        r = sentence.split(delimiter)
        result = [a + delimiter for a in r if a]
    return result

def is_valid_text(string):
    valid = True
    if not string:
        valid = False
    elif not isinstance(string, str):
        valid = False
    else:
        # Clean text
        string = remove_structural_char(string)
        if len(string) < 1:
            valid = False
    return valid

def trim_structural_char(string):
    """ Trim trailing and proceeding structural characters (invisible) from the string."""
    if len(string) == 0:
        return ''
    spc = ['\t', '\n', ' ', '　']
    # Check the first character
    while len(string) > 0 and string[0] in spc:
        string = string[1:]
    # Check the last character
    while len(string) > 0 and string[-1] in spc:
        string = string[:-1]
    return string

def remove_structural_char(string):
    """ Remove structural characters (invisible) from the string."""
    spc = ['\t', '\n', ' ', '　']
    for s in spc:
        string = string.replace(s, '')
    return string

def is_literal_tag(tag_str):
    spt = ['script', 'style', 'noscript', 'object', 'source', 'time', 'video', 'button', 'img', 'map']
    if tag_str.lower() in spt:
        return False
    else:
        return True

