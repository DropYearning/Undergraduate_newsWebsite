# coding:utf-8
import jieba
import jieba.analyse
import pymysql
import datetime

# 计时跟踪
starttime = datetime.datetime.now()
# 与数据库建立连接
conn = pymysql.connect(host="127.0.0.1",port=3306,user='root',passwd='hdu220313',db='web',charset='utf8')
cur = conn.cursor()

# 载入球队字典
jieba.load_userdict('/Users/Zhouliang/PycharmProjects/NBA/teamdict.txt')
# 载入球员字典
jieba.load_userdict('/Users/Zhouliang/PycharmProjects/NBA/playerdict.txt')
# 载入教练字典
jieba.load_userdict('/Users/Zhouliang/PycharmProjects/NBA/coachdict.txt')
# 载入事件字典
jieba.load_userdict('/Users/Zhouliang/PycharmProjects/NBA/eventdict.txt')

cur.execute("SELECT count(id) FROM cmdb_nbanews")
count = cur.fetchone()
count = count[0]
cur.execute("SELECT id, title FROM cmdb_nbanews LIMIT 0,%d" % count)
rt = cur.fetchall()
for row in rt:
    id = row[0]
    title = row[1]
    keywords = jieba.analyse.extract_tags(title, allowPOS=('nr', 'nz'))
    keys_str = ','.join(keywords)
    output = {
        'ID':id,
        '标题': title,
        '关键词':keys_str
    }
    print(output)
    cur.execute("UPDATE cmdb_nbanews SET keywords='%s' WHERE id=%d" %(keys_str,id))
    cur.connection.commit()

# 释放数据库连接
cur.close()
conn.close()
# 显示运行时间
endtime = datetime.datetime.now()
print (endtime - starttime)