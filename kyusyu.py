import requests
from bs4 import BeautifulSoup
import csv


# 対象のURLを指定
url_page = [
            'https://www.88onsen.com/spot',
            "https://www.88onsen.com/spot/index/mode/paging/page/2/t//category/",
            "https://www.88onsen.com/spot/index/mode/paging/page/3/t//category/",
            "https://www.88onsen.com/spot/index/mode/paging/page/4/t//category/",
            "https://www.88onsen.com/spot/index/mode/paging/page/5/t//category/",
            "https://www.88onsen.com/spot/index/mode/paging/page/6/t//category/",
            "https://www.88onsen.com/spot/index/mode/paging/page/7/t//category/",
            "https://www.88onsen.com/spot/index/mode/paging/page/8/t//category/",
            "https://www.88onsen.com/spot/index/mode/paging/page/9/t//category/",
            "https://www.88onsen.com/spot/index/mode/paging/page/10/t//category/",
            "https://www.88onsen.com/spot/index/mode/paging/page/11/t//category/",
            "https://www.88onsen.com/spot/index/mode/paging/page/12/t//category/",
            "https://www.88onsen.com/spot/index/mode/paging/page/13/t//category/",
            "https://www.88onsen.com/spot/index/mode/paging/page/14/t//category/",]
count=0

<<<<<<< HEAD
csv_file = '九州温泉道.csv'
items=['住所', '電話番号', '営業時間', '料金', '泉質', '泉人優待', 'アクセス', '施設サイト']
=======
csv_file = '九州温泉道2.csv'
items=['Google map','住所', '電話番号', '営業時間', '料金', '泉質', '泉人優待', 'アクセス', '施設サイト']
>>>>>>> 4ade272 (Temporary commit for branch switch)
with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(["番号",'施設名']+items)  # csvのヘッダーを書き込み

for url in url_page:
    # ページの内容を取得
    response = requests.get(url)
    html_content = response.content

    # BeautifulSoupを使ってHTMLを解析
    soup = BeautifulSoup(html_content, 'html.parser')

    # divタグのsectionクラスの値を取得
    sections = soup.find_all('div', class_='section')
    for section in sections:
        a_tags = section.find_all('a')

        # aタグの値と番号を重複なく取得
        links=set([("https://www.88onsen.com"+a.get('href'),a.get('href').split("/")[-1],a.get_text(strip=True)) for a in a_tags if "/spot/detail/" in a.get('href') and a.get_text(strip=True)!=""])
        
        for link in links:
            print(link)
    
    # 詳細情報をcsvに書き出し
    with open(csv_file, mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        for onsen_url,number,name in links:
            print(onsen_url)
            info={item: "" for item in items}
            # ページの内容を取得
            response = requests.get(onsen_url)
            html_content = response.content

            # BeautifulSoupを使ってHTMLを解析
            soup = BeautifulSoup(html_content, 'html.parser')

            # テーブルを取得
            table = soup.find('div',id="spot_detail")

            # テーブルの行データを取得
<<<<<<< HEAD
            row = []
            for dt,dd in zip(table.find_all('dt'),table.find_all('dd')):
                info[dt.get_text(strip=True)]=dd.get_text(strip=True)
=======
            for dt,dd in zip(table.find_all('dt'),table.find_all('dd')):
                info[dt.get_text(strip=True)]=dd.get_text(strip=True)
            info["Google map"]="https://www.google.com/maps/search/?api=1&query="+info["住所"]
>>>>>>> 4ade272 (Temporary commit for branch switch)
            row=list(info.values())
            
            writer.writerow([number,name]+row+[onsen_url])


