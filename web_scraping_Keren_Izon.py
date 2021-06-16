# -*- coding: utf-8 -*-
# the script assumes that the input sites are written in Hebrew language bacause of encoding issue.
# when printing to screen run the command: chcp 65001 ,and then run the script.

import requests
# required to install the following: pip install BeautifulSoup4
from bs4 import BeautifulSoup
from collections import Counter
 

def crawl(url):
 
    r = requests.get(url).content
    soup = BeautifulSoup(r.decode('utf-8','ignore'), 'html.parser')
    
    content = ''
    for tag in soup.find_all(['p','h1','h2','h3','h4','h5','h6','form','button','label','select','option','a','li','th','tr','td']):
        content += tag.text[::-1]  # the minus is for reversing the text because it's Hebrew (from right to left)

    # print(content)
    return content


def processing_data(data):
    num_of_common_words = 30  # it can be any number of words as wanted
    words_list = []
    result = []
    num_words = {}
    symbols = "^()&*_-+=#$%{[}]|\;:\"<>?/.,!@ "
 
    words = data.lower().split() # convert the data to lowercase (to compare them efficiently) and split to words

    for word in words:
        words_list.append(word) # collect the words into words_list array

    for word in words_list:
        for i in range(len(symbols)):
            word = word.replace(symbols[i], '') # replace the symbol with empty string
        if len(word) > 0:   # if the result of the replacing is greater than zero - means it's a word
            result.append(word)
    
    for word in result:
        if word in num_words: # for each word in 'result': if it exists in 'num_words' - update and add 1, if it doesn't exist - start with 1
            num_words[word] += 1
        else:
            num_words[word] = 1
 
    count = Counter(num_words)
    frequent_words = count.most_common(num_of_common_words) # sorting 'num_words' according the most frequent words
    print(frequent_words)
 
 

def crawl_urls(urls_list):
    content_txt = ''
    for url in urls_list:
        content_txt += crawl(url)
    processing_data(content_txt)


crawl_urls(["http://he.wikipedia.org","http://ynet.co.il"])