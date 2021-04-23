from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import underthesea
import numpy
import pandas
import csv
import seaborn
import re
import string
import warnings
warnings.filterwarnings('ignore')

#đọc file data
data = pandas.read_csv('data/raw_data.csv')
stopwords = pandas.read_csv('data/stopwords.csv',header=None)

#xử lý danh sách stopword
stop_list = []
for i in stopwords.index:
    stop_list.append(stopwords.iloc[i,0])

#lowercase cho tất cả dữ liệu
data = data.applymap(lambda s:s.lower())

#loại bỏ dấu
data['Title'] = data['Title'].str.replace('[^\w\s]', '')
data['Description'] = data['Description'].str.replace('[^\w\s]', '')

with open('data/preprocessing.csv', 'w', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Topic', 'Content'])

#xét từng dòng
for i in data.index:
    #tokenize
    data_token_topic = underthesea.word_tokenize(data['Topic'][i])
    data_token_title = underthesea.word_tokenize(data['Title'][i])
    data_token_des = underthesea.word_tokenize(data['Description'][i])

    #bỏ stopword cho topic (thực ra cũng không cần thiết lắm)
    for word in data_token_topic:
        if word in stop_list:
            data_token_topic.remove(word)
    #bỏ stopword cho title
    for word in data_token_title:
        if word in stop_list:
            data_token_title.remove(word)
    #bỏ stopword cho description
    for word in data_token_des:
        if word in stop_list:
            data_token_des.remove(word)

    with open('data/preprocessing.csv', 'a', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([data_token_topic, data_token_title + data_token_des])
