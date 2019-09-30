from collections import Counter

import jieba
import pymysql
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pyecharts import options
from pyecharts.options import InitOpts, TextStyleOpts

import lagou


def draw_img(result):
    tmp = [(area, num * 5) for area, num in result]
    c = (
        Geo(InitOpts(width="center", height="700px", page_title="Area-Top30", bg_color="#152353"))
            .add_schema(
            maptype="china",
            itemstyle_opts=options.ItemStyleOpts(color="#AFEEEE	", border_color="#111"),
            )
            .add(
            "",
            tmp,
            type_=ChartType.EFFECT_SCATTER,
            color="red",
            )
            .set_series_opts(label_opts=options.LabelOpts(is_show=False))
            .set_global_opts(xaxis_opts=options.AxisOpts(),
                             title_opts=options.TitleOpts(title="Area-Top30", pos_left="center", title_textstyle_opts=TextStyleOpts(color="#cdcd66", font_size=24, font_family="Courier New")),\
                             visualmap_opts=options.VisualMapOpts(min_=1700, max_=95000, range_text=("高", "低"), pos_left="10%", \
                                                                  is_calculable=False, pos_top="top", range_color=["#DDDD00", "#C75D17", "#AA3434"],\
                                                                  textstyle_opts=TextStyleOpts(color="white", font_family="Courier New")))
    )
    c.render()


def get_job_address():
    address = []
    try:
        with lagou.ensure_conn().cursor() as cursor:
            cursor.execute("select job_address from tb_data")
            for value in cursor.fetchall():
                address.append(value[0][0:2])
    except pymysql.MySQLError as err:
        print(err)
    return address


def main():
    # draw_img()
    address = get_job_address()
    text = "".join(address)
    list = jieba.lcut(text)
    count = list.count("异地")
    for _ in range(0, count):
        list.remove("异地")
    counter = Counter(list)
    result = counter.most_common(30)
    print(result)
    draw_img(result)


if __name__ == '__main__':
    main()