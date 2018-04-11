import os

import resources.loader as ld

class TextPair(object):
    """ Used for the set version of multiplier. Resulted in being slower than list version. Not used. """
    def __init__(self, text1, text2):
        self.text1 = text1
        self.text2 = text2
        self.h = hash(text1 + text2)
    def __eq__(self, other):
        return self.text1 == other.text1 and self.text2 == other.text2

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.h

class _Multiplier(object):
    def __init__(self, tag, elements):
        self.tag = tag
        self.elements = elements

    def multiply(self, srcs, tgts):
        result_srcs = []
        result_tgts = []
        for src, tgt in zip(srcs, tgts):
            if self.tag in src or self.tag in tgt:
                for txt in self.elements:
                    result_srcs.append(src.replace(self.tag, txt))
                    result_tgts.append(tgt.replace(self.tag, txt))
            else:
                result_srcs.append(src)
                result_tgts.append(tgt)
        return result_srcs, result_tgts

    def multiply_set(self, pairs):
        """ Set version of process. Resulted in being slower than list version. Not used. """
        result = set()
        for pair in pairs:
            src = pair.text1
            tgt = pair.text2
            if self.tag in src or self.tag in tgt:
                for txt in self.elements:
                    s = src.replace(self.tag, txt)
                    t = tgt.replace(self.tag, txt)
                    result.add(TextPair(s, t))
            else:
                result.add(TextPair(src, tgt))
        return result

class NameMultiplier(_Multiplier):
    def __init__(self, names = None):
        if not names:
            rl = ld.NameLoader()
            names = rl.load_names()
        _Multiplier.__init__(self, '{name}', names)

class CityMultiplier(_Multiplier):
    def __init__(self, cities = None):
        if not cities:
            rl = ld.CityLoader()
            cities = rl.load_cities()
        _Multiplier.__init__(self, '{city}', cities)


