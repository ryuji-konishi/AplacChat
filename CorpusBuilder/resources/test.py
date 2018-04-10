import sys
#sys.path.insert(0, '..\\')  # This is required to import common

import unittest
import time
import multiplexer as mpx
import loader as ld

class TestMultiplexer(unittest.TestCase):
    def setUp(self):
        pass

    def test_simple(self):
        names = ['Jack', 'George']
        pair = ["I'm {name}", "Hi {name}."]
        expected = [["I'm Jack", "I'm George"], ["Hi Jack.", "Hi George."]]

        name_mpx = mpx.NameMultiplexer(names)
        src = pair[0]
        tgt = pair[1]

        srcs = [src]
        tgts = [tgt]

        srcs, tgts = name_mpx.multiplex(srcs, tgts)

        actual = [srcs, tgts]
        self.assertListEqual(expected, actual)
        
    def test_multi(self):
        names = ['Jack', 'George']
        cities = ['Tokyo', 'Sydney']
        pairs = [
            ["I'm {name}", "Hi {name}."],
            ["I'm {name} in {city}", "Hi {name}. How's {city} like?"],
        ]
        expected = [
            [
                "I'm Jack", 
                "I'm George",
                "I'm Jack in Tokyo", 
                "I'm Jack in Sydney", 
                "I'm George in Tokyo",
                "I'm George in Sydney"
            ], 
            [
                "Hi Jack.", 
                "Hi George.",
                "Hi Jack. How's Tokyo like?", 
                "Hi Jack. How's Sydney like?", 
                "Hi George. How's Tokyo like?",
                "Hi George. How's Sydney like?"
            ]
        ]

        name_mpx = mpx.NameMultiplexer(names)
        city_mpx = mpx.CityMultiplexer(cities)
        srcs_result = []
        tgts_result = []
        for pair in pairs:
            src = pair[0]
            tgt = pair[1]

            srcs = [src]
            tgts = [tgt]

            srcs, tgts = name_mpx.multiplex(srcs, tgts)
            srcs, tgts = city_mpx.multiplex(srcs, tgts)

            srcs_result.extend(srcs)
            tgts_result.extend(tgts)

        actual = [srcs_result, tgts_result]
        self.assertListEqual(expected, actual)
        
    def test_speed(self):
        names = ["%d" % i for i in range(100)]
        cities = ["%d" % i for i in range(100)]
        pairs = [["{name} {city} %d" % i, "{name} {city} %d" % i] for i in range(1000)]
        name_mpx = mpx.NameMultiplexer(names)
        city_mpx = mpx.CityMultiplexer(cities)
        srcs_result = []
        tgts_result = []
        st = time.time()
        for pair in pairs:
            src = pair[0]
            tgt = pair[1]

            srcs = [src]
            tgts = [tgt]

            srcs, tgts = name_mpx.multiplex(srcs, tgts)
            srcs, tgts = city_mpx.multiplex(srcs, tgts)

            srcs_result.extend(srcs)
            tgts_result.extend(tgts)
        print ("Speed test (list version)", round(time.time() - st, 2), "sec")

    # def test_speed_set(self):
    #     """ Set version of process. Resulted in being slower than list version. Not used. """
    #     names = ["%d" % i for i in range(100)]
    #     cities = ["%d" % i for i in range(100)]
    #     pairs = [["{name} {city} %d" % i, "{name} {city} %d" % i] for i in range(1000)]
    #     name_mpx = mpx.NameMultiplexer(names)
    #     city_mpx = mpx.CityMultiplexer(cities)
    #     result = set()
    #     st = time.time()
    #     for src, tgt in pairs:
    #         pair = mpx.TextPair(src, tgt)
    #         tmp_pairs = [pair]

    #         tmp_pairs = name_mpx.multiplex_set(tmp_pairs)
    #         tmp_pairs = city_mpx.multiplex_set(tmp_pairs)

    #         result = result.union(tmp_pairs)
    #     print ("Speed test (set version)", round(time.time() - st, 2), "sec")

        
if __name__ == "__main__":
    unittest.main()
