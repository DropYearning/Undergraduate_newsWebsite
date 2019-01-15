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
        cur.execute("INSERT INTO cmdb_nbanews(source,pubtime,link,title,content) VALUES(%s,%s,%s,%s,%s)",("搜狐",dbPubtime,dbLink,dbTitle,dbContent))
        cur.connection.commit()
        print("Feedback: 来自[搜狐]的新闻[%s]已经保存到数据库." % dbTitle)
    else:
        print("Feedback: 来自[搜狐]的新闻[%s]已存在!" % dbTitle)
        return -1

#采集首页新闻
startUrl = "http://sports.sohu.com/nba_a.shtml"
startData = requests.get(startUrl)
# charset = GBK
startData.encoding = 'gbk'
sgbkData = startData.text
ssoup = BeautifulSoup(sgbkData, 'lxml')

#获取新闻页数
varString = re.search(r'var maxPage = [0-9]*', sgbkData).group(0)
pageCount = re.search(r'\d+', varString).group(0)

snewsList = ssoup.find('div', {'class': 'f14list'}).findAll('a', href=re.compile("http://www.sohu.com/a/[0-9]+_[0-9]"))
for n in snewsList:
    stitle = n.get_text()
    sinUrl = n.get("href")
    sinPage_data = requests.get(sinUrl).text
    sinSoup = BeautifulSoup(sinPage_data, 'lxml')
    try:
        spubtime = sinSoup.find(id="news-time").get_text()
    except AttributeError as err:
        print("Error: 采集来自[搜狐]的新闻"+stitle+" "+sinUrl+"出现错误!")
        continue
    scontent = sinSoup.find(attrs={'class': 'article'}).text
    scontent_out = re.sub('[\n\r\t\xa0\u200b]', '', scontent)
    #首页去重
    if storeNews(spubtime, sinUrl, stitle, scontent_out) == -1:
        print("Finish: 检测到重复,[搜狐]采集结束.")
        exit(0)


def pageCollect(url):
    urlData = requests.get(url)
    urlData.encoding = 'gbk'
    gbkData = urlData.text
    soup = BeautifulSoup(gbkData, 'lxml')
    newsList = soup.find('div', {'class': 'f14list'}).findAll('a', href=re.compile("http://www.sohu.com/a/[0-9]+_[0-9]"))
    for n in newsList:
        title = n.get_text()
        inUrl = n.get("href")
        inPage_data = requests.get(inUrl).text
        inSoup = BeautifulSoup(inPage_data, 'lxml')
        try:
            pubtime = inSoup.find(id="news-time").get_text()
        except AttributeError :
            print("Error: 采集来自[搜狐]的新闻"+title+" "+inUrl+"出现错误!")
            continue
        content = inSoup.find(attrs={'class': 'article'}).text
        content_out = re.sub('[\n\r\t\xa0\u200b]', '', content)
        if storeNews(pubtime, inUrl, title, content_out) == -1:
            return -1


#继续采集后9页新闻
for i in range(1,10):
    pageNumber = int(pageCount) - i
    sohuUrl = 'http://sports.sohu.com/nba_a_'+str(pageNumber)+".shtml"
    if pageCollect(sohuUrl) == -1:
        print("Finish: 检测到重复,[搜狐]采集结束.")
        exit(0)


#释放数据库连接
cur.close()
conn.close()
#显示运行时间
endtime = datetime.datetime.now()
print (endtime - starttime)