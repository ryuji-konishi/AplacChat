# -*- coding: utf-8 -*-
special_tokens = ['<unk>', '<s>', '</s>', '<br>', '<sp>']

def delimit_multi_char_text(text):
    """ Split the given text into a list at each character/word level
         considering multibyte character encoding in the following way.
         Also the special characters are symbolized for example line-break 
         is replaced as with '<br>' tag.
        A) 'abc def' -> ['abc', 'def']
        B) 'That isn't cat. That is a dog.' -> ['That', "isn't", 'cat', '.', 'That', 'is', 'a', 'dog', '.']
        C) 'abcあいうdef' -> ['abc', 'あ', 'い', 'う', 'def']
        D) 'abc defあい　うえお' -> ['abc', 'def', 'あ', 'い', '　', 'う', 'え', 'お']
        E) 'abc\ndef' -> ['abc', '<br>', 'def']
        F) 'abc  def' -> ['abc', '<sp>', 'def']
    """
    result = []
    text = text.replace('\n', ' <br> ')
    # By splitting with ' ', if several ' ' appears in the given text continuously,
    # they result in the empty text in the result list. In that case, put the special
    # token of <sp> so that the space is embedded into the vocabulary.
    for word in text.split(' '):
        if len(word) == 0:
            result.append('<sp>')
            continue
        
        # Check the 1st character and set the flag. The flag is used to check
        # if the character is changed between ASCII <-> Multibyte
        first_char = word[0]
        if ord(first_char) < 128:
            flag = 0
        else:
            flag = 1

        buf = ''
        for char in word:
            if ord(char) < 128:
                buf += char
                flag = 0
            else:
                if flag ^ 1 and len(buf) > 0:
                    result.append(buf)
                    buf = ''
                result.append(char)
                flag = 1
        if len(buf) > 0:
            # If the ASCII word is ending with period, separte it.
            if buf[-1] == '.':
                result.append(buf[:-1])
                result.append('.')
            else:
                result.append(buf)

    return result

def concatenate_multi_char_list(words):
    """ Combine the given list into a single text. This function works oppoisite
        from delimit_multi_char_text. The special tokens are decoded into the
        actual character for example '<br>' tag is converted into line-break.
        A) ['abc', 'def'] -> 'abc def'
        B) ['That', "isn't", 'cat', '.', 'That', 'is', 'a', 'dog', '.'] -> 'That isn't cat. That is a dog.'
        C) ['abc', 'あ', 'い', 'う', 'def'] -> 'abcあいうdef'
        D) ['abc', 'def', 'あ', 'い', '　', 'う', 'え', 'お'] -> 'abc defあい　うえお'
        E) ['abc', '<br>', 'def'] -> 'abc\ndef'
        F) ['abc', '<sp>', 'def'] -> 'abc  def'
    """
    result = ''
    prev_ascii = False
    for word in words:
        if word == '<sp>':
            result += ' '
            continue
        if word == '<br>':
            result += '\n'
            prev_ascii = False
            continue
        if word == '.':
            result += '.'
            continue
        
        # Check the word is all in ASCII. If the previous word is also in ASCII,
        # insert space in between.
        if is_ascii(word):
            if prev_ascii:
                result += ' ' + word
            else:
                result += word
            prev_ascii = True
        else:
            result += word
            prev_ascii = False

    return result

def join_list_by_space(str_list):
    return ' '.join(str_list)

def is_ascii(s):
    return all(ord(c) < 128 for c in s)
