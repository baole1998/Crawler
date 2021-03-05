from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import timedelta, date
import pymysql
import json

conn = pymysql.connect(host='127.0.0.1',
                       port=3306,
                       user='root',
                       database = 'stockData',
                       password='123123as',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

cur = conn.cursor()
try:
    cur.execute("Create database if not exists stockData default character set utf8mb4;")
except Exception as x:
    print(x, flush=True)
    conn.rollback()

try:
    tablename = 'fullStockDataPerYear'
    quer = f'''
    create table if not exists {tablename} (
        ID int(30) auto_increment,
        Symbol varchar(10) not null,
        TradingDate varchar(10) not null,
        OpenPrice int(10) not null,
        HighPrice int(10) not null,
        LowPrice int(10) not null,
        ClosePrice int(10) not null,
        TotalQtty int(10) not null,
        TotalValue double not null,
        PTQtty int(10) not null,
        AVGPrice int(10) not null,
        AdjClosePrice int(10) not null,
        AdjAVGPrice int(10) not null,
        AdjHighPrice int(10) not null,
        AdjLowPrice int(10) not null,
        AdjOpenPrice int(10) not null,
        primary key (ID)
    );
    '''
    cur.execute(quer)
    conn.commit()
    print("Kết nối thành công Database!!!")
except Exception as e:
    print(e, flush=True)
    conn.rollback()

def checking_if_data_existed(data,symbol):
    data_checking = True
    try:
        with conn.cursor() as cursor:
            sql = f''' SELECT * FROM {tablename} where TradingDate='{data}' and Symbol='{symbol}' '''
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) > 0:
                data_checking = False
        return data_checking
    except Exception as e:
        print(e, flush=True)


def crawler(url,json):
    chrome_options = Options()
    chromedriver = '/Users/lebao/PycharmProjects/CrawlNews/chromeDriver/chromedriver'
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chromedriver)
    driver.get(url)
    elem = driver.find_element_by_xpath('/html/body/pre')
    data = elem.text
    json = json.loads(data)
    x = int(len(json['data']))
    i = 0

    while True:
        for i in range(0,x):
            Symbol = (json['data'][i]['Symbol'])
            TradingDate = (json['data'][i]['TradingDate'])
            OpenPrice = (json['data'][i]['OpenPrice'])
            HighPrice = (json['data'][i]['HighPrice'])
            LowPrice = (json['data'][i]['LowPrice'])
            ClosePrice = (json['data'][i]['ClosePrice'])
            TotalQtty = (json['data'][i]['TotalQtty'])
            TotalValue = (json['data'][i]['TotalValue'])
            PTQtty = (json['data'][i]['PTQtty'])
            AVGPrice = (json['data'][i]['AVGPrice'])
            AdjClosePrice = (json['data'][i]['AdjClosePrice'])
            AdjAVGPrice = (json['data'][i]['AdjAVGPrice'])
            AdjHighPrice = (json['data'][i]['AdjHighPrice'])
            AdjLowPrice = (json['data'][i]['AdjLowPrice'])
            AdjOpenPrice = (json['data'][i]['AdjOpenPrice'])

            if checking_if_data_existed(TradingDate,Symbol) is True:

                query = f'''
                    Insert into {tablename}(
                    Symbol,
                    TradingDate,
                    OpenPrice,
                    HighPrice,
                    LowPrice,
                    ClosePrice,
                    TotalQtty,
                    TotalValue,
                    PTQtty,
                    AVGPrice,
                    AdjClosePrice,
                    AdjAVGPrice,
                    AdjHighPrice,
                    AdjLowPrice,
                    AdjOpenPrice
                    )
                    value (
                    '{Symbol}',
                    '{TradingDate}',
                    '{OpenPrice}',
                    '{HighPrice}',
                    '{LowPrice}',
                    '{ClosePrice}',
                    '{TotalQtty}',
                    '{TotalValue}',
                    '{PTQtty}',
                    '{AVGPrice}',
                    '{AdjClosePrice}',
                    '{AdjAVGPrice}',
                    '{AdjHighPrice}',
                    '{AdjLowPrice}',
                    '{AdjOpenPrice}'
                    );
                '''
                cur.execute(query)
                conn.commit()
                print('Insert Success!!!')
            else:
                print("Data Existed!!!")
                continue
        if i <= x:
            break
    driver.close()

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)



start_date = date(2000, 7, 28)
end_date = date(2021, 3, 4)
for single_date in daterange(start_date, end_date):
    url = 'http://10.32.79.12/stockHistsByDate/'+ str(single_date.strftime("%d-%m-%Y"))+'/S'
    crawler(url,json)


