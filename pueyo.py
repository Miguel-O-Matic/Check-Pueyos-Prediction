#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import pandas as pd

def plotRollingAvg(df, ax, names, title, logscale=False):
    for name in names:
        ax.plot(pd.to_datetime(df.loc[name].index), 
                df.loc[name].diff().rolling(window=7).mean(), 
                linewidth=2,
                label=name)

    _, ax2 = ax.get_xlim()
    ax.set_xlim(ax2-7*17, ax2)
    ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')

    if logscale:
        ax.set_yscale('log')
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
    ax.yaxis.set_minor_locator(plt.NullLocator())

    ax.legend(loc='best', prop={'size': 12})
    if title:
        ax.title.set_text(title+', 7-Day Rolling Avg')
    ax.grid(color='#d4d4d4')

# Load global time-series so we can compare US vs EU
df_global = pd.read_csv(
    ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/'
     'csse_covid_19_data/csse_covid_19_time_series/'
     'time_series_covid19_confirmed_global.csv'))
df_global = df_global.drop(columns=['Province/State','Lat', 'Long'])
df_global = df_global.groupby('Country/Region').agg('sum')
# Add row for EU+UK totals
eu = ['Austria',  'Belgium', 'Bulgaria',  'Croatia',    'Cyprus', 'Czechia',     'Denmark', 
      'Estonia',  'Finland', 'France',    'Germany',    'Greece', 'Hungary',     'Ireland', 
      'Italy',    'Latvia',  'Lithuania', 'Luxembourg', 'Malta',  'Netherlands', 'Poland', 
      'Portugal', 'Romania', 'Slovakia',  'Slovenia',   'Spain',  'Sweden',      'United Kingdom']
df_global.loc['EU+UK',:] = df_global.loc[eu].sum()

# Load US data so we can look at the four most populous states
df_us = pd.read_csv(
    ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/'
     'csse_covid_19_data/csse_covid_19_time_series/'
     'time_series_covid19_confirmed_US.csv'))
df_us = df_us.drop(columns=[
    'UID', 'iso2', 'iso3', 'code3', 'FIPS', 
    'Admin2', 'Country_Region','Lat', 'Long_'])
df_us = df_us.groupby('Province_State').agg('sum')
# Add row for US total (not needed or used)
df_us.loc['United States',:] = df_us.sum(axis=0)

countries = ['EU+UK', 'US']
print(df_global.diff(axis=1).loc[countries].iloc[:,-7:])
print('')

states = ['California', 'Texas', 'Florida', 'New York']
print(df_us.diff(axis=1).loc[states].iloc[:,-7:])

pd.plotting.register_matplotlib_converters()
plt.style.use('fivethirtyeight')
fig, (ax1, ax2) = plt.subplots(2,1,figsize=(10, 9))
plotRollingAvg(df_global, ax1, countries, 'Daily New Cases')
plotRollingAvg(df_us, ax2, states, '')
fig.autofmt_xdate() 
plt.show()
