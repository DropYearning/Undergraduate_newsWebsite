# coding:utf-8
import re
import pymysql
import requests
import datetime
from bs4 import BeautifulSoup
#计时跟踪
starttime = datetime.datetime.now()

#使用pymysql进行数据库连接
conn = pymysql.connect(host="127.0.0.1",port=3306,user='root',passwd='hdu220313',db='web',charset='utf8')
cur = conn.cursor()

#新闻存储函数
def storeNews(dbPubtime,dbLink,dbTitle,dbContent):
    cur.execute("SELECT id FROM cmdb_nbanews WHERE link=%s",dbLink)
    checkExist = cur.fetchone()
    if checkExist == None:
        cur.execute("INSERT INTO cmdb_nbanews(source,pubtime,link,title,content) VALUES(%s,%s,%s,%s,%s)",("虎扑",dbPubtime,dbLink,dbTitle,dbContent))
        cur.connection.commit()
        print("Feedback: 来自[虎扑]的新闻[%s]已经保存到数据库." % dbTitle)
    else:
        print("Feedback: 来自[虎扑]的新闻[%s]已存在!" % dbTitle)
        return -1

#页面分析函数
def pageCollect(url):
    urlData = requests.get(url).text
    soup = BeautifulSoup(urlData,'lxml')
    newsList = soup.select("div.list-hd > h4 > a")
    for n in newsList:
        title = n.get_text()
        inUrl = n.get("href")
        inPage_data = requests.get(inUrl).text
        inSoup = BeautifulSoup(inPage_data, 'lxml')
        pubtime = inSoup.find(id="pubtime_baidu").text
        content = inSoup.find(attrs={'class' :'artical-main-content'}).text
        content_out = re.sub('[\n\r\t\xa0\u200b]','',content)
        if storeNews(pubtime, inUrl, title, content_out) == -1:
            return -1

#每次最多采集前十页新闻
for pageNumber in range(1,10) :
    hupuUrl = "https://voice.hupu.com/nba/"+str(pageNumber)
    if pageCollect(hupuUrl) == -1:
        print("Finish: 检测到重复,[虎扑]采集结束.")
        exit(0)



#释放数据库连接
cur.close()
conn.close()
endtime = datetime.datetime.now()
print (endtime - starttime)