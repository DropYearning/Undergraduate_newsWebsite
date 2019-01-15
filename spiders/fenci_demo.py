# coding:utf-8
import jieba
import  jieba.analyse
import jieba.posseg as pseg

# 载入球队字典
jieba.load_userdict('/Users/Zhouliang/PycharmProjects/NBA/teamdict.txt')
# 载入球员字典
jieba.load_userdict('/Users/Zhouliang/PycharmProjects/NBA/playerdict.txt')
# 载入事件字典
jieba.load_userdict('/Users/Zhouliang/PycharmProjects/NBA/eventdict.txt')

s1 = "库兹马：我可以成为一名非常不错的组织者"
s2 = "德拉季奇谈失利：从比赛的第一分钟就打得很糟,火箭惨败"
s3 = "大卫-李宣布从NBA退役 勇士夺冠功臣开启新人生"

# words = pseg.cut(s3)
# for word, flag in words:
#     print('%s %s' % (word, flag))

keywords = jieba.analyse.extract_tags(s2, allowPOS = ('nr','nz'))
print(keywords)