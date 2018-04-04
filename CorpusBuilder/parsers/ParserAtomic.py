import os
import sys
from html.parser import HTMLParser
import utils.header_utils as header_utils
import utils.utils as utils

class Parser(object):
    def __init__(self, result_store):
        self.result_store = result_store

    def parse(self, html):
        self.delegate = _MyParser(self.result_store)
        self.delegate.feed(html)


class _MyParser(HTMLParser):
    def __init__(self, result_store):
        HTMLParser.__init__(self)
        self.result_store = result_store
        self.is_literal_tag = False
        self.sources = []
        self.targets = []
        self.prev_text = None

    def handle_starttag(self, tag, attrs):
        self.is_literal_tag = utils.is_literal_tag(tag)

    def handle_endtag(self, tag):
        if tag.lower() == 'html':
            # This means the HTML parsing is ending.
            # If there is data on hold, export it into file.
            self.flash_into_file()

    def handle_data(self, data):
        if not self.is_literal_tag:     # Avoid script tag etc
            return

        data = data.strip()
        if len(data) > 0:
            buf_list = utils.split_jpn_sentence(data)
            self.sliding_push(buf_list)

    def sliding_push(self, list_texts):
        """Loop through the given list and push each element into
            either source or target list via sliding window which is a
            2 words sized and shifts though the input by each word.
            This means that the 2 words are taken from the input,
            the 1st word goes into the source, and the 2nd goes into
            target. The window is shifted by 1, 2 words are taken from
            the input again, and this time its 1st word is the 2nd word
            of the previous iteration, and they go into source/target
            respectively.
            For example, if the given list is ['A', 'B', 'C'], then 
            the source list will contain ['A', 'B'] and the target list
            will contains ['B', 'C'].
            The last state parsists. This means that if the given input 
            list is shorter than 2, then the word is pushed into source,
            then this function waits for the next call. At the next call,
            the 1st element in the list goes into target.
        """
        for t in list_texts:
            if len(t) == 0:
                continue
            if self.prev_text:
                self.sources.append(self.prev_text)
                self.targets.append(t)
                self.prev_text = t
            else:
                self.prev_text = t


    def flash_into_file(self):
        if len(self.sources) > 0 and len(self.targets) > 0:
            self.result_store.store_result(self.sources, self.targets)

