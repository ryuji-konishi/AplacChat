# -*- coding: utf-8 -*-
import re

import resources.loader as rl
import utils.vocab_utils as vocab_utils
from common import char_utils as cu

myname = '田村'
yourname = '田村さん'
html_target_tag = ['h1', 'h2', 'h3', 'h4', 'h5']

# Regular expressions to remove character patterns from source and target
regexs_both = [
    # ESSAY 452／（１） 〜これまで
    u'^ESSAY [0-9|０-９]+', 
    # Part 01：最強最速の情況記憶
    u'^Part [0-9|０-９| ]+[.|．|:|：]', 
    # ２．学生ビザの取得方法
    u'^[0-9|０-９| ]+[.|．|:|：]',
    # 1-1.概況　オーストラリアの犯罪状況
    u'^[0-9|０-９| ]+[-|－|−]+[0-9|０-９| ]+[.|．|:|：]*',
    # beginning of
    u'^[　|～|〜|－|／|、|●|★|■|→|:|;|~]+', 
    # numbers in brackets at the beginning （１） （その１）これまで
    u'^[(|\\[|\\{|<|（|【|｛|＜][0-9|０-９|その| ]+[)|\\]|\\}|>|）|】|｝|＞]',
    # numbers in brackets at the end  これまで（１）（その１）
    u'[(|\\[|\\{|<|（|【|｛|＜][0-9|０-９|その| ]+[)|\\]|\\}|>|）|】|｝|＞]$',
    # constant keywords at the beginning
    u'^[日本／|◆コラム|今週の１枚|更新記録簿|を|初稿福島記]',
    # exact line
    u'^Home$|^ツイート$',
    # Copyright 1996
    u'Copyright [0-9|０-９|-|－|−]+',
    # email address
    u'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+']

# Regular expressions to remove from source
regexs_src = [
    # repeating symbol characters at the beginning
    u'^[!#%&\\)\\*\\+,\\-\\./:;=>\\?@\\\\\\]\\^_`|\\}~¢¤§¨­®°±´¸×÷‐―‥…※℃ⅠⅡⅢⅣ←↑→↓⇔∀−∥∪≒≠≦≪≫━■□▲△▼▽◆◇○◎●◯★☆♪♬♭、。々〇〉》」』】〒〕〜゛゜・ー㎡！＃％＆）＊＋，－．／：；＝＞？＠＼］＾＿｀｝～｣､]+',
    # any of / ／ ・  ＊ ＃
    u'[/／・＊＃]']

def get_symbol_ratio(text):
    """ Calculate the ratio of symbol characters contained in the given text.
        For example, '!@#$%' is 100%, and 'abcdef' is 0%.
    """
    # count the number of symbol characters in text
    cnt = 0
    for char in text:
        if cu.is_char_ascii_symbol(char) or cu.is_char_full_symbol(char):
            cnt += 1

    # return the ratio
    if len(text) == 0:
        return 0
    else:
        return cnt / len(text)

def get_number_ratio(text):
    """ Calculate the ratio of number characters contained in the given text.
        For example, '01234' is 100%, and 'abcdef' is 0%.
    """
    # count the number of number characters in text
    cnt = 0
    for char in text:
        if cu.is_char_ascii_number(char) or cu.is_char_full_number(char):
            cnt += 1

    # return the ratio
    if len(text) == 0:
        return 0
    else:
        return cnt / len(text)

def regex_trim(text, reg_exps):
    """ Remove the keyword being matched with regular expression and return the result.
        reg_exps is a list of regular expression strings.
    """
    # Loop until trimming has no effect
    while True:
        buf = text
        for regex in reg_exps:
            buf = re.sub(regex, '', buf).strip()
        if text == buf:     # no difference between before and after.
            break
        text = buf
    return text

def contains(text, phrases):
    for phrase in phrases:
        if phrase in text:
            return True
    return False

def validate_pair_html(source, target):
    """ This is a function that takes source/target text pairs from the or HTML parsers, 
        and it decides if the texts are valid and to be processed and stored into corpus.
    """
    if get_symbol_ratio(source) >= 0.5:
        return '', ''
    if get_number_ratio(source) >= 0.5:
        return '', ''

    # Ignore any texts that contain specific phrases.
    ignore_phrases = [
        u'→MORE', u'★→', u'→APLaCの総合トップに戻る']
    if contains(source, ignore_phrases) or contains(target, ignore_phrases):
        return '', ''

    source = regex_trim(source, regexs_both)
    source = regex_trim(source, regexs_src)
    target = regex_trim(target, regexs_both)

    if len(source) > 200 or len(target) > 200:
        return '', ''   # skip too long
    if len(source) < 3 or len(target) < 3:
        return '', ''   # skip too short
    return source.strip(), target.strip()

def validate_pair_corpus(source, target):
    """ This is a function that takes source/target text pairs from the corpus resouces,
        and it decides if the texts are valid and to be processed and stored into corpus.
    """
    return source, target

class SaluteLoader(object):
    """ Salute sentense pair resource loader class.
        The initial data is loaded from CSV file during development.
    """
    def __init__(self, lang = 'jpn'):
        self.delegate = rl.MultiColInitLoader(__file__,
            'salute', 'salute_' + lang + '.json', 'salute_' + lang + '.csv')

    def load(self):
        """ Load and return a set of source/target list. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

class ConversationLoader(object):
    """ Conversation sentense pair resource loader class.
        The initial data is loaded from CSV file during development.
    """
    def __init__(self, lang = 'jpn'):
        self.delegate = rl.MultiColInitLoader(__file__,
            'conversation', 'conversation_' + lang + '.json', 'conversation_' + lang + '.csv')

    def load(self):
        """ Load and return a set of source/target list. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

