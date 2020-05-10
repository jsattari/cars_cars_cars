from os.path import join, dirname
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row, column, gridplot, layout
from bokeh.models import (
    ColumnDataSource, Select, Slider, HoverTool, SingleIntervalTicker,
    NumeralTickFormatter, Label, Dropdown, Title)
from bokeh.plotting import figure


# function that filters data
def get_dataset(src, name, car):
    df = src[(src.year == name) & (src.brand == car)].copy()
    return ColumnDataSource(data=df)


# function to create graph
def create_figure(src):
    x_title = 'Mileage (miles)'
    y_title = 'Price (dollars)'
    p = figure(
        x_range=(0, 1100000), y_range=(0, 100000),
        plot_height=400, plot_width=800, tools='pan,box_zoom,reset,save')
    p.title.text_font_size = '25px'
    p.title.text_color = 'black'
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title
    p.xaxis.formatter.use_scientific = False
    p.yaxis.formatter.use_scientific = False
    p.xaxis.formatter = NumeralTickFormatter(format=('0[.]0a'))
    p.yaxis.formatter = NumeralTickFormatter(format=('$0,0.00'))
    p.background_fill_color = "black"
    p.background_fill_alpha = 0.05
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.outline_line_width = 2
    p.outline_line_alpha = 0.8
    p.outline_line_color = "red"
    p.xaxis.ticker = SingleIntervalTicker(interval=100000)
    p.yaxis.ticker = SingleIntervalTicker(interval=10000)
    p.circle(x='mileage', y='price', size=5,
             color="red", alpha=0.8, source=src)
    return p


def create_linegraph(src):
    p2 = figure(
        x_range=(2012, 2020), y_range=(0, 100000),
        plot_height=600, plot_width=800, tools='pan,box_zoom,reset,save',
        title='Average Price by Year', title_location='above')
    x_title = 'Year'
    y_title = 'Avg_Price (dollars)'
    p2.title.text_font_size = '25px'
    p2.title.text_color = 'black'
    p2.xaxis.axis_label = x_title
    p2.yaxis.axis_label = y_title
    p2.xaxis.formatter.use_scientific = False
    p2.yaxis.formatter.use_scientific = False
    p2.xaxis.formatter = NumeralTickFormatter(format=('0'))
    p2.yaxis.formatter = NumeralTickFormatter(format=('$0,0.00'))
    p2.background_fill_color = "black"
    p2.background_fill_alpha = 0.05
    p2.xgrid.grid_line_color = None
    p2.ygrid.grid_line_color = None
    p2.outline_line_width = 2
    p2.outline_line_alpha = 0.8
    p2.outline_line_color = "red"
    p2.xaxis.ticker = SingleIntervalTicker(interval=1)
    p2.yaxis.ticker = SingleIntervalTicker(interval=10000)
    p2.line(x='year', y='avg_price', line_width=3, source=src)
    return p2

# function that updates based on slider
def update_plot(attrname, old, new):
    year = year_select.value
    label.text = str(year)
    brand = brand_select.value
    src = get_dataset(df2, year, brand)
    source.data.update(src.data)


# function to change title based on brand
def update_title(attrname, old, new):
    brand = brand_select.value
    title.text = 'Car Resale Values by Year (Since 2012): ' + brand


# import data
df = pd.read_csv(join(dirname(__file__), 'data/usa_cars_datasets.csv'))

# filter data to post 2012
df2 = df[df.year >= 2012]

# set inital plot to filter on min year
year = df2.year.min()

# brand values
brand_list = df2.brand.unique().tolist()
# brand_list = brand_list.sort()
brand = brand_list[0]

# apply filter to data based on year var
source = get_dataset(df2, year, brand)

# create plot from source
plot = create_figure(source)

# year label on plot
label = Label(x=840000, y=80000, text=str(
    df2['year'].min()), text_font_size='60px', text_color='#ff496c')

# dynamic plot title
title = Title(text='Car Resale Values by Year (Since 2012): ' + brand, align='left')

# adding plot labels to glyph
plot.add_layout(label)
plot.add_layout(title, 'above')

# slider tool, slider update action
year_select = Slider(
    start=df2['year'].min(), end=df2['year'].max(), value=df2['year'].min(), step=1, title="Year")
year_select.on_change('value', update_plot)

# brand select and update action
brand_select = Select(
    title="Brand:", value=brand_list[0], options=brand_list)
brand_select.on_change('value', update_plot)
brand_select.on_change('value', update_title)

# hover tool (shows values on graph)
hover_tool = HoverTool(
    tooltips=[
        ('Make', '@brand'),
        ('Model', '@model'),
        ('State', '@state'),
        ('Price', '@price{($0,000.00)}'),
        ('Mileage', '@mileage{(0,000)}')])

# adding hover tools to plot
plot.add_tools(hover_tool)

# line graph data filtration
df_short = df2[['year', 'price']]

# group by mean and reset index
df_line = df_short.groupby(df['year'])['price'].agg(['mean'])
df_line = df_line.reset_index(drop=False)

# rename columns
df_line.columns = ['year', 'avg_price']

# declare source of line graph
source2 = ColumnDataSource(df_line)

# create line graph
line_plot = create_linegraph(source2)

# hover tool (shows values on graph)
hover_tool2 = HoverTool(
    tooltips=[
        ('Average Price', '@avg_price{($0,000.00)}'),
        ('Year', '@year{(0000)}')])

# adding hover tools to plot
line_plot.add_tools(hover_tool2)

# format widget grid for layout
widgets = column(year_select, brand_select, sizing_mode='scale_width')

# format layout
curdoc().add_root(layout([
    [plot, widgets],
    [line_plot]
], sizing_mode='stretch_height'
))
curdoc().title = "cars_cars_cars"
