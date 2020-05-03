from os.path import join, dirname
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select, Slider, HoverTool, SingleIntervalTicker
from bokeh.plotting import figure

def get_dataset(src, name):
    df = src[src.year == name].copy()
    return ColumnDataSource(data=df)


def create_figure(src):
    x_title = 'Mileage (miles)'
    y_title = 'Price (dollars)'
    p = figure(
        x_range=(0,1100000), y_range=(0,100000),
        plot_height=600, plot_width=800, tools='pan,box_zoom,reset',
        title='Car Resale Values by Year', title_location='above')
    p.title.text_font_size = '25px'
    p.title.text_color = 'black'
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title
    # p.xaxis.ticker = SingleIntervalTicker(interval=15)
    # p.yaxis.ticker = SingleIntervalTicker(interval=5)
    p.circle(x='mileage', y='price', size=5, color="red", alpha=0.5, source=src)
    return p


def update_plot(attrname, old, new):
    year = year_select.value
    src = get_dataset(df, year)
    source.data.update(src.data)


df = pd.read_csv(join(dirname(__file__), 'data/usa_cars_datasets.csv'))
df = df[df.year >= 2012]

year = df.year.min()

source = get_dataset(df, year)
plot = create_figure(source)

year_select = Slider(
    start=df['year'].min(), end=df['year'].max(), value=df['year'].min(), step=1, title="Year")

year_select.on_change('value', update_plot)

hover_tool = HoverTool(
        tooltips=[
            ('Make', '@brand'),
            ('Model', '@model'),
            ('State', '@state'),
            ('Price', '@price'),
            ('Mileage', '@mileage')])

plot.add_tools(hover_tool)

controls = column(year_select)

curdoc().add_root(row(plot, controls))
curdoc().title = "cars_cars_cars"
