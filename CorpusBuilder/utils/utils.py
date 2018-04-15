# -*- coding: utf-8 -*-
import collections
import random

def split_jpn_sentence(sentence):
    """ Split a Japanese sentence into a list and return it"""
    return split_sentence(sentence, u'。')

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

def distribute(lst, ratio):
    """ Divide the list into multiple lists with ratio.
        The ratio is a tuple containing the distribution ratios in float totaling 1.
    """
    if sum(ratio) != 1:
        raise ValueError("The ratio has to add up to 1.")

    result_lists = []

    # List of each length of result lists.
    ratio_lens = [int(len(lst) * r) for r in ratio]
    st = 0
    for l in ratio_lens:
        result_lists.append(lst[st:st + l])
        st += l

    return tuple(result_lists)

def distribute_rnd(lst, ratio):
    """ Distribute the list randomly into multiple lists.
        The ratio is a tuple containing the distribution ratios in float totaling 1.
    """
    random.shuffle(lst)
    return distribute(lst, ratio)

def sort_unicode_word_list(words):
    """ Sort the given list of words by Unicode code point value. """
    words.sort()

