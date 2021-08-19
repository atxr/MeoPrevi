#!/usr/bin/env python3
# Grab the prevision of important satellites

import os
from plotly.express import timeline
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

database_sats = 'data/maj_sats.data'

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
with open(database_sats, 'r') as f:
    sats = {sat:idsat for [sat, idsat] in [x.strip('\n').split('~') for x in f.readlines()]}

df = pd.DataFrame([])
for sat in sats:
    
    satid = sats[sat]
    print(sat, end=' - ')
    
    try:
        f = open('data/.'+sat+'.tmp', 'r')
        beg = datetime.fromisoformat(f.readline().strip('\n'))
        end = datetime.fromisoformat(f.readline().strip('\n'))
        now = datetime.utcnow()
        if beg > now or now > end:
            f.close()
            raise Exception('Expired file')
        
        print('Using local database ...')
        tab = f.read()

    except (FileNotFoundError, Exception):
        print('Downloading data ...')
        url = "https://heavens-above.com/PassSummary.aspx?lat=43.7413&lng=6.9&loc=Caussol&alt=0&tz=CET&satid="+str(satid)
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        driver.find_element_by_id("ctl00_cph1_radioAll").click()
        tab = driver.find_element_by_class_name("standardTable").text
        driver.close()

        with open('data/.'+sat+'.tmp', 'w') as f:
            f.write(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S\n"))
            f.write((datetime.utcnow() + timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S\n"))
            f.write(tab)

    
    lines = tab.split('\n')[2:]
    lines = list(map(lambda x: x.split(' '), lines))


    # shape of a line 
    #['18', 'Aug', '-', '08:42:50', '10°', 'NE', '09:04:22', '22°', 'E', '09:24:53', '10°', 'SE', 'daylight']

    sh = {'day': 0, 'mon' : 1, 'h_st' : 3, 'p_st':5, 'clm':7, 'p_clm':8, 'h_fi':9, 'p_fi':11}

    begs = [datetime.fromisoformat(str(datetime.now().year) +'-'+  str(months.index(x[sh['mon']])+1).rjust(2,"0") +'-'+ x[sh['day']] +' '+ x[sh['h_st']]) for x in lines]
    ends = [datetime.fromisoformat(str(datetime.now().year) +'-'+  str(months.index(x[sh['mon']])+1).rjust(2,"0") +'-'+ x[sh['day']] +' '+ x[sh['h_fi']]) for x in lines]
    for i in range(len(lines)):
        #switch to UTC
        begs[i] -= timedelta(hours=2)
        ends[i] -= timedelta(hours=2)
        
        if begs[i] > ends[i]:
            ends[i] += timedelta(days=1)

    clms = [int(x[sh['clm']][:-1]) for x in lines]

    for beg, end, clm in zip(begs, ends, clms):
        if int(clm) > 20:
            df = df.append(pd.DataFrame([dict(Sat=sat.ljust(10, ' '), Start=beg, Finish=end)]))


print(df)

utc = datetime.utcnow()
xmin = (utc - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
xmax = (utc + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")

fig = timeline(df, x_start = 'Start', x_end='Finish', title="Previ MEO", y='Sat', color='Sat', range_x=[xmin,xmax], hover_name='Sat', height=900)
fig.update_layout(
    hoverlabel=dict(
        font_size=25
    )
)

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

os.system("sleep 2; xdg-open http://127.0.0.1:8050/")
app.run_server(debug=False, use_reloader=False)

