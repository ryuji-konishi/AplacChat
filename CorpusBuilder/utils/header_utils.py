header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']      # all h tags defined
tag_map = dict(zip(header_tags, range(len(header_tags))))

def is_header_tag(tag_str):
    if tag_str.lower() in header_tags:
        return True
    else:
        return False

class Header(object):
    def __init__(self, tag_str):
        """ tag_str: The HTML header tag name text ex 'H1', 'H2' etc"""
        self.name = tag_str.lower()
        self.ID = tag_map[self.name]

    def __lt__(self, other):
        """ Operator '<'"""
        return self.ID < other.ID
    def __le__(self, other):
        """ Operator '<='"""
        return self.ID <= other.ID
    def __eq__(self, other):
        """ Operator '=='"""
        return self.ID == other.ID
    def __ne__(self, other):
        """ Operator '!='"""
        return self.ID != other.ID
    def __ge__(self, other):
        """ Operator '>='"""
        return self.ID >= other.ID
    def __gt__(self, other):
        """ Operator '>'"""
        return self.ID > other.ID

if __name__ == "__main__":
    h1 = Header('h1')
    h2 = Header('h2')

    print (h1 < h2)

