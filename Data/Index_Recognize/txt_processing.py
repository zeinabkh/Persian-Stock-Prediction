import regex
import re
from cleantext import clean
from hazm import Normalizer
class Preprocess:

    @staticmethod
    def find_urls(text):
        txt = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',"اینجا کلیک کنید.", text)
        return txt


    def cleaning(self, text):
        text = text.strip()
        text = Normalizer().normalize(text)
        text = re.sub("[٠۰۲۱١٢۳٣۴٤۵٥٦۶۷٧٨٩۹۸]+", " عدد ", text)
        text = re.sub("[0123456789]+", " عدد ", text)
        text = text.replace("?", " ؟ ").replace(".", " . ").replace("*"," ")
        punctuation_pattern = re.compile(r"@|\*|\$|\%|\&|\)|\(|\}|\{|\[|\]|/|\(|/-|\+|(\.)|_|[a-zA-Z]|:|;|=|؛|'|,")
        text = text.replace("،", " ، ")
        text = punctuation_pattern.sub(r' ', text)
        text = text.replace("،", " ، ")
        text = re.sub(r"(؟)(؟)+", " ؟ ", re.sub(r'(!)(!)+', " ! ", text))
        # regular cleaning
        text = clean(text,
                     fix_unicode=True,
                     to_ascii=False,
                     lower=True,
                     no_line_breaks=True,
                     no_urls=True,
                     no_emails=True,
                     no_phone_numbers=True,
                     no_numbers=True,
                     no_digits=True,
                     no_currency_symbols=True,
                     no_punct=False,
                     replace_with_url=" ",
                     replace_with_email=" ",
                     replace_with_phone_number=" ",
                     replace_with_number=" عدد ",
                     replace_with_digit=" ",
                     replace_with_currency_symbol=" ",
                     )

        # removing wierd patterns

        # removing extra spaces, hashtags
        text = re.sub("\s+", " ", self.remove_emoji(text))
        text = re.sub("\s+", " ", text)
        # print(text,"@@@@@")
        return text

    @staticmethod
    def remove_emoji(string):
        emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)

        return re.sub(r'( )( )+', r' ', emoji_pattern.sub(r'', string).replace("\n", " "))


# text = " فملی، غگل، دانا، وطوبی، فرابورس، وتجارت، برکت، تلیسه، غنوش،"
# print(re.sub("\s+", " ", text.replace("،", " ،    ")))
