import requests
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('display.max_columns', 10)
url = 'https://doska.ykt.ru/nedvizhimost/kvartiry/prodau'
params = {'page': 1}
pages = 1
n = 1
df=pd.DataFrame(columns=['Desc','Price', 'Date'])
while params['page'] <= pages:
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='d-post_body')

    for n, i in enumerate(items, start=n):
        itemDesc = i.find('div', class_='d-post_desc').text.strip()
        itemPrice = i.find('div', class_='d-post_price').text.strip().split("р")[0]
        itemDate = i.find('span', class_='d-post_date').text.strip()
        df = pd.concat([pd.DataFrame([[itemDesc, itemPrice, itemDate]], columns=df.columns), df], ignore_index=True)

    #last_page_num = int(soup.find_all('li')[-2].text)
    last_page_num = int(1)

    pages = last_page_num if pages < last_page_num else pages
    params['page'] += 1
df['Price']=df['Price'].str.replace('\xa0', '').astype('int')
df['Rooms'] = df['Desc'].apply(lambda x: int(x.split(" комн.")[0][-2:]) if 'комн.' in x else (0 if 'Студия' in x else None))
df['Area'] = df['Desc'].apply(lambda x: int(x.split(" м²")[0][-3:]) if 'м²' in x else None)
df['Price_per_area']=(df['Price']/df['Area']/1000).round(3)

flat_type=['112 серия',
            'Блочный',
            'Дерев. б/у',
            'Дерев. ч/б',
            'Другое',
            'Инд. планировка',
            'Каркасно-щитовой',
            'КПД',
            'Малосемейка',
            'Монолитно-каркасный',
            'Сталинка',
            'Хрущевка']

#df['Type'] = df['Desc'].apply(lambda x: contains_word(flat_type, x))


df['Type'] = df['Desc'].str.split(",")
#df['Type2'] = df['Type'].apply(lambda x: x if x in flat_type else None)
#df['Type2']=df['Type'].find(flat_type)
print(df['Type'].find(flat_type))



#print(df.describe())
#print(df.info())