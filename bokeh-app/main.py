from os.path import join, dirname
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import (
    ColumnDataSource, Select, Slider, HoverTool, SingleIntervalTicker,
    NumeralTickFormatter, Label)
from bokeh.plotting import figure


# function that filters data
def get_dataset(src, name):
    df = src[src.year == name].copy()
    return ColumnDataSource(data=df)


# function to create graph
def create_figure(src):
    x_title = 'Mileage (miles)'
    y_title = 'Price (dollars)'
    p = figure(
        x_range=(0, 1100000), y_range=(0, 100000),
        plot_height=600, plot_width=800, tools='pan,box_zoom,reset,save',
        title='Car Resale Values by Year', title_location='above')
    p.title.text_font_size = '25px'
    p.title.text_color = 'black'
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title
    p.xaxis.formatter.use_scientific = False
    p.yaxis.formatter.use_scientific = False
    p.xaxis.formatter = NumeralTickFormatter(format=('0,000'))
    p.yaxis.formatter = NumeralTickFormatter(format=('$0,000.00'))
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


# function that updates based on slider
def update_plot(attrname, old, new):
    year = year_select.value
    label.text = str(year)
    src = get_dataset(df, year)
    source.data.update(src.data)


# import data
df = pd.read_csv(join(dirname(__file__), 'data/usa_cars_datasets.csv'))

# filter data to post 2012
df = df[df.year >= 2012]

# set inital plot to filter on min year
year = df.year.min()

# apply filter to data based on year var
source = get_dataset(df, year)

# create plot from source
plot = create_figure(source)

# year label on plot
label = Label(x=800000, y=80000, text=str(
    df['year'].min()), text_font_size='70px', text_color='#ff496c')

# adding plot label to glyph
plot.add_layout(label)

# slider tool, slider update action
year_select = Slider(
    start=df['year'].min(), end=df['year'].max(), value=df['year'].min(), step=1, title="Year")
year_select.on_change('value', update_plot)

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

# apply columns to app grid
controls = column(year_select)

# format layout
curdoc().add_root(row(plot, controls))
curdoc().title = "cars_cars_cars"
