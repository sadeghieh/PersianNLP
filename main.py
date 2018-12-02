import os, re
from normalizer import Persianizer

if __name__ == '__main__':
    SOURCE_DATA_PATH = './data/'
    OUTPUT_DATA_PATH = './out/'
    if not os.path.exists(OUTPUT_DATA_PATH):
        os.mkdir(OUTPUT_DATA_PATH)

    p = Persianizer()
    for file in os.listdir(SOURCE_DATA_PATH):
        filename = file.split('.')
        """ Only open document files, ignores OSX system dot files/folders """
        if filename[-1] in ['txt', 'xml', 'html']:
            with open(SOURCE_DATA_PATH + file, 'rt', encoding='utf-8') as f:
                raw = f.read()
            print('Processing file {} ... '.format(file), end='')
            text = p.filter_xml_tags(raw)   # Remove HTML/XML tags
            text = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', '', text)  ## Remove Timestamp
            text = re.sub(r'(["*]){2,}', '\g<1>', text)  # Remove duplicate special characters
            text = p.filter_url(text)  # Remove URLs
            text = p.trim_whitespace(text)  # Remove extra whitespace
            text = p.filter_diacritics(text)  # Remove diacritics
            text = p.filter_tatvil(text)  # Remove ARABIC/PERSIAN TATVIL (-) character
            text = p.normalize_arabic_letters(text)  # Replace Arabic 'يكة' code-points
            text = p.localize_digits(text)  # Replace Non-Persian digit code-points
            text = p.normalize_hamza(text)  # Normalize إأئؤ and ء
            text = p.localize_punc(text)  # Normalize punctuation marks, optionally wrap with space
            text = p.filter_zwnj(text, ' ')  # Remove or Replace zwnj with any other character (space in this case)
            text = p.normalize_affixation(text)  # Normalize the use of inflectional and lexical suffixes and prefixes
            print('{}Done{}'.format('\033[92m\033[1m', '\033[0m\033[0m'))

            new_filename = ''.join(filename[:-1]) + '.txt'
            with open(OUTPUT_DATA_PATH + new_filename, 'wt', encoding='utf-8') as f:
                print('Saving normalized file as {}'.format(new_filename))
                f.write(text)
