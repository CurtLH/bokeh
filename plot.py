import pandas as pd
from bokeh.sampledata.iris import flowers
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool

colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
flowers['colors'] = [colormap[x] for x in flowers['species']]

hover = HoverTool(tooltips=[
    ("Sepal length", "@sepal_length"),
    ("Sepal width", "@sepal_width"),
    ("Petal length", "@petal_length"),
    ("Species", "@species")
    ])

p = figure(title = "Iris Morphology", plot_height=500, plot_width=500, tools=[hover, "pan,reset,wheel_zoom"])

p.xaxis.axis_label = 'Petal Length'
p.yaxis.axis_label = 'Petal Width'

p.circle('petal_length', 'petal_width', color='colors', 
         fill_alpha=0.2, size=10, source=ColumnDataSource(flowers))

output_file('flowers.html')

show(p)

from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [5, 3, 4, 2, 4, 6]

source = ColumnDataSource(data=dict(fruits=fruits, counts=counts))

q = figure(x_range=fruits, plot_height=350, toolbar_location=None, title="Fruit Counts")
q.vbar(x='fruits', top='counts', width=0.9, source=source, legend="fruits",
       line_color='white', fill_color=factor_cmap('fruits', palette=Spectral6, factors=fruits))

q.xgrid.grid_line_color = None
q.y_range.start = 0
q.y_range.end = 9
q.legend.orientation = "horizontal"
q.legend.location = "top_center"

