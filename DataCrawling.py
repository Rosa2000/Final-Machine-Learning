from bs4 import BeautifulSoup
import pandas
import requests
import csv
import colorama

# lấy link cho các topic
base_url = 'https://vnexpress.net'
topic_list = ['Thời sự', 'Thế giới', 'Kinh doanh', 'Pháp luật', 'Giáo dục', 'Giải trí']  # list chứa topic
topic_url = []  # list chứa các url

response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

topic_url_temp = soup.find('nav', class_='main-nav').find_all('a')

# lấy url bảng tin của từng topic
for topics in topic_url_temp:
    topic = topics.attrs["href"]  # lấy href

    if topics.get('title') in topic_list:
        topic_url_temp = base_url + topic  # trang 1 của từng topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp + '-p2'  # trang 2 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p2', '-p3')  # trang 3 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p3', '-p4')  # trang 4 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p4', '-p5')  # trang 5 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p5', '-p6')  # trang 6 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p6', '-p7')  # trang 7 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p7', '-p8')  # trang 8 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p8', '-p9')  # trang 9 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p9', '-p10')  # trang 10 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p10', '-p11')  # trang 11 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p11', '-p12')  # trang 12 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p12', '-p13')  # trang 13 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p13', '-p14')  # trang 14 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p14', '-p15')  # trang 15 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p15', '-p16')  # trang 16 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p16', '-p17')  # trang 17 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p17', '-p18')  # trang 18 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p18', '-p19')  # trang 19 của topic
        topic_url.append(topic_url_temp)
        topic_url_temp = topic_url_temp.replace('-p19', '-p20')  # trang 20 của topic
        topic_url.append(topic_url_temp)

with open('data/raw_data.csv', 'w', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Topic', 'Title', 'Description'])

# lấy dữ liệu từng topic
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
            # đoạn này là để bỏ location cho những bài báo có dính location
            # nếu không bỏ thì dữ liệu xuất ra bị dính lại
            if des.find('span', class_='location-stamp') is not None:
                new_tag = soup.new_tag('b')
                new_tag.string = ''
                replaced = des.span.replace_with(new_tag)
                des = des.text
            else:
                des = des.text
            des = des.strip('\n ')

            # viết thêm vào file data
            writer.writerow([topic, title, des])
