# coding:utf-8
import re
import pymysql
import requests
import datetime
from bs4 import BeautifulSoup
#计时跟踪
starttime = datetime.datetime.now()

#使用pymysql进行数据库连接
conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='hdu220313', db='web', charset='utf8')
cur = conn.cursor()

#新闻存储函数
def storeNews(dbPubtime,dbLink,dbTitle,dbContent):
    cur.execute("SELECT id FROM cmdb_nbanews WHERE link=%s",dbLink)
    checkExist = cur.fetchone()
    if checkExist == None:
        cur.execute("INSERT INTO cmdb_nbanews(source,pubtime,link,title,content) VALUES(%s,%s,%s,%s,%s)", ("NBA中文网", dbPubtime, dbLink, dbTitle, dbContent))
        cur.connection.commit()
        print("Feedback: 来自[NBA中文网]的新闻[%s]已经保存到数据库." % dbTitle)
    else:
        print("Feedback: 来自[NBA中文网]的新闻[%s]已存在!" % dbTitle)
        return -1

url = "http://china.nba.com/news/"
urlData = requests.get(url).text
soup = BeautifulSoup(urlData, 'lxml')
newsList = soup.find('div', {'class':'news-list'}).findAll('a',href = re.compile("^http://.*"))
for n in newsList:
    title = n.find('span', {'class':'news-title'}).text
    inUrl = n.get("href")
    inPage_data = requests.get(inUrl).text
    inSoup = BeautifulSoup(inPage_data, 'lxml')
    pubtime = inSoup.find('span', {'class':'article-time'}).text
    content = inSoup.find(id="Cnt-Main-Article-QQ").text
    if storeNews(pubtime, inUrl, title, content) == -1:
        print("Finish: 检测到重复,[NBA中文网]采集结束.")
        break

endtime = datetime.datetime.now()
print(endtime - starttime)