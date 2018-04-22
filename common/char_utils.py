import sys

# Unocode code page ranges. Note that they are not UTF8, nor UTF16, but code page values.
# https://ja.wikipedia.org/wiki/Unicode%E4%B8%80%E8%A6%A7_3000-3FFF
none_char_ranges = [[0x0000, 0x0020], [0x007F, 0x00A0], [0x2000, 0x200F], [0x2028, 0x202F],
    [0x2066, 0x206F], [0xFFF9, 0xFFFF]]
ascii_ranges = [[0x0021, 0x007E], [0x00A1, 0x00B8]]
ascii_symbol_ranges = [[0x0021, 0x002F], [0x003A, 0x0040],      # Note this is overlapped with 'ascii_ranges'
    [0x005B, 0x0060], [0x007B, 0x007E]]
ascii_alpabet_ranges = [[0x0041, 0x005A], [0x0061, 0x007A]]     # Note this is overlapped with 'ascii_ranges'
ascii_number_ranges = [[0x0030, 0x0039]]                        # Note this is overlapped with 'ascii_ranges'
full_symbol_ranges = [[0x3001, 0x3036], [0x3099, 0x309E], 
    [0xFF01, 0xFF0F], [0xFF1A, 0xFF20], [0xFF3B, 0xFF40], [0xFF5B, 0xFF65]]
full_number_ranges = [[0xFF10, 0xFF19]]
full_alphabet_ranges = [[0xFF21, 0xFF3A], [0xFF41, 0xFF5A]]
hiragana_ranges = [[0x3041, 0x3094], [0x3099, 0x309E]]
katakana_ranges = [[0x30A1, 0x30F6], [0x30FB, 0x30FE]]
katakana_half_ranges = [[0xFF66, 0xFF9D]]


if (sys.version_info > (3, 0)):
     # Python 3 code in this block
    def _get_code_ranges(code_ranges, chars):
        for rng in code_ranges:
            for code in range(rng[0], rng[1]):
                chars.append(chr(code))
else:
     # Python 2 code in this block
    def _get_code_ranges(code_ranges, chars):
        for rng in code_ranges:
            for code in range(rng[0], rng[1]):
                chars.append(unichr(code))

def _is_within_ranges(code_ranges, code):
    for rng in code_ranges:
        if rng[0] <= code <= rng[1]:
            return True
    return False

def get_charactors_ascii():
    """ Return ASCII characters in list. """
    result = []
    _get_code_ranges(ascii_ranges, result)
    return result

def get_charactors_ascii_symbol():
    """ Return ASCII symbol (non alphabet) characters in list. """
    result = []
    _get_code_ranges(ascii_symbol_ranges, result)
    return result

def get_charactors_ascii_alphabet():
    """ Return ASCII alphabet characters in list. """
    result = []
    _get_code_ranges(ascii_alpabet_ranges, result)
    return result

def get_charactors_ascii_number():
    """ Return ASCII number 0 - 9 characters in list. """
    result = []
    _get_code_ranges(ascii_number_ranges, result)
    return result

def get_charactors_full_symbol():
    """ Return full-width symbol characters in list. """
    result = []
    _get_code_ranges(full_symbol_ranges, result)
    return result

def get_charactors_full_number():
    """ Return full-width number characters in list. """
    result = []
    _get_code_ranges(full_number_ranges, result)
    return result

def get_charactors_full_alphabet():
    """ Return full-width alphabet characters in list. """
    result = []
    _get_code_ranges(full_alphabet_ranges, result)
    return result

def get_charactors_hiragana():
    """ Return hiragana characters in list. """
    result = []
    _get_code_ranges(hiragana_ranges, result)
    return result

def get_charactors_katakana():
    """ Return katakana characters in list. """
    result = []
    _get_code_ranges(katakana_ranges, result)
    return result

def get_charactors_katakana_half():
    """ Return half-width katakana characters in list. """
    result = []
    _get_code_ranges(katakana_half_ranges, result)
    return result

def is_charactor_ascii(char):
    """ Return if the character is ASCII code. """
    return _is_within_ranges(ascii_ranges, ord(char))

def is_charactor_ascii_symbol(char):
    """ Return if the character is ASCII symbol (non alphabet) character. """
    return _is_within_ranges(ascii_symbol_ranges, ord(char))

def is_charactor_ascii_alphabet(char):
    """ Return if the character is ASCII alphabet character. """
    return _is_within_ranges(ascii_alpabet_ranges, ord(char))

def is_charactor_ascii_number(char):
    """ Return if the character is ASCII number 0 - 9 character. """
    return _is_within_ranges(ascii_number_ranges, ord(char))

def is_charactor_full_symbol(char):
    """ Return if the character is full-width symbol code. """
    return _is_within_ranges(full_symbol_ranges, ord(char))

def is_charactor_full_number(char):
    """ Return if the character is full-width number code. """
    return _is_within_ranges(full_number_ranges, ord(char))

def is_charactor_full_alphabet(char):
    """ Return if the character is full-width alphabet code. """
    return _is_within_ranges(full_alphabet_ranges, ord(char))

def is_charactor_hiragana(char):
    """ Return if the character is hiragana code. """
    return _is_within_ranges(hiragana_ranges, ord(char))

def is_charactor_katakana(char):
    """ Return if the character is katakana code. """
    return _is_within_ranges(katakana_ranges, ord(char))

def is_charactor_katakana_half(char):
    """ Return if the character is half-width katakana code. """
    return _is_within_ranges(katakana_half_ranges, ord(char))

def is_none_char(char):
    """ Return if the character is none-character (control code). """
    return _is_within_ranges(none_char_ranges, ord(char))

