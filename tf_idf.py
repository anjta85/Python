import urllib.request
import re
import math
from html.parser import HTMLParser
from collections import Counter

class HTMLDataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._words = []
        self._ignore = False

    def handle_starttag(self, tag, attrs):
        self._ignore = tag in ["script", "link"]

    def handle_data(self, data):
        # этот метод вызывается каждый раз,
        # когда парсер находит какие-то данные в html-коде
        if not self._ignore:
            self._words.extend(
                map(lambda x: x.lower(),
                    re.findall("[\w]+", data))
            )

    def handle_endtag(self, tag):
        self._ignore = False

    def get_words(self):
        return self._words

def get_page_html(url):
    # получаем страницу и пытаемся её декодировать
    return urllib.request.urlopen(url).read().decode("iso-8859-1")

def get_all_urls(file_with_urls):
    # забираем все url'ы из файла file_with_urls
    text = file_with_urls.read()
    links = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text)
    return links

def get_all_words(html):
    # получаем все слова из html
    parser = HTMLDataParser()
    parser.feed(html)
    return parser.get_words()

def tf(word, document):
    # считаем TF для word в документе document
    word_cnt = 0
    for document_word in document:
        word_cnt += 1
    return word_cnt / len(document)

def idf(word, documents_count, all_words):
    # считаем IDF (просто по определению)
    return math.log(documents_count / all_words[word])

def tf_idf(word, document, documents_count, all_words):
    TF = tf(word, document)
    IDF = idf(word, documents_count, all_words)
    return TF * IDF

def tf_idf_all_words(document, documents_count, all_words):
    # считаем TF-IDF для каждого слова в документе
    rates = {}
    for word in document:
        rates[word] = tf_idf(word, document, documents_count, all_words)
    return rates

def main():
    file_with_urls = open("urls.txt", encoding="utf-8")
    # all_words хранит для каждого слова количество документов,
    # в которых оно встречается
    all_words = Counter()
    # хранит для каждого документа множество уникальных слов
    documents = []
    for url in get_all_urls(file_with_urls):
        html = get_page_html(url)
        words = set(get_all_words(html))
        documents.append(words)
        all_words.update(words)
    print(tf_idf_all_words(documents[0], len(documents), all_words))

if __name__ == "__main__":
    main()
