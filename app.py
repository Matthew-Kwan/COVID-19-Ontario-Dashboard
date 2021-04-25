# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time
import datetime

# Import style sheet
external_stylesheets = ['./style.css']

# Define the Dash app
app = dash.Dash(__name__)

# Define the server
server = app.server

# IMPORT DATA
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# The link below auto updates the dashboard with the latest covidtesting.csv available (tested this with 1 day)
df = pd.read_csv('https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv')

# DATA CLEANING
# Need to prep a variety of datasets for use in the dashboard

# dataframe for variants
df_variant = df[df['Reported Date'] >= '2021-01-15']

# convert to date time and subtract 7 days
df_variant['Reported Date'] = pd.to_datetime(df['Reported Date']) - pd.to_timedelta(7, unit='d')

# add new columns
df_variant['New_B.1.1.7_Cases'] = df_variant['Total_Lineage_B.1.1.7'].fillna(0).diff()
df_variant['New_B.1.351_Cases'] = df_variant['Total_Lineage_B.1.351'].fillna(0).diff()
df_variant['New_P.1_Cases'] = df_variant['Total_Lineage_P.1'].fillna(0).diff()
df_variant['Total_New_Cases'] = df_variant['Total Cases'].diff()
df_variant['New_Regular_Cases'] = df_variant['Total_New_Cases'] - (df_variant['New_B.1.1.7_Cases'] + df_variant['New_B.1.351_Cases'] + df_variant['New_P.1_Cases'])

# group by week
df_variant_v2 = df_variant.groupby([pd.Grouper(key='Reported Date', freq='W')])['New_B.1.1.7_Cases', 'New_B.1.351_Cases','New_P.1_Cases','New_Regular_Cases','Total_New_Cases'].sum().reset_index().sort_values('Reported Date')

# Add percentage columns for text on stacked barchart
df_variant_v2["%_B.1.1.7"] = df_variant_v2["New_B.1.1.7_Cases"]/df_variant_v2["Total_New_Cases"]
df_variant_v2["%_B.1.351"] = df_variant_v2["New_B.1.351_Cases"]/df_variant_v2["Total_New_Cases"]
df_variant_v2["%_P.1"] = df_variant_v2["New_P.1_Cases"]/df_variant_v2["Total_New_Cases"]
df_variant_v2["%_Regular"] = df_variant_v2["New_Regular_Cases"]/df_variant_v2["Total_New_Cases"]

# drop the last row (which will always be an incomplete week)
df_variant_v2 = df_variant_v2[:-1]

# Add total new cases daily to df
df['Total_New_Cases'] = df['Total Cases'].diff()

# METRICS DATASET
df_metrics = df.copy()
df_metrics.sort_values(by='Reported Date', ascending=False, inplace=True)

df_metrics_v2 = df_metrics.groupby(df.index // 7).mean()
df_metrics_v2 = df_metrics_v2.round(0)

week1 = df_metrics_v2.iloc[0,:]
week2 = df_metrics_v2.iloc[1,:]

m1 = ""
m2 = ""
m3 = ""

if ((week1["Number of patients hospitalized with COVID-19"] - week2["Number of patients hospitalized with COVID-19"]) >= 0):
  m1 = 'green'
else:
  m1 = 'red'

if ((week1["Number of patients in ICU due to COVID-19"] - week2["Number of patients in ICU due to COVID-19"]) >= 0):
  m2 = 'green'
else:
  m2 = 'red'

if ((week1["Number of patients in ICU on a ventilator due to COVID-19"] - week2["Number of patients in ICU on a ventilator due to COVID-19"]) >= 0):
  m3 = 'green'
else:
  m3 = 'red'

# END OF DATA CLEANING
# HELPER FUNCTIONS

def unixTimeMillis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))

def unixToDatetime(unix):
    ''' Convert unix timestamp to datetime. '''
    return pd.to_datetime(unix,unit='s')

def getMarks(start, end, Nth=100):
    ''' Returns the marks for labeling.
        Every Nth value will be used.
    '''
    result = {}
    for i, date in enumerate(daterange):
        if(i%Nth == 1):
            # Append value to dict
            result[unixTimeMillis(date)] = str(date.strftime('%Y-%m-%d'))

    return result



# Get the date range to work with dash.py and plotly
daterange = pd.date_range(start=df['Reported Date'].min(), end=df['Reported Date'].max())

# HTML LAYOUT
app.layout = html.Div(children=[
    html.H1(children='COVID-19 Ontario Dashboard'),

    html.Div(children='''
            A dashboard to help reveal the severity of the third-wave of COVID-19 in Ontario.
    ''', id="header-text"),

    html.Div([
      html.Div([
        html.P(children="Average # of Hospitalizations in Last 7 Days"),
        html.H2(children=str(week1["Number of patients hospitalized with COVID-19"])),
        html.P(children="Difference compared to 7 days prior: {}".format(str(week1["Number of patients hospitalized with COVID-19"] - week2["Number of patients hospitalized with COVID-19"])),
               className=m1)
      ], className="four columns metric")
    ]),

    html.Div([
      html.Div([
        html.P(children="Average # of ICUs in Last 7 Days"),
        html.H2(children=str(week1["Number of patients in ICU due to COVID-19"])),
        html.P(children="Difference compared to 7 days prior: {}".format(str(week1["Number of patients in ICU due to COVID-19"] - week2["Number of patients in ICU due to COVID-19"])),
               className=m2)
      ], className="four columns metric")
    ]),

    html.Div([
      html.Div([
        html.P(children="Average # of ICUs on a Ventilator in Last 7 Days"),
        html.H2(children=str(week1["Number of patients in ICU on a ventilator due to COVID-19"])),
        html.P(children="Difference compared to 7 days prior: {}".format(str(week1["Number of patients in ICU on a ventilator due to COVID-19"] - week2["Number of patients in ICU on a ventilator due to COVID-19"])),
               className=m3)
      ], className="four columns metric")
    ]),

    html.Div([
      html.Div([
        dcc.Graph(id='graph-with-slider')
      ], className="six columns")
    ]),

    html.Div([
      html.Div([
        dcc.Graph(id='stack-bar')
      ], className="six columns")
    ]),

    html.Div([
      html.Div([
        html.Div(children='''
          Use the date slider below to select dates for the graphs. Note that the graph on the right only starts around 01/2021.
        ''', id="slider-text"),
        html.P(id="date-range"),
        dcc.RangeSlider(
          id='date-slider',
          min = unixTimeMillis(daterange.min()),
          max = unixTimeMillis(daterange.max()),
          value = [unixTimeMillis(daterange.min()),
                    unixTimeMillis(daterange.max())],
          marks=getMarks(daterange.min(),
                      daterange.max())
      )
      ], className="twelve columns")
    ]),
])

# Checks for changes in the date slider
@app.callback(
    Output('date-range', 'children'),
    Output('graph-with-slider', 'figure'),
    Output('stack-bar', 'figure'),
    Input('date-slider', 'value'))
def update_figure(value):

    # Line graph for total cases
    filtered_df = df[df['Reported Date'] >= str(unixToDatetime(value[0]))]
    filtered_df = filtered_df[df['Reported Date'] <= str(unixToDatetime(value[1]))]

    fig = px.line(filtered_df, x="Reported Date", y="Total_New_Cases", title="Daily number of new COVID-19 cases in Ontario")
    fig.update_layout(transition_duration=500)

    # Stack bar graph for variant data
    df_variant_filtered = df_variant_v2[df_variant_v2['Reported Date'] >= str(unixToDatetime(value[0]))]
    df_variant_filtered = df_variant_filtered[df_variant_v2['Reported Date'] <= str(unixToDatetime(value[1]))]

    fig2 = go.Figure(data=[
    go.Bar(name='Regular', x=df_variant_filtered['Reported Date'], y=df_variant_filtered['New_Regular_Cases'], text=(df_variant_filtered['%_Regular']*100).round(2), textposition='auto'),
    go.Bar(name='B.1.1.7', x=df_variant_filtered['Reported Date'], y=df_variant_filtered['New_B.1.1.7_Cases'], text=(df_variant_filtered['%_B.1.1.7']*100).round(2), textposition='auto'),
    go.Bar(name='B.1.351', x=df_variant_filtered['Reported Date'], y=df_variant_filtered['New_B.1.351_Cases'], text=(df_variant_filtered['%_B.1.351']*100).round(2), textposition='auto'),
    go.Bar(name='P.1', x=df_variant_filtered['Reported Date'], y=df_variant_filtered['New_P.1_Cases'], text=(df_variant_filtered['%_P.1']*100).round(2), textposition='auto'),
    ])

    fig2.update_layout(barmode='stack', title_text="New Cases Weekly by COVID-19 Variant")

    date_range_p = "Date Range: {} to {}".format(str(unixToDatetime(value[0]).date()), str(unixToDatetime(value[1]).date()))
    return date_range_p, fig, fig2

if __name__ == '__main__':
    app.title = "COVID-19 Ontario Dashboard"
    app.run_server(debug=True)