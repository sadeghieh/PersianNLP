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

        # preserve order where mapping across languages may be applicable, e.g. numbers or punctuation marks
        ranges = \
            {'punctuation': {'fa': r'؟!٪)(،؛.', 'en': r'?!%(),;.'},
             'numerals':    {'fa': '۰۱۲۳۴۵۶۷۸۹', 'en': '0123456789', 'ar': '٠١٢٣٤٥٦٧٨٩'},
             'alphabet':    {'fa': arabic_w, 'en': r'[a-zA-Z]'},
             'diacritics':  {'fa': u'\u0610-\u061A\u064B-\u065F'}}

        return ranges[boundary] if boundary else ranges

    @staticmethod
    def get_affixes(affix_type: str = 'all', lang: str = 'fa') -> dict:
        affixes = \
            {'post_INFL': {'fa': ['های*', 'ها ای', 'ای+', 'ی+', 'مان', 'تان', 'شان',
                                  'هایم', 'هایت', 'هایش', 'هایمان', 'هایتان', 'هایشان', 'ام', 'ات', 'اش']},
             'post_LEX': {'fa': ['ای', 'اید', 'ام', 'ایم', 'اند', 'جاتی?', 'آوری?', 'نشینی?', 'کننده', 'کنندگی',
                                 'پاشی?', 'پوشی?', 'پوشانی?', 'شناسی?', 'شناسانی?', 'پذیری?', 'پذیرانی?',
                                 'شکنی?', 'شکنانی?', 'فشانی?', 'سازی?', 'آلودی?', 'آمیزی?', 'زدای*',
                                 'انگیزی?', 'خیزی?', 'سوزی?', 'پراکنی', 'خوری', 'افکنی?', 'دانی?',
                                 'پروری?', 'پریشی?', 'نویسی?', 'وار', 'واره', 'کارانی?', 'پژوهی?', 'سنجی?',
                                 'کنان', 'پردازی?', 'رسانی?', 'یابی?', 'پیما', 'گری?', 'گیری?', 'مندی?', 'ساعته',
                                 'ور', 'اندازی?']},
             'pre_INFL': {'fa': ['ن?می']},
             'pre_LEX': {'fa': ['نا', 'بی', 'فرا', 'سوء', 'ابر']}}

        out = affixes if affix_type == 'all' else affixes[affix_type]
        return out[lang] if lang in out else {}

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


class Persianizer(Normalizer):

    def filter_zwnj(self, text: str, replace: str = '') -> str:
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
        tatweel = '\u0640'
        return text.replace(tatweel, '')

    def filter_yah_ezafe(text: str) -> str:
        pass

    def normalize_hamza(text: str) -> str:
        text = re.sub(r'(?<=['+'آاوی'+'])'+'ء'+'(?=[\s\r\n])', '', text)
        text = re.sub(r'(?<![\r\n\s\u200C])' + 'آ', 'ا', text)

        mapping = str.maketrans('أئؤ', 'ایو')
        return text.translate(mapping)

    def normalize_arabic_letters(text: str) -> str:
        mapping = str.maketrans('يك', 'یک')
        return text.translate(mapping)

    def filter_nonsense(text: str, preserve: str = '') -> str:
        pass
