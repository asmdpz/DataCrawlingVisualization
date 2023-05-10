import pyecharts.options as opts
from pyecharts.charts import Line, Grid
import pandas as pd
import numpy as np


# 绘制折线图
# x为横坐标
# y为纵坐标（折线数据）
# z为折线的名称
def draw_line(x, y, z):
    x = np.array(x).astype("str")
    l = Line()
    l.add_xaxis(xaxis_data=x)
    for i in range(len(y)):
        l.add_yaxis(series_name=z[i],y_axis=y[i])
    l.set_global_opts(
            title_opts=opts.TitleOpts(title="教育分类股票收盘价折线图",title_textstyle_opts=opts.TextStyleOpts(font_size=30),pos_left="30%",subtitle="从2022-3-28至2023-3-24",subtitle_textstyle_opts=opts.TextStyleOpts(font_size=18)),
            xaxis_opts=opts.AxisOpts(name="日期", type_="category", boundary_gap=False,is_show=True, axislabel_opts=opts.LabelOpts(rotate=20,margin=5)),
            yaxis_opts=opts.AxisOpts(name="收盘价",is_show=True),

            legend_opts=opts.LegendOpts(pos_top="8%", item_gap=12, textstyle_opts=opts.TextStyleOpts(font_size=16))

    )
    line = (
        l
    )
    g = Grid(
        init_opts=opts.InitOpts(
            width="1800px",
            height="950px",
            page_title="教育分类股票收盘价折线图"
        )
    )
    g.add(line, grid_opts=opts.GridOpts(pos_top="20%"))
    g.render("./picture/result.html")


def read_data():
    url = "./dataset/data.csv"
    data_list = pd.read_csv(url)
    data_list = data_list.groupby('股票名称')
    x = []
    y = []
    z = []
    x_key = 1
    for data in data_list:
        data = data[1]
        if x_key == 1:
            x = data['日期']
            x = np.array(x)
            x_key = 0
        close_price = data['收盘价']
        close_price = np.array(close_price).astype("str")
        y.append(close_price)
        name = data['股票名称']
        name = np.array(name)
        name = name[0]
        z.append(name)
        # print(f"name-->{name}")
    return x, y, z


def main():
    # 将csv文件中的数据可视化
    print("++++++++++++正在可视化白酒的k线数据++++++++++++")
    x,y,z = read_data()
    draw_line(x,y,z)


if __name__ == '__main__':
    main()
