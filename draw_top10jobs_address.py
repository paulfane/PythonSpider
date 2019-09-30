# from snapshot_selenium import snapshot as driver

from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Pie, Radar, Bar


def set_Y(top_10, bar):
    for kw in top_10:
        bar.add_yaxis(f"{kw[0]}", [count * 5 for city, count in kw[1]])


# -> 后接的元数据，一般表明了函数的返回值为何种类型
def radar_base(top_10) -> Bar :
    tmp = top_10[0]
    tmp1 = tmp[1]
    xs = [city for city, count in tmp1]
    bar = Bar().add_xaxis(xs) \
               .set_series_opts(label_opts=opts.LabelOpts(is_show=False))\
               .set_global_opts(title_opts=opts.TitleOpts(title="Top10"))
    set_Y(top_10, bar)
    return bar


def main():
    pass


if __name__ == '__main__':
    main()
