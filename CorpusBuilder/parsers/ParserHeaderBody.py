import os
import sys
from bs4 import BeautifulSoup, element
from abc import ABC, abstractmethod
from html.parser import HTMLParser
import utils.header_utils as header_utils
import utils.utils as utils

class Parser(object):
    def __init__(self, result_store, target_tag = None):
        self.result_store = result_store
        if target_tag:
            self.target_tags = [target_tag]
        else:
            self.target_tags = header_utils.header_tags

    def parse(self, html):
        for target_tag in self.target_tags:
            # self.delegate = BS_HeaderBodyParser(target_tag, self.result_store)
            self.delegate = HTML_HeaderBodyParser(target_tag, self.result_store)
            self.delegate.feed(html)
            self.delegate.flash_into_file()

# BeautifulSoup version
class BS_AbstractHeaderBodyParser(ABC):
    def __init__(self):
        pass

    def feed(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        for t in soup.body.contents:
            self._parse_tag(t)
        self.parse_finish()

    def _parse_tag(self, tag):
        if isinstance(tag, element.NavigableString):
            self.handle_data(tag)
        elif isinstance(tag, element.Tag):
            self.handle_starttag(tag)
            for c in tag.contents:
                self._parse_tag(c)
            self.handle_endtag(tag)

    @abstractmethod
    def handle_starttag(self, tag):
        pass

    @abstractmethod
    def handle_endtag(self, tag):
        pass

    @abstractmethod
    def handle_data(self, data):
        pass

    @abstractmethod
    def parse_finish(self):
        pass

class BS_HeaderTag(object):
    def __init__(self, tag):
        if isinstance(tag, element.Tag):
            tag = tag.name
        self.tag = header_utils.Header(tag)
        self.data = ''
    
    def is_same_level(self, other_tag):
        other = header_utils.Header(other_tag.name)
        return self.tag == other

    def is_upper_than(self, other_tag):
        other = header_utils.Header(other_tag.name)
        # H1 is upper than H2. Below is 1 < 2.
        return self.tag < other

    def is_lower_than(self, other_tag):
        other = header_utils.Header(other_tag.name)
        # H2 is lower than H1. Below is 2 > 1.
        return self.tag > other


class BS_HeaderBodyParser(BS_AbstractHeaderBodyParser):
    def __init__(self, target_tag, result_store):
        BS_AbstractHeaderBodyParser.__init__(self)
        self.target = BS_HeaderTag(target_tag)
        self.result_store = result_store
        self.current = None
        self.body = ''
        self.is_waiting_target_endtag = False
        self.is_processing_header_tag = False
        self.processing_tag = ''

    def handle_starttag(self, tag):
        self.processing_tag = tag
        self.is_processing_header_tag = header_utils.is_header_tag(tag.name)
        if not self.is_processing_header_tag:
            return

        if not self.current:
            if self.target.is_same_level(tag):
                # Start the data process.
                self.current = BS_HeaderTag(tag)
                self.body = ''
                self.is_waiting_target_endtag = True
        elif self.current.is_same_level(tag):
            # If we encounter the same level tag,
            # export the currently processed data.
            self.flash_into_file()
            # Then start the next data process.
            self.current = BS_HeaderTag(tag)
            self.is_waiting_target_endtag = True
        elif self.current.is_lower_than(tag):
            # If we encounter the upper level tags (ex H1 is upper than H2),
            # export the currently processed data.
            self.flash_into_file()
            # Clear the current state. Then wait for the next data process.
            self.is_waiting_target_endtag = False

    def handle_endtag(self, tag):
        if not header_utils.is_header_tag(tag.name):
            return
        elif self.target.is_same_level(tag):
            self.is_waiting_target_endtag = False

    def handle_data(self, data):
        data = utils.trim_structural_char(data)
        if len(data) == 0:
            return
        if self.current:
            if self.is_processing_header_tag:
                if self.is_waiting_target_endtag:
                    self.current.data += data
            elif not utils.is_literal_tag(self.processing_tag.name):
                return
            elif self.body:
                self.body += '\n' + data
            else:
                self.body = data

    def parse_finish(self):
        # If there is data on hold, export it into file.
        self.flash_into_file()
        
    def flash_into_file(self):
        if self.current and self.body:
            self.result_store.store_result(self.current.data, self.body)
            self.current = None
            self.body = ''

# HTML Parser version
class HTML_HeaderTag(object):
    def __init__(self, tag_str):
        self.tag = header_utils.Header(tag_str)
        self.data = ''
    
    def is_same_level(self, other_tag_str):
        other = header_utils.Header(other_tag_str)
        return self.tag == other

    def is_upper_than(self, other_tag_str):
        other = header_utils.Header(other_tag_str)
        # H1 is upper than H2. Below is 1 < 2.
        return self.tag < other

    def is_lower_than(self, other_tag_str):
        other = header_utils.Header(other_tag_str)
        # H2 is lower than H1. Below is 2 > 1.
        return self.tag > other

class HTML_HeaderBodyParser(HTMLParser):
    def __init__(self, target_tag, result_store):
        HTMLParser.__init__(self)
        self.target = HTML_HeaderTag(target_tag)
        self.result_store = result_store
        self.current = None
        self.body = ''
        self.is_waiting_target_endtag = False
        self.is_processing_header_tag = False
        self.processing_tag = ''

    def handle_starttag(self, tag, attrs):
        self.processing_tag = tag
        self.is_processing_header_tag = header_utils.is_header_tag(tag)
        if not self.is_processing_header_tag:
            return

        if not self.current:
            if self.target.is_same_level(tag):
                # Start the data process.
                self.current = HTML_HeaderTag(tag)
                self.body = ''
                self.is_waiting_target_endtag = True
        elif self.current.is_same_level(tag):
            # If we encounter the same level tag,
            # export the currently processed data.
            self.flash_into_file()
            # Then start the next data process.
            self.current = HTML_HeaderTag(tag)
            self.is_waiting_target_endtag = True
        elif self.current.is_lower_than(tag):
            # If we encounter the upper level tags (ex H1 is upper than H2),
            # export the currently processed data.
            self.flash_into_file()
            # Clear the current state. Then wait for the next data process.
            self.is_waiting_target_endtag = False

    def handle_endtag(self, tag):
        if tag.lower() == 'html':
            # This means the HTML parsing is ending.
            # If there is data on hold, export it into file.
            self.flash_into_file()
        elif not header_utils.is_header_tag(tag):
            return
        elif self.target.is_same_level(tag):
            self.is_waiting_target_endtag = False

    def handle_data(self, data):
        data = utils.trim_structural_char(data)
        if len(data) == 0:
            return
        if self.current:
            if self.is_processing_header_tag:
                if self.is_waiting_target_endtag:
                    self.current.data += data
            elif not utils.is_literal_tag(self.processing_tag):
                return
            elif self.body:
                self.body += '\n' + data
            else:
                self.body = data

    def flash_into_file(self):
        if self.current and self.body:
            self.result_store.store_result(self.current.data, self.body)
            self.current = None
            self.body = ''

