import sys
sys.path.insert(0, '..\\')  # This is required to import common

import unittest
import aplac.aplac as aplac

class TestAplac(unittest.TestCase):
    def setUp(self):
        pass

    def test_regex_trim_both(self):
        result = aplac.regex_trim(u"ESSAY 452／（１） 〜あいう", aplac.regexs_both)
        self.assertEqual(result, u"あいう")
        result = aplac.regex_trim(u"Part 01：あいう", aplac.regexs_both)
        self.assertEqual(result, u"あいう")
        result = aplac.regex_trim(u"２．あいう", aplac.regexs_both)
        self.assertEqual(result, u"あいう")
        result = aplac.regex_trim(u"1-1.あいう", aplac.regexs_both)
        self.assertEqual(result, u"あいう")
        result = aplac.regex_trim(u"abc.def-012@abc.defあいう", aplac.regexs_both)
        self.assertEqual(result, u"あいう")
        result = aplac.regex_trim(u"Copyright 1996あいう", aplac.regexs_both)
        self.assertEqual(result, u"あいう")
        result = aplac.regex_trim(u"日本／あいう", aplac.regexs_both)
        self.assertEqual(result, u"あいう")
        result = aplac.regex_trim(u"", aplac.regexs_both)
        self.assertEqual(result, u"")

    def test_regex_trim_source(self):
        result = aplac.regex_trim(u"!#%&)*+,-./:;=>?@\\]^_`|}~あいう", aplac.regexs_src)
        self.assertEqual(result, u"あいう")
        result = aplac.regex_trim(u"¢¤§¨­®°±´¸×÷‐―‥…※℃ⅠⅡⅢⅣ←↑→↓⇔∀−∥∪≒≠≦≪≫━■□▲△▼▽◆◇○◎●◯★☆♪♬♭あいう", aplac.regexs_src)
        self.assertEqual(result, u"あいう")
        result = aplac.regex_trim(u"、。々〇〉》」』】〒〕〜゛゜・ー㎡！＃％＆）＊＋，－．／：；＝＞？＠＼］＾＿｀｝～｣､あいう", aplac.regexs_src)
        self.assertEqual(result, u"あいう")
        result = aplac.regex_trim(u"/あ／い・う＊え＃お", aplac.regexs_src)
        self.assertEqual(result, u"あいうえお")

if __name__ == "__main__":
    unittest.main()


