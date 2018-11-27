from normalizer import Normalizer

n = Normalizer()

text_1 = 'مُن در ایآٍن مْتن علائمِ اضافه     را حُذف می‌‌‌‌‌‌‌‌‌‌‌کَنم.'
text_2 = 'چرا نباید در این متن چیزی را که فارسی نیست, فارسی نکرد?'
text_3 = 'اعداد ٣ این متن ٠ فارسی ٥ نبود 4 ولی حالا8 هست.'

print(n.filter_diacritics(text_1))
