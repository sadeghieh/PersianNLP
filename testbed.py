from normalizer import Persianizer

p = Persianizer()

text_1 = 'مُن در ایآٍن مْتن علائمِ اضافه     را حُذف می‌‌‌‌‌‌‌‌‌‌‌کَنم.'
text_2 = 'چرا نباید در این متن چیزی را که فارسی نیست, فارسی نکرد?'
text_3 = 'اعداد ٣ این متن ٠ فارسی ٥ نبود 4 ولی حالا8 هست.'
text_4 = 'منشاء آشنآ فن‌آوری فنآوری شیء'

print(p.filter_final_hamza(text_4))
