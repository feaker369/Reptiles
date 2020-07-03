# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 21:28:47 2020

@author: Administrator
"""

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from wordcloud import WordCloud
from scipy.misc import imread
from imageio import imread
import jieba
from pylab import mpl
from pyecharts import options as opts
from pyecharts.charts import Map

#数据清洗部分
# 使用matplotlib能够显示中文
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
#  读取数据
df = pd.read_csv('1.csv', encoding='gbk')

# 进行数据清洗，过滤掉实习岗位
#df.drop(df[df['职位名称'].str.contains('实习')].index, inplace=True)
#print(df.describe())


# 由于csv文件中的字符是字符串形式，先用正则表达式将字符串转化为列表，在去区间的均值
pattern = '\d+'
df['工作年限'] = df['工作经验'].str.findall(pattern)
print(type(df['工作年限']), '\n\n\n')
avg_work_year = []
count = 0
for i in df['工作年限']:
    # print('每个职位对应的工作年限',i)
    # 如果工作经验为'不限'或'应届毕业生',那么匹配值为空,工作年限为0
    if len(i) == 0:
        avg_work_year.append(0)
        count += 1
    # 如果匹配值为一个数值,那么返回该数值
    elif len(i) == 1 or len(i) == 2:
        avg_work_year.append(int(''.join(i)))
        count += 1
    # 如果匹配为一个区间则取平均值
    else:
        num_list = [int(j) for j in i]
        avg_year = sum(num_list) / 2
        avg_work_year.append(avg_year)
        count += 1
print(count)
df['avg_work_year'] = avg_work_year

#将字符串转化为列表，薪资取中间值
df['salary'] = df['薪资'].str.findall(pattern)
#
avg_salary_list = []
for k in df['salary']:
    int_list = [int(n) for n in k]
    avg_salary = int_list[0] + (int_list[1] - int_list[0]) / 2
    avg_salary_list.append(avg_salary)
df['月薪'] = avg_salary_list

company_size = []
count1 = 0;
for i in df['公司规模']:
    if i == "2000人以上":
        company_size.append('超大')
    
    elif i == "500-2000人":
        company_size.append('大型')
        count1 += 1
    elif i == "150-500人":
        company_size.append('中上')

    elif i == "50-150人":
        company_size.append('中型')
        
    elif i == "15-50人":
        company_size.append('小型')
        
    elif i == "少于15人":
        company_size.append('微型')
        
df['company_size'] = company_size  
df.to_csv('python1.csv', index=False,encoding='gbk')

#数据可视化部分
"""1、绘制python薪资的频率直方图并保存"""
plt.hist(df['月薪'], bins=8, facecolor='#ff6700', edgecolor='blue')  # bins是默认的条形数目
plt.xlabel('薪资(单位/千元)')
plt.ylabel('频数/频率')
plt.title('大数据岗位薪资直方图')
plt.savefig('大数据岗位薪资分布.jpg')
plt.show()

"""2、绘制饼状图并保存"""
city = df['城市'].value_counts()
print(type(city))
# print(len(city))
label = city.keys()
print(label)
city_list = []
count = 0
n = 1
distance = []
for i in city:

    city_list.append(i)
    print('列表长度', len(city_list))
    count += 1
    if count > 5:
        n += 0.1
        distance.append(n)
    else:
        distance.append(0)
plt.pie(city_list, labels=label, labeldistance=1.2, autopct='%2.1f%%', pctdistance=0.6, shadow=True, explode=distance)
plt.axis('equal')  # 使饼图为正圆形
plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
plt.savefig('大数据岗位地理位置分布图.jpg')
plt.show()

plt.hist(df['company_size'], bins=6, facecolor='#ff6700', edgecolor='blue')  # bins是默认的条形数目
plt.xlabel('规模')
plt.ylabel('频数/频率')
plt.title('对大数据有需求的公司直方图')
plt.savefig('对大数据有需求的公司分布.jpg')
plt.show()

"""4、绘制福利待遇的词云"""
text = ''
for line in df['公司福利']:
    if len(eval(line)) == 0:
        continue
    else:
        for word in eval(line):
            # print(word)
            text += word

cut_word = ','.join(jieba.cut(text))
word_background = imread('词云.jpg')
cloud = WordCloud(
    font_path=r'C:\Windows\Fonts\simfang.ttf',
    background_color='white',
    mask=word_background,
    max_words=500,
    max_font_size=100,
    width=400,
    height=800

)
word_cloud = cloud.generate(cut_word)
word_cloud.to_file('福利待遇词云.png')
plt.imshow(word_cloud)
plt.axis('off')
plt.show()

"""5、基于pyechart的柱状图"""
city = df['城市'].value_counts()
print(type(city))
print(city)
# print(len(city))

keys = city.index  # 等价于keys = city.keys()
values = city.values

data = [('北京', 116),('四川', 28),('辽宁', 2),('广东',126),('福建', 1),
       ('浙江', 43),('安徽', 3),('甘肃', 1),('江苏', 10),('广西', 2),
       ('山东', 1),('上海', 81),('天津', 4),('湖北', 12),('陕西', 7),
       ('湖南', 3),('河南', 2),('重庆', 8)]
def map_china() -> Map:
    c = (
        Map()
        .add(series_name="需求人数", data_pair=data, maptype="china",zoom = 1,center=[105,38])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="大数据岗位需求图"),
            visualmap_opts=opts.VisualMapOpts(max_=9999,is_piecewise=True,
                            pieces=[{"max": 10, "min": 0, "label": "10-0","color":"#FFE4E1"},
                                    {"max": 20, "min": 11, "label": "20-11","color":"#FF7F50"},
                                    {"max": 50, "min": 21, "label": "50-21","color":"#F08080"},
                                    {"max": 100, "min": 51, "label": "100-51","color":"#CD5C5C"},
                                    {"max": 200, "min": 101, "label": ">=100", "color":"#8B0000"}]
                                             )
        )
    )
    return c

d_map = map_china()
d_map.render("map.html")