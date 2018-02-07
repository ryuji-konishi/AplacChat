import os
import sys
from bs4 import BeautifulSoup, element
import utils.header_utils as header_utils
import utils.utils as utils

# Python 3
# from abc import ABC, abstractmethod
# from html.parser import HTMLParser
# Python 2
from abc import ABCMeta, abstractmethod
from HTMLParser import HTMLParser

class Parser(object):
    def __init__(self, result_store):
        self.delegate = TreeAtomicParser(result_store)

    def parse(self, html):
        self.delegate.feed(html)

class Node(object):
    """ This class represents a HTML object that is part of the
    HTML document.ABC
    """
    def __init__(self, parent_node = None):
        """ parent_node: The Node class object that is the parent of this node. If None this is the root node which represents the entire HTML document."""
        self.parent_node = parent_node
        self.children = []

    def to_string(self):
        """ Return a text that describes this object. For debug purpose."""
        return 'Root'

    def is_same_level(self, other_node):
        """ This method is called only when this is the root node."""
        return False

    def is_upper_than(self, other_node):
        """ This method is called only when this is the root node."""
        return True

    def is_lower_than(self, other_node):
        """ This method is called only when this is the root node."""
        return False

    def add_child(self, child_node):
        """ child_node: The Node class object that is to be added of this node's children"""
        self.children.append(child_node)

    def export(self):
        """ Return a tupple of source/target list pair of this object."""
        return [], []  # Empty because this is the root node which doesn't have any meaningful value.

    def traverse_export(self):
        """ Travel across the tree structure and collect the complete source/target pair text.
        The result is a tuple of source and target, each of which is a list of text.
        Both lists are indexed in order to be corresponding each other. One value in the source list
        corresponds to one value in the target list with the same index.
        """
        # The root node doesn't have data to export. Other than that,
        # First get the result of this object.
        source, target = self.export()
        # Next get the result from the all children and append after this object's result.
        for c in self.children:
            s, t = c.traverse_export()
            source.extend(s)    # Append the children's list to my list
            target.extend(t)
        return source, target
        
    def dump(self, indent):
        """ Travel across the tree structure and collect the complete source/target pair text.
        This behaviour is very similar to traverse_export() but the result data format is different.
        The result is the one-line text, containing the pair of source and target concatenated
        being separated with carriage return.
        """
        result = ' ' * indent + self.to_string() + '\n'
        indent += 1
        for c in self.children:
            c_result, _ = c.dump(indent)
            result += c_result
        indent -= 1
        return result, indent

class NodeHeader(Node):
    """ This class represents a HTML header tag (h1, h2 etc)
    """
    def __init__(self, parent_node, tag_str, tag_data):
        """ tag_data: The text value that is contained in the header tag. <h1>This is tag_data</h1> """
        Node.__init__(self, parent_node)
        self.tag = header_utils.Header(tag_str)
        self.data = utils.trim_structural_char(tag_data)

    def to_string(self):
        """ Return a text that describes this object. For debug purpose."""
        return self.tag.name + ' ' + self.data

    def export(self):
        """ Return a tupple of source/target list pair of this object."""
        source, target = [], []
        for c in self.children:
            targets = utils.split_jpn_sentence(c.data)
            for t in targets:
                source.append(self.data)
                target.append(t)
        return source, target

    def is_same_level(self, other_node):
        return self.tag == other_node.tag

    def is_upper_than(self, other_node):
        # H1 is upper than H2. Below is 1 < 2.
        return self.tag < other_node.tag

    def is_lower_than(self, other_node):
        # H2 is lower than H1. Below is 2 > 1.
        return self.tag > other_node.tag

class LeafBody(Node):
    """ This class represents any text section or paragrah that is considered as the
        content of the preceeding HTML header. This is a leaf node in the tree structure
        thus this node doesn't have children.
    """
    def __init__(self, parent_node, body_data):
        """ body_data: The section or paragrah text that this leaf node contains."""
        Node.__init__(self, parent_node)
        self.data = utils.trim_structural_char(body_data)

    def to_string(self):
        """ Return a text that describes this object. For debug purpose."""
        # return ''
        return self.data

    def is_same_level(self, other_node):
        """ This method is called only when this is a leaf node."""
        return False

    def is_upper_than(self, other_node):
        """ This method is called only when this is a leaf node."""
        return False

    def is_lower_than(self, other_node):
        """ This method is called only when this is a leaf node."""
        return True

class TreeParser(object):
    def __init__(self):
        self.root_node = Node()

    def feed(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        # Node pointer tracks the current node object which the following process
        # takes as a parent node. This pointer goes through the tree structure,
        # from node to node, points to a node which is the current processing parent node, 
        # and collects its child nodes.
        node_pointer = self.root_node
        for t in soup.body.contents:
            node_pointer = self._parse_tag(node_pointer, t)

    def dump(self):
        indent = 0
        result, _ = self.root_node.dump(indent)
        return result

    def _parse_tag(self, node_pointer, tag):
        if isinstance(tag, element.Comment):
            pass
        elif isinstance(tag, element.NavigableString):
            if utils.is_valid_text(tag):
                leaf = LeafBody(node_pointer, tag)
                node_pointer.add_child(leaf)
        elif isinstance(tag, element.Tag):
            if header_utils.is_header_tag(tag.name):
                data = tag.contents[0]
                node = NodeHeader(node_pointer, tag.name, data)
                if node_pointer.is_same_level(node) or node_pointer.is_lower_than(node):
                    node.parent_node = self._trace_up_to_parent(node_pointer, node)
                    node.parent_node.add_child(node)
                elif node_pointer.is_upper_than(node):
                    node_pointer.add_child(node)
                else:
                    node_pointer.add_child(node)
                node_pointer = node
            elif utils.is_literal_tag(tag.name):
                for c in tag.contents:
                    node_pointer = self._parse_tag(node_pointer, c)
        return node_pointer

    def _trace_up_to_parent(self, start_node, my_node):
        """ Trace up the tree and look for the parent node for my_node and return it."""
        n = start_node
        while n.is_same_level(my_node) or n.is_lower_than(my_node):
            n = n.parent_node
        return n

class TreeAtomicParser(TreeParser):
    def __init__(self, result_store):
        TreeParser.__init__(self)
        self.result_store = result_store

    def feed(self, html_doc):
        TreeParser.feed(self, html_doc)
        source, target = self.root_node.traverse_export()
        self.result_store.store_result(source, target)
