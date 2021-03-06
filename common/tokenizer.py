# -*- coding: utf-8 -*-
import sys
from common.dictionary import Dictionary as dic
from common import char_utils
from io import StringIO

# Special tokens that are used in the vocaburary file. These are required to represent to 
# indicate special directions to the seq2seq RNN.
special_tokens = [u'<unk>', u'<s>', u'</s>', u'<br>', u'<sp>', u'<fp>']

# Special tokens that are used for letter case upper/lower patterns.
letter_case_tokens = [u'<c1>', u'<c2>']
special_tokens.extend(letter_case_tokens)       # Combine special tokens so that they are stored in to vocab file together.

# Define special characters that are handled as a 'single word' in the vocaburary no matter
# what context it's being used. 
special_atoms = []
special_atoms.extend(char_utils.get_chars_ascii_number())
special_atoms.extend(char_utils.get_chars_ascii_symbol())
special_atoms.extend(char_utils.get_chars_full_number())
special_atoms.extend(char_utils.get_chars_full_symbol())
special_atoms.remove(u"'")

# Define terminating characters that are specifically handled as a 'single word' in the vocaburary. 
# For example, "A car." is devided into "A", "car" and ".".
special_terminators = [u'.']
  
# Define quoting characters that are specifically handled as a 'single word' in the vocaburary. 
# For example, '"car"' is devided into '"', "car" and '"'.
# special_quoates = [u'"']

# Define bracket characters that are specifically handled as a 'single word' in the vocaburary. 
# For example, if you have a sentense "(Hello world)", you don't want it be devided into two words "(Hello" and "World)". 
# Instead, get four words "(", "Hellow", "World" and ")".
# It's important that they have to appear as a pair in a sentense and also in a right order. 
# For example, "(Hello World)" is correct but "(Hello World]" is not. Also ")Hello World(" is not correct.
# special_brackets = [
#     [u'(', ')'],
#     [u'{', '}'],
#     [u'[u', ']'],
#     [u'“', '”'],
#     [u'（', '）'],
#     [u'(', '）'],
#     [u'（', ')'],
#     [u'「', '」'],
#     [u'【', '】'],
#     [u'『', '』'],
#     [u'＜', '＞']
# ]

""" MeCab was once considered but decided not to use as of Apr.2018 """
# if (sys.version_info > (3, 0)):
#      # Python 3 code in this block
#     class _MeCab(object):
#         def __init__(self):
#             import MeCab
#             self.m = MeCab.Tagger("-Owakati")   # Option wakati splits text into words concatenated by space ' '

#         def tokenize(self, text):
#             words_text = self.m.parse(text)
#             return words_text.split()           # Split text by space into a list
# else:
#      # Python 2 code in this block
#     class _MeCab(object):
#         def __init__(self):
#             import MeCab
#             self.m = MeCab.Tagger("-Owakati")   # Option wakati splits text into words concatenated by space ' '

#         def tokenize(self, text):
#             words_text = self.m.parse(text.encode('utf8'))
#             words_text = unicode(words_text, 'utf8')
#             return words_text.split()           # Split text by space into a list


class tokenizer(object):

    def __init__(self):
        self.dic = dic.Dictionary()
        self.tagger = LetterCaseTagger()
        # self.morph_tokenizer = _MeCab()     # The delegated morphological analyzer tokenizer

    # def _morph_tokenize(self, texts):
    #     """ Loop throught the text list, and tokenize the text into multiple words
    #         by the morphological analyzer tokenizer.
    #         Return the list of tokenized words.
    #     """
    #     result = []
    #     for text in texts:
    #         if len(text) > 1 and text not in special_tokens:
    #             words = self.morph_tokenizer.tokenize(text)
    #             result.extend(words)
    #         else:
    #             result.append(text)
    #     return result

    def split(self, sentense):
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
            G) 'He said "What's up?"' -> ['He', 'said', '"', '<c1>', "what's", 'up', '?', '"']
        """
        texts = [sentense.replace(u'\n', u' <br> ').replace(u'　', u' <fp> ')]

        words = self._split_by_space(texts)
        for atom in special_atoms:
            words = self._split_by_atomic(atom, words)
        words = self._split_by_char_code(words)
        words = self._split_by_terminator(words)
        words = self._breakdown(words)
        words = self._letter_case(words)

        # words = self._morph_tokenize(words)

        return words

    def concatenate(self, words):
        """ Combine the given list into a single text. This function works oppoisite
            from split. The special tokens are decoded into the
            actual character for example '<br>' tag is converted into line-break.
            A) ['abc', 'def'] -> 'abc def'
            B) ['<c1>', 'that', "isn't", 'cat', '.', '<c1>', 'that', 'is', 'a', 'dog', '.'] -> 'That isn't cat. That is a dog.'
            C) ['abc', 'あ', 'い', 'う', 'def'] -> 'abcあいうdef'
            D) ['abc', 'def', 'あ', 'い', '　', 'う', 'え', 'お'] -> 'abc defあい　うえお'
            E) ['abc', '<br>', 'def'] -> 'abc\ndef'
            F) ['abc', '<sp>', 'def'] -> 'abc  def'
        """
        result = u''
        prev_ascii = False
        case_tag = ''
        for word in words:
            if self.tagger.isCaseTag(word):
                case_tag = word
                continue
            else:
                if word == u'<sp>':
                    result += u' '
                    continue
                elif word == u'<br>':
                    result += u'\n'
                    prev_ascii = False
                    continue
                elif word == u'.':
                    result += u'.'
                    continue
                elif word == u'<fp>':
                    result += u'　'
                    continue
            
            # If you get here with case_tag value, change the case of word accordingly.
            if case_tag:
                word = self.tagger.untag([case_tag, word])
            case_tag = ''

            # Check the word is all in ASCII. If the previous word is also in ASCII,
            # insert space in between.
            if self._is_ascii(word):
                if prev_ascii:
                    result += u' ' + word
                else:
                    result += word
                prev_ascii = True
            else:
                result += word
                prev_ascii = False

        return result

    def _split_by_brackets(self, _open, _close, texts):
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
                s = StringIO(text)
                # The result is temporary collected in this list. If the brackets are correctly found, this list will become the result.
                tempResult = []
                while True:
                    resultText = u''
                    openFound = False
                    closeFound = False

                    while True:
                        char = s.read(1)
                        if char == u'':
                            break;
                        # First look for the open bracket
                        if openFound == False and char == _open:
                            openFound = True
                            if len(resultText) > 0:
                                tempResult.append(resultText)
                            tempResult.append(char)
                            resultText = u''
                        # If open bracket is found, look for close bracket
                        elif openFound == True and char == _close:
                            closeFound = True
                            if len(resultText) > 0:
                                tempResult.append(resultText)
                            resultText = u''
                            tempResult.append(char)
                            break;
                        else:
                            resultText += char

                    # Check if the close bracket is found.
                    if openFound and closeFound:
                        if  len(resultText) > 0:
                            tempResult.append(resultText)
                    elif len(resultText) > 0:
                        # If not, that means the bracket order is not right, and the text is not delimited.
                        tempResult.append(resultText)
                    elif openFound:
                        # The stream reached to the end while the brackets are in a wrong order.
                        tempResult = []
                        break;
                    else:
                        # The stream reached to the end
                        break;

                if len(tempResult) > 0:
                    # Push the temporary list as the result.
                    result.extend(tempResult)
                else:
                    # This means the brackets are in a wrong order.
                    result.append(text)

        return result

    # Below is unused because it collides with _split_by_brackets() above. They can't be used at the same time
    # because when brackets and quotes are nested, once a sentense is chopped off into snipets of words, 
    # you can't tell which of bracktes and quotes are in the upper layer of nesting.
    def _split_by_quote(self, quote, texts):
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
                        resultText = u''
                    else:
                        resultText += char
                if  len(resultText) > 0:
                    result.append(resultText)
        return result

    def _split_by_space(self, texts):
        """ Take a list of text, devide by ' ' into list, and return all words in a single list.
            By splitting with ' ', if several ' ' appears in the given sentense continuously,
            they result in the empty text in the result list. In that case, put the special
            token of <sp> so that the space is embedded into the vocabulary.
        """
        result = []
        for text in texts:
            for word in text.split(u' '):
                if len(word) == 0:
                    result.append(u'<sp>')
                    continue
                
                if (len(word)):
                    result.append(word)
        return result

    def _split_by_atomic(self, atom, words):
        """ Take a list of word, devide by atomic character into list, and return all words in a single list.
            For example, 'abc,def' -> ['abc', ',', 'def']
        """
        result = []
        for word in words:
            if len(word) > 1 and word not in special_tokens:
                buf = u''
                for char in word:
                    if char == atom:
                        if len(buf):
                            result.append(buf)
                            buf = u''
                        result.append(atom)
                    else:
                        buf += char

                if len(buf):
                    result.append(buf)
            else:
                result.append(word)

        return result

    def _split_by_terminator(self, words):
        """ Loop throught the word list, and if the word ends with a terminator(ex period), separte it.
        """
        result = []
        for word in words:
            if len(word) == 1:
                result.append(word)
            elif len(word) > 1:                
                lastChar = word[-1]
                if lastChar in special_terminators:
                    result.append(word[:-1])  # remove the last character
                    result.append(lastChar)
                else:
                    result.append(word)
        return result

    def _breakdown(self, words):
        """ Loop throught the word list, and if the word is not in language dictionary
            break the word into characters.
        """
        result = []
        for word in words:
            if len(word) > 1 and word not in special_tokens:
                exists = self.dic.Check(word)
                if exists:
                    result.append(word)
                else:
                    for char in word:
                        result.append(char)
            else:
                result.append(word)
        return result

    def _letter_case(self, words):
        """ Loop throught the word list, and describe each word for the letter case patterns with tag.
        """
        result = []
        for word in words:
            if len(word) > 1 and self._is_ascii(word):
                tagged = self.tagger.tag(word)
                result.extend(tagged)
            else:
                result.append(word)
        return result

    def _split_by_quote(self, words):
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

    def _split_by_char_code(self, words):
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

            buf = u''
            for char in word:
                if ord(char) < 128:     # check if ASCII
                    buf += char
                    code_change = 0
                else:
                    if code_change ^ 1 and len(buf) > 0:
                        result.append(buf)
                        buf = u''
                    result.append(char)
                    code_change = 1
            
            if (len(buf)):
                result.append(buf)

        return result

    def _is_ascii(self, word):
        return all(ord(c) < 128 for c in word)

class LetterCaseTagger(object):

    def __init__(self):
        pass

    def isCaseTag(self, word):
        """ Return if the given word is a reserved tag token text for this class object."""
        return word in letter_case_tokens

    def tag(self, word):
        """ Check the given word in each letter and return the description of the case patterns.
            For example;
            'apple' -> ['apple']
            'Apple' -> ['<c1>', 'apple']
            'APPLE' -> ['<c2>', 'apple']
            'aPple' -> ['aPple']

            Thus the given word has to be in latin language (English, French etc).
            The returning value is a list of texts. 
        """
        result = []
        if word[0].isupper():
            if all(c.isupper() for c in word):
                result.append(u'<c2>')
            else:
                result.append(u'<c1>')
            result.append(word.lower())
        else:
            result.append(word)
        return result

    def untag(self, words):
        """ Return the untagged text of given word.
            For example;
            ['<c1>', 'apple'] -> 'Apple'
            ['<c2>', 'apple'] -> 'APPLE'
            ['apple'] -> 'apple'
            ['aPple'] -> 'aPple'
        """
        if words[0] == '<c1>':
            result = words[1].title()
        elif words[0] == '<c2>':
            result = words[1].upper()
        else:
            result = words[0]
        return result
