# coding:utf-8
from bs4 import BeautifulSoup
import requests

playerlist = []
teams = ["rockets","spurs","pelicans","grizzlies","mavericks","warriors",
        "lakers","suns","clippers","kings","timberwolves","blazers",
        "nuggets","thunder","jazz","celtics","raptors","76ers","knicks",
        "nets","wizards","magic","heat","hornets","hawks","pistons",
        "cavaliers","bucks","pacers","bulls"]
# 遍历相关介绍网页
for team in teams :
    url = "https://nba.hupu.com/players/"+team
    urlData = requests.get(url).text
    soup = BeautifulSoup(urlData,'lxml')
    list = soup.find('tbody').findAll('a')
    for n in list:
        name = n.get_text()
        if name != '\n\n':
            playerlist.append(name)
result_list = []
# 分割姓和名
for player in playerlist:
    templist = player.split('-')
    result_list = result_list + templist
# 生成球员字典
for name in result_list:
    print(name,end=' ')
    print("100",end=' ')
    print("nr")