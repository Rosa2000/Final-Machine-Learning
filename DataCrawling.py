from bs4 import BeautifulSoup
import pandas
import requests
import csv
import colorama

#lấy link cho các topic
base_url = 'https://vnexpress.net'
topic_list = ['Thời sự', 'Thế giới', 'Kinh doanh', 'Pháp luật', 'Giáo dục', 'Giải trí'] #list chứa topic
topic_url = [] #list chứa các url

response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

topic_url_temp = soup.find('nav', class_ = 'main-nav').find_all('a')

#lấy url bảng tin của từng topic
for topics in topic_url_temp:
    topic = topics.attrs["href"] #lấy href

    if topics.get('title') in topic_list:
        topic_url_temp = base_url + topic #trang 1 của từng topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp + '-p2' #trang 2 của topic
        topic_url.append(topic_url_temp)

with open('data/raw_data.csv', 'w', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Topic', 'Title', 'Description'])

#lấy dữ liệu từng topic
for url in topic_url:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # tìm dữ liệu
    news_feed = soup.findAll('p', class_='description')

    # xuất csv
    with open('data/raw_data.csv', 'a', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        for news in news_feed:
            # tách dữ liệu và ghi vào file
            topic = soup.find('h1').find('a').get('title')
            title = news.find('a').get('title')
            des = news.find('a')
            #đoạn này là để bỏ location cho những bài báo có dính location
            #nếu không bỏ thì dữ liệu xuất ra bị dính lại
            if des.find('span', class_ = 'location-stamp') is not None:
                new_tag = soup.new_tag('b')
                new_tag.string = ''
                replaced = des.span.replace_with(new_tag)
                des = des.text
            else:
                des = des.text
            des = des.strip('\n ')

            #viết thêm vào file data
            writer.writerow([topic, title, des])
