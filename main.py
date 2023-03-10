import requests
from bs4 import BeautifulSoup
import pandas as pd
url = 'https://doska.ykt.ru/nedvizhimost/kvartiry/prodau'
params = {'page': 1}
pages = 1
n = 1
df=pd.DataFrame(columns=['Room', 'Price', 'Date'])
while params['page'] <= pages:
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='d-post_body')

    for n, i in enumerate(items, start=n):
        itemDesc = i.find('div', class_='d-post_desc').text.strip().split(" комн.")
        itemRoom = i.find('div', class_='d-post_desc').text.strip().split(" комн.")[0]
        itemPrice = i.find('div', class_='d-post_price').text.strip().split("р")[0]
        itemDate = i.find('span', class_='d-post_date').text.strip()
        df = pd.concat([pd.DataFrame([[itemRoom, itemPrice, itemDate]], columns=df.columns), df], ignore_index=True)

    #last_page_num = int(soup.find_all('li')[-2].text)
    last_page_num = int(1)
    pages = last_page_num if pages < last_page_num else pages
    params['page'] += 1
df['Price']=df['Price'].str.replace('\xa0', '').astype('int')
#df['Room']=df['Room'].astype('int')
print(df)



