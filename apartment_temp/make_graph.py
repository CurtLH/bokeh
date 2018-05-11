#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from subprocess import run

# define path to project
path = '/home/curtis/github/bokeh/apartment_temp'

# if we are not there, move to the project
if os.getcwd() != path:
    os.chdir(path)

# connect to the database
conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="apassword",
                        host="localhost")

conn.autocommit = True
cur = conn.cursor()
engine = create_engine('postgresql://postgres:apassword@localhost:5432/postgres')

# read in SQL query
fd = open('query.sql', 'r')
sql = fd.read()
fd.close()

# run SQL query
df = pd.read_sql_query(sql, engine)

# subset the df to 1 week
df = df.tail(98)

# format data for plotting
source = ColumnDataSource(df)

# create bokeh plot
output_file('temps.html')

# define hover tooltips
hover = HoverTool(tooltips=[('datetime', '@datetime{%F}'),
                            ('inside', '@inside{1.1}'),
                            ('outside', '@outside{1.1}')],
                  formatters={'datetime': 'datetime'},
                  mode='vline')

# create plot
p = figure(x_axis_type='datetime', 
           plot_width=600, 
           plot_height=400,
           title='Apartment Temperatures',
           tools=[hover, 'pan', 'wheel_zoom', 'box_zoom', 'reset'])

# adjust the title
p.title.align = 'center'
p.title.text_font_size = '20pt'

# get current datetime for the title
now = datetime.now().strftime('%A %B %d %I:%M%p')
last_updated = 'Last updated {}'.format(now)

# configure plot
p.grid.grid_line_alpha=0.3
p.xaxis.axis_label = last_updated
p.yaxis.axis_label = 'Temperature'

# add inside temperature
p.line('datetime', 
       'inside', 
       color='#ef8a62', 
       legend='Inside', 
       line_width=4, 
       source=source)

# add outside temperature
p.line('datetime', 
       'outside', 
       color='#67a9cf', 
       legend='Outside', 
       line_width=4, 
       source=source)

# show the plot
show(p)

# commit the changes
run(['git', 'add', '.'])
run(['git', 'commit', '--amend', '--no-edit'])
#run(['git', 'push', '-f'])
