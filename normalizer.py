import re


class Normalizer:

    supported_languages = ['fa', 'en']

    def __init__(self, language: str = 'fa'):
        if self.is_supported(language):
            self.locale = language
        else:
            # revert to the default locale
            self.locale = 'fa'

        punct_range = self.get_unicode_range('punctuation')
        alphabet_range = self.get_unicode_range('alphabet')
        numeral_range = self.get_unicode_range('numerals')
        self.punctuation = punct_range[self.locale]
        self.alphabet = alphabet_range[self.locale]
        self.digits = numeral_range[self.locale]

    @staticmethod
    def get_unicode_range(boundary: str = None) -> dict:
        arabic_w = u'\u0621-\u063A\u0641-\u064A'  # ARABIC ALPHABET
        arabic_w += u'\u067E\u0686\u0698\u06A9\u06AF\u06CC\u0654'  # EXTENDED ARABIC LETTERS

        # preserve order where mapping across languages may be applicable, i.e. numbers or punctuation marks
        ranges = \
            {'punctuation': {'fa': r'؟!٪)(،؛.', 'en': r'?!%(),;.'},
             'numerals':    {'fa': '۰۱۲۳۴۵۶۷۸۹', 'en': '0123456789', 'ar': '٠١٢٣٤٥٦٧٨٩'},
             'alphabet':    {'fa': arabic_w, 'en': r'[a-zA-Z]'},
             'diacritics':  {'fa': u'\u0610-\u061A\u064B-\u065F'}}

        return ranges[boundary] if boundary else ranges

    def get_punctuation(self) -> str:
        return self.punctuation

    def get_numerals(self) -> str:
        return self.digits

    def get_alphabet(self) -> str:
        return self.alphabet

    def is_supported(self, lang: str) -> bool:
        return True if lang in self.supported_languages else False

    def localize_punc(self, text: str, sep: str = ' ') -> str:
        out_charset = self.get_punctuation()
        punct_marks = self.get_unicode_range('punctuation')

        # a list of punctuation marks not used by the current locale
        in_charsets = [punct_marks[lang] for lang in punct_marks if lang != self.locale]

        for i in range(len(in_charsets)):
            tbl = str.maketrans(in_charsets[i], out_charset)
            text = text.translate(tbl)

        if sep:
            text = re.sub('(?<!\s)([' + out_charset + ']{1,3})', sep + '\g<0>', text)
            text = re.sub('([' + out_charset + ']){1,3}(?!\s)', '\g<0>' + sep, text)

        return text

    def localize_digits(self, text: str) -> str:
        out_charset = self.get_numerals()
        numerals = self.get_unicode_range('numerals')

        # a list of digit characters not used by the current locale
        in_charsets = [numerals[lang] for lang in numerals if lang != self.locale]

        for i in range(len(in_charsets)):
            tbl = str.maketrans(in_charsets[i], out_charset)
            text = text.translate(tbl)

        return text

    def filter_zwnj(self, text: str, replace: str = '') -> str:
        # TODO: Move to a language specific instance of the Normalizer Object
        return text.replace('\u200c', replace)

    def filter_diacritics(self, text: str) -> str:
        diacritics = self.get_unicode_range('diacritics')
        return re.sub('[{}]'.format(diacritics[self.locale]), '', text)

    def filter_foreign(text: str) -> str:
        # TODO: use class internal methods and attributes
        arabic = '\s'
        arabic += '\u060C\u061B\u061F\u06D4'  # ARABIC COMMA SEMICOLON QUESTION FULLSTOP
        arabic += '\u064B-\u0652'             # ARABIC DIACRITICS
        arabic += '\u0621-\u063A\u0641-\u064A'   # ARABIC ALPHABET
        arabic += '\u067E\u0686\u0698\u06A9\u06AF\u06CC\u0654'
        arabic += '\u0660-\u0669\u06F0-\u06F9'   # ARABIC DIGITS
        arabic += '\u0640'                    # ARABIC TATWEEL

        non_arabic = '[^' + arabic + ']'
        return re.sub(non_arabic, '', text)

    def trim_whitespace(self, text: str) -> str:
        text = re.sub(' {2,}', ' ', text)
        text = re.sub('\n{2,}', '\n', text)
        text = re.sub('\u200C{2,}', '\u200C', text)

        return text

    def filter_tatvil(text: str) -> str:
        # TODO: Move to a language specific instance of the Normalizer Object
        tatweel = '\u0640'
        return text.replace(tatweel, '')

    def filter_yah_ezafe(text: str) -> str:
        # TODO: Move to a language specific instance of the Normalizer Object
        pass

    def filter_final_hamza(text: str) -> str:
        # TODO: Move to a language specific instance of the Normalizer Object
        pass

    def filter_nonsense(text: str, preserve: str = '') -> str:
        pass
