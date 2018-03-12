# -*- coding: utf-8 -*-

# Special tokens that are used in the vocaburary file. These are required to represent to 
# indicate special directions to the seq2seq RNN.
special_tokens = ['<unk>', '<s>', '</s>', '<br>', '<sp>']

# Define terminating characters that are specifically handled as a 'single word'. 
# For example, "A car." is devided into "A", "car" and ".".
special_terminators = ['.', ',']

# Define quoting characters that are specifically handled as a 'single word'. 
# For example, '"car"' is devided into '"', "car" and '"'.
special_quoates = ['"']

# Define bracket characters that are specifically handled as a 'single word' in the vocaburary. 
# For example, if you have a sentense "(Hello world)", you don't want it be devided into two words "(Hello" and "World)". 
# Instead, get four words "(", "Hellow", "World" and ")".
# It's important that they have to appear as a pair in a sentense and also in a right order. 
# For example, "(Hello World)" is correct but "(Hello World]" is not. Also ")Hello World(" is not correct.
special_brackets = [
    ['(', ')'],
    ['[', ']'],
    ['“', '”'],
    ['（', '）'],
    ['「', '」'],
    ['【', '】'],
    ['『', '』'],
    ['＜', '＞']
]

def delimit_multi_char_text(sentense):
    """ Split the given sentense into a list at each character/word level
         considering multibyte character encoding in the following way.
         Also the special characters are symbolized for example line-break 
         is replaced as with '<br>' tag.
        A) 'abc def' -> ['abc', 'def']
        B) 'That isn't cat. That is a dog.' -> ['That', "isn't", 'cat', '.', 'That', 'is', 'a', 'dog', '.']
        C) 'abcあいうdef' -> ['abc', 'あ', 'い', 'う', 'def']
        D) 'abc defあい　うえお' -> ['abc', 'def', 'あ', 'い', '　', 'う', 'え', 'お']
        E) 'abc\ndef' -> ['abc', '<br>', 'def']
        F) 'abc  def' -> ['abc', '<sp>', 'def']
        G) 'He said "What's up?"' -> ['He', 'said', '"', What's", 'up?', '"']
    """
    texts = [sentense.replace('\n', ' <br> ')]

    for pair in special_brackets:
        texts = _delimit_texts_by_brackets(pair[0], pair[1], texts)

    words = _delimit_texts_by_space(texts)

    words = _delimit_words_by_quote(words)

    words = _delimit_words_by_char_code(words)

    words = _delimit_words_by_terminator(words)

    return words

def _delimit_texts_by_brackets(_open, _close, texts):
    """ Take a list of text, devide by brackets, and return all words in a single list.
        Brackets are handled as a single word. Brackets have to be a pair of open bracket and close bracket.
        For example, '(abc)' -> ['(', 'abc', ')']
    """
    result = []
    for text in texts:
        # First of all, check if the text contains both open and close brackets.
        if not (_open in text and _close in text):
            # If not, here we have nothing to worry. The result text is not delimited.
            result.append(text)
        else:
            # Now we know that the text contains both open and close. But we don't know how many and their order.
            # Devide the text by close bracket, and loop through it. The open bracket has to appear first.
            for words in text.split(_close):
                if len(words) == 0: # This is the case if the close bracket is either the first or the last character in the text.
                    continue
                words += _close     # Append the close because split() function removes it.
                resultText = ''
                openFound = False
                closeFound = False
                # The result is temporary collected in this list. If the brackets are correctly found, this list will become the result.
                tempResult = []
                for char in words:
                    # First look for the open bracket
                    if openFound == False and char == _open:
                        openFound = True
                        if len(resultText) > 0:
                            tempResult.append(resultText)
                        tempResult.append(char)
                        resultText = ''
                    # If open bracket is found, look for close bracket
                    elif openFound == True and char == _close:
                        closeFound = True
                        if len(resultText) > 0:
                            tempResult.append(resultText)
                        tempResult.append(char)
                        resultText = ''
                    else:
                        resultText += char
                if  len(resultText) > 0:
                    tempResult.append(resultText)
                # Check if the close bracket is found.
                if closeFound:
                    # Push the temporary list as the result.
                    result.extend(tempResult)
                else:
                    # If not, that means the bracket order is not right, and the text is not delimited.
                    result.append(words)

    return result

# Below is unused because it collides with _delimit_texts_by_brackets() above. They can't be used at the same time
# because when brackets and quotes are nested, once a sentense is chopped off into snipets of words, 
# you can't tell which of bracktes and quotes are in the upper layer of nesting.
def _delimit_texts_by_quote(quote, texts):
    """ Take a list of text, devide by quote, and return all words in a single list.
        Quotes are handled as a single word. Quotes have to be a pair.
        For example, '"car"' -> ['"', "car", '"']
    """
    result = []
    for text in texts:
        # First of all, check if the text contains even number of quotes.
        cnt = text.count(quote)
        if cnt == 0 or cnt % 2 != 0:
            # If not, here we have nothing to worry. The result text is not delimited.
            result.append(text)
        else:
            for char in text:
                if char == quote:
                    if len(resultText) > 0:
                        result.append(resultText)
                    result.append(char)
                    resultText = ''
                else:
                    resultText += char
            if  len(resultText) > 0:
                result.append(resultText)
    return result

def _delimit_texts_by_space(texts):
    """ Take a list of text, devide by ' ' into list, and return all words in a single list.
        By splitting with ' ', if several ' ' appears in the given sentense continuously,
        they result in the empty text in the result list. In that case, put the special
        token of <sp> so that the space is embedded into the vocabulary.
    """
    result = []
    for text in texts:
        for word in text.split(' '):
            if len(word) == 0:
                result.append('<sp>')
                continue
            
            if (len(word)):
                result.append(word)
    return result

def _delimit_words_by_terminator(words):
    """ Loop throught the word list, and if the word ends with a terminator(ex period), separte it.
    """
    result = []
    for word in words:
        lastChar = word[-1]
        if lastChar in special_terminators:
            result.append(word[:-1])  # remove the last character
            result.append(lastChar)
        else:
            result.append(word)
    return result

def _delimit_words_by_quote(words):
    """ Loop throught the word list, and if the word starts or ends with quote, separte it.
    """
    result = []
    for word in words:
        if len(word) > 1:
            firstChar = word[0]
            if firstChar in special_quoates:
                result.append(firstChar)
                word = word[1:]  # remove the first character
            lastChar = word[-1]
            if lastChar in special_quoates:
                word = word[:-1]  # remove the last character
                result.append(word)
                result.append(lastChar)
            else:
                result.append(word)
        else:
            result.append(word)
    return result

def _delimit_words_by_char_code(words):
    """ Take a word and devide it into a list to return. The word is devided by character code type.
        For example, 'abcあいうdef' -> ['abc', 'あ', 'い', 'う', 'def']
    """
    result = []
    for word in words:
        # Check the 1st character and set the flag. The flag is used to check
        # if the character is changed between ASCII <-> Multibyte
        first_char = word[0]
        if ord(first_char) < 128:   # check if ASCII
            code_change = 0
        else:
            code_change = 1

        buf = ''
        for char in word:
            if ord(char) < 128:     # check if ASCII
                buf += char
                code_change = 0
            else:
                if code_change ^ 1 and len(buf) > 0:
                    result.append(buf)
                    buf = ''
                result.append(char)
                code_change = 1
        
        if (len(buf)):
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
