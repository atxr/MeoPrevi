#!/usr/bin/env python3
# Grab the prevision of important satellites


import os
import pandas as pd
from plotly.express import timeline
from selenium import webdriver
from datetime import datetime, timedelta
import dash
import dash_core_components as dcc
import dash_html_components as html



def previ(sat, satid):
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
    
    df=pd.DataFrame([])
    for beg, end, clm in zip(begs, ends, clms):
        if int(clm) > 20:
            df = df.append([dict(Sat=sat, Start=beg, Finish=end)])

    return df




def get_figure(df, range_x=[]):
    utc = datetime.utcnow().replace(microsecond=0)
    if range_x== []:
        range_x = [(utc - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S"),
                   (utc + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")]

    fig = timeline(
            df, 
            x_start = 'Start', x_end='Finish', 
            title="Previ MEO", y='Sat', color='Sat', 
            range_x=range_x, 
            hover_name='Sat', height=900)
    fig.update_layout(
        hoverlabel=dict(
            font_size=25
        )
    )
    fig.add_vline(x=utc, line_width=3, line_dash="dash")
    return fig, range_x


def get_df(sats):
    df = pd.DataFrame([])
    for satid in sats:
        df = df.append(previ(sats[satid], satid)) 
    return df

def get_sats(datasets=['maj_sats.data']):
    sats = {}
    for dataset in datasets:
        with open('data/'+dataset, 'r') as f:
            #update sats dict with unique id
            sats.update({idsat:sat for [sat, idsat] in [x.strip('\n').split('~') for x in f.readlines()]})
    return sats


if __name__=='__main__':
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    sats = get_sats()
    df = get_df(sats)
    fig, range_x = get_figure(df)

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        html.H1('MEO Previ'),
        html.Div([ 
            html.H2('Options'),
            html.Div([
                html.H3('Add new satellite'),
                dcc.Input(id='new_sat_name', type='text', placeholder='Satelitte name'), 
                dcc.Input(id='new_sat_id', type='text', placeholder='Satelitte ID'),
                html.Button('Add', id='add_button')]),
            html.Div([html.H3('Controls'),
                html.Button('Refresh', id='refresh_button'),
                html.Button('Update local database', id='update_local_button')]),
            html.Div([html.H3('Dataset'),
                dcc.Dropdown(
                multi=True, disabled=False,
                options=[
                    {'label': 'ILRS major satelittes', 'value': 'maj_sats.data'},
                    {'label': 'All satelittes', 'value': 'sats.data'},
                    {'label': 'Galileos', 'value': 'galileo.data'}
                ], value='maj_sats.data', id='dataset_dropdown')]),
            ], id='option_div'),
        html.Div([
            html.H2('Timeline'),
            dcc.Graph(figure=fig, id='timeline'), 
            dcc.Interval(
                id='interval-component',
                interval=5*60*1000, # 5min (in milliseconds)
                n_intervals=0)
            ])
    ])

    
    @app.callback(
        dash.dependencies.Output('timeline', 'figure'),
        [dash.dependencies.Input('refresh_button', 'n_clicks')],
        [dash.dependencies.Input('add_button', 'n_clicks')],
        [dash.dependencies.Input('update_local_button', 'n_clicks')],
        [dash.dependencies.Input('dataset_dropdown', 'value')],
        [dash.dependencies.Input('interval-component', 'n_intervals')],
        [dash.dependencies.State('new_sat_name', 'value')],
        [dash.dependencies.State('new_sat_id', 'value')])
    def update_output(n_ref, n_add, n_upd_loc, dataset, n_inter, sat, satid):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate
        
        btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
        global df
        global range_x
        global sats

        if btn_id == 'add_button':
            #add new satellite to the figure, update time, but keep the range_x
            df = df.append(previ(sat, satid))
            figure, range_x = get_figure(df, range_x=range_x)
        
        elif btn_id == 'refresh_button':
            #update time and range_x 
            figure, range_x = get_figure(df)

        elif btn_id == 'update_local_button':
            #redownload every sats tpm file in the database
            tmpfiles = [file for file in os.listdir(os.getcwd()+'/data') 
                             if file[0] =='.' and file[-4:] == '.tmp']
            for file in tmpfiles:
                os.remove(os.getcwd()+'/data/'+file)
            df = get_df(sats)
            figure, range_x = get_figure(df, range_x=range_x)
        
        elif btn_id == 'dataset_dropdown':
            sats = get_sats(dataset)
            df = get_df(sats)
            figure, range_x = get_figure(df, range_x=range_x)
        
        else: #btn_id == 'interval-component'
            #update time only every 5min
            figure, range_x = get_figure(df, range_x=range_x)

        return figure, btn_id == 'dataset_dropdown'

    #os.system("sleep 2; xdg-open http://127.0.0.1:8050/")
    app.run_server(debug=True)

