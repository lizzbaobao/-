import time
import random
import mysql.connector
from mysql.connector import Error
import requests
from bs4 import BeautifulSoup


headers = {'user-agent':'my-app/0.0.1'}
page = 0


while True :

    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='127.0.0.1',          # 主機名稱
            database='8591', # 資料庫名稱
            user='root',        # 帳號
            password='')  # 密碼

        if connection.is_connected():
            
            # 顯示資料庫版本    
            db_Info = connection.get_server_info()
            print("資料庫版本：", db_Info)

            # 顯示目前使用的資料庫
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("目前使用的資料庫：", record)

            while True :
                urlsearch = "https://www.8591.com.tw/mallList-list.html?&searchGame=859&searchServer=984&group=1&priceSort=2&searchType=1&searchKey=%E6%99%BA&firstRow="+str(page)+"&totalRows=380#menu',headers=headers"

                r = requests.get(urlsearch,headers=headers)
                response = r.text
                soup = BeautifulSoup(response)  
                totalpage = soup.find(id='Col22Right').find("span",class_='R').text
                # print(totalpage)
                for link in soup.find_all('a',class_="detail_link"):
                    urlid = link.get('href').split('=') #getID
                    goods = link.find('span').text
                    # print(link.find('span').text)
                    #print(s1[1])
                    # print("https://www.8591.com.tw/mallList-wareDetail.html?id="+urlid[1])
                    cursor.execute("SELECT * FROM `baowu` WHERE `ID` ="+urlid[1]+";")
                    count = cursor.fetchall()
                    # print("///////")
                    # print(len(count))
                    # print("///////")
                    if len(count) < 1 :
                        # print(urlid)
                        sql = "INSERT INTO baowu (name, ID) VALUES (%s, %s);"
                        new_data = (goods,int(urlid[1]))
                        cursor = connection.cursor()
                        cursor.execute(sql, new_data)
                        connection.commit()
                        #//////推播///////
                        r = requests.post(
                            f"https://api.telegram.org/bot1737087528:AAGBdJDsctayDOArDfIJVCJDgzB8RLv57y0/sendMessage",
                            json={"chat_id":"698466146","text":goods+"\n"+"https://www.8591.com.tw/mallList-wareDetail.html?id="+urlid[1],},
                        )
                        #//////////////////////////

                
                time.sleep(random.uniform(5,15))
                print("time OK")
                page = page + 21
                if page > int(totalpage):
                    break



                


    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
    
    time.sleep(random.uniform(6800,7500))