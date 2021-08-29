#!/usr/bin/env python3
# Grab the prevision of important satellites


import os
from sys import argv
import pyautogui
import pandas as pd
from plotly.express import timeline, line_polar
from selenium import webdriver, common
from datetime import datetime, timedelta
import dash
import dash_core_components as dcc
import dash_html_components as html


months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

try:
   path = argv[1] 
   if path[-1] != '/':
       path += '/'
except:
   path = '/home/'+os.getlogin()+'/.local/bin/MeoPrevi/'
    

def previ(sat, satid):
    print(sat, end=' - ')
    
    try:
        f = open(path+'tmp/.'+sat+'.tmp', 'r')
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
        try:
            driver.find_element_by_xpath(xpath="//a[@href='SetCulture.ashx?newcul=en']").click()
            driver.get(url)
        except common.exceptions.WebDriverException:
            pass

        driver.find_element_by_id("ctl00_cph1_radioAll").click()
        tab = driver.find_element_by_class_name("standardTable").text
        driver.close()

        with open(path+'tmp/.'+sat+'.tmp', 'w') as f:
            f.write(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S\n"))
            f.write((datetime.utcnow() + timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S\n"))
            f.write(tab)

    
    lines = tab.split('\n')[2:]
    lines = list(map(lambda x: x.split(' '), lines))


    # shape of a line 
    #['18', 'Aug', '-', '08:42:50', '10°', 'NE', '09:04:22', '22°', 'E', '09:24:53', '10°', 'SE', 'daylight']

    sh = {'day': 0, 'mon' : 1, 'h_st' : 3, 'p_st':5, 'clm':7, 'p_clm':8, 'h_fi':9, 'p_fi':11}

    begs = [datetime.fromisoformat(str(datetime.now().year) +'-'+  str(months.index(x[sh['mon']])+1).rjust(2,"0") +'-'+ x[sh['day']].rjust(2,"0") +' '+ x[sh['h_st']]) for x in lines]
    ends = [datetime.fromisoformat(str(datetime.now().year) +'-'+  str(months.index(x[sh['mon']])+1).rjust(2,"0") +'-'+ x[sh['day']].rjust(2,"0") +' '+ x[sh['h_fi']]) for x in lines]
    for i in range(len(lines)):
        #switch to UTC
        begs[i] -= timedelta(hours=2)
        ends[i] -= timedelta(hours=2)
        
        if begs[i] > ends[i]:
            ends[i] += timedelta(days=1)

    clms = [int(x[sh['clm']][:-1]) for x in lines]
    p_clms = [x[sh['p_clm']] for x in lines]
    
    p_sts = [x[sh['p_st']] for x in lines]
    p_fis = [x[sh['p_fi']] for x in lines]

    df=pd.DataFrame([])
    for beg, end, clm, p_clm, p_st, p_fi in zip(begs, ends, clms, p_clms, p_sts, p_fis):
        if int(clm) > 20:
            traj = [{'theta':x, 'z':y} for x,y in [[p_st, 10], [p_clm, clm], [p_fi, 10]]]
            df = df.append([dict(Sat=sat, Start=beg, Finish=end, Traj=traj)])

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
            range_x=range_x, custom_data=['Traj'],
        hover_name='Sat', height=900, width=width*2/3)
    fig.update_layout(
        hoverlabel=dict(
            font_size=25
        )
    )
    fig.add_vline(x=utc, line_width=3, line_dash="dash")
    return fig, range_x

def get_polar(df_polar, sat):
    polar = line_polar(df_polar, r="z", theta="theta", range_r=[90,0], title='Trajectory '+sat,
                    width=(width/3 - 100) , height=(width/3 - 100))
    polar.update_layout(
            polar = dict(
                angularaxis_categoryarray = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 
                                             'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
                )
            )
    return polar

def get_df(sats):
    df = pd.DataFrame([])
    for satid in sats:
        df = df.append(previ(sats[satid], satid)) 
    print(df)
    return df

def get_sats(datasets=['ILRS_Satellites.data']):
    sats = {}
    for dataset in datasets:
        with open(path+'data/'+dataset, 'r') as f:
            #update sats dict with unique id
            sats.update({idsat:sat for [sat, idsat] in [x.strip('\n').split('~') for x in f.readlines()]})
    return sats


if __name__=='__main__':
    if not os.path.exists(path+'tmp'):
        os.mkdir(path+'tmp')

    width, _ = pyautogui.size()

    sats = get_sats()
    df = get_df(sats)
    fig, range_x = get_figure(df)
    polar = get_polar(pd.DataFrame([{'theta': 'N', 'z': 0}]), '')


    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div([
        html.H1('MEO Previ'),
        html.Div([ 
            html.H2('Options'),
            html.Div([
                html.Div([
                    html.H3('Add new satellite'),
                    dcc.Input(id='new_sat_name', type='text', placeholder='Satelitte name'), 
                    dcc.Input(id='new_sat_id', type='text', placeholder='Satelitte ID'),
                    html.Button('Add', id='add_button')]),
                html.Div([
                    html.H3('Remove satellite'),
                    dcc.Dropdown(id='rem_sat_name', multi=True, placeholder='Satelitte name',
                        options=[{'label': sat, 'value': satid} for satid, sat in sats.items()]), 
                    html.Button('Remove', id='remove_button')])
                ]),
            html.Div([html.H3('Controls'),
                html.Button('Refresh', id='refresh_button'),
                html.Button('Update local database', id='update_local_button')]),
            html.Div([html.H3('Dataset'),
                dcc.Dropdown(
                multi=True, disabled=False,
                options=[
                    {'label': dataset[:-5], 'value': dataset}
                        for dataset in os.listdir(path+'data/')], 
                        value='ILRS_Satellites.data', id='dataset_dropdown'),
                dcc.Input(id='save_input', type='text', placeholder='Dataset name'), 
                html.Button('Save current Dataset', id="save_btn")])
            ], id='option_div'),
        html.Div([
            html.H2('Timeline'),
            html.Div([
                dcc.Graph(figure=fig, id='timeline', className='inb'), 
                dcc.Graph(figure=polar, className='inb', id='polar')], 
                id='div_graph')
            ]),
        dcc.Interval(
            id='interval-component',
            interval=5*60*1000, # 5min (in milliseconds)
            n_intervals=0)
       ])
    
    @app.callback(
            dash.dependencies.Output('save_input', 'value'),
            dash.dependencies.Output('dataset_dropdown', 'options'),
            dash.dependencies.Input('save_btn', 'n_clicks'),
            dash.dependencies.State('save_input', 'value'),
            dash.dependencies.State('dataset_dropdown', 'options')
            )
    def save(n, filename, opt):
        if n == None or n == 0:
            raise dash.exceptions.PreventUpdate
        
        if filename == '':
            filename = 'unamed'

        if filename[-5:] == '.data':
            filename = filename[:-5]

        with open(path+'data/'+filename+'.data', 'w') as f:
            for satid in sats:
                f.write(sats[satid]+'~'+satid+'\n')
            f.close()
        return '', opt + [{'label': filename, 'value': filename+'.data'}]

    @app.callback(
            dash.dependencies.Output('new_sat_name', 'value'),
            dash.dependencies.Output('new_sat_id', 'value'),
            dash.dependencies.Input('add_button', 'n_clicks'))
    def clear_add_btn(_):
        return '', ''


    @app.callback(
            dash.dependencies.Output('rem_sat_name', 'value'),
            dash.dependencies.Input('remove_button', 'n_clicks'))
    def clear_rem_btn(_):
        return ''


    @app.callback(
        dash.dependencies.Output('timeline', 'figure'),
        [dash.dependencies.Input('refresh_button', 'n_clicks')],
        [dash.dependencies.Input('add_button', 'n_clicks')],
        [dash.dependencies.Input('remove_button', 'n_clicks')],
        [dash.dependencies.Input('update_local_button', 'n_clicks')],
        [dash.dependencies.Input('dataset_dropdown', 'value')],
        [dash.dependencies.Input('interval-component', 'n_intervals')],
        [dash.dependencies.State('new_sat_name', 'value')],
        [dash.dependencies.State('new_sat_id', 'value')],
        [dash.dependencies.State('rem_sat_name', 'value')])
    def update_output(n_ref, n_add, n_rem, n_upd_loc, dataset, n_inter, add_sat, add_satid, l_rem_sat):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate
        
        btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
        global df
        global range_x
        global sats

        if btn_id == 'add_button':
            #add new satellite to the figure, update time, but keep the range_x
            sats.update({add_satid: add_sat})
            df = df.append(previ(add_sat, add_satid))
            figure, range_x = get_figure(df, range_x=range_x)
        
        elif btn_id == 'remove_button':
            #add new satellite to the figure, update time, but keep the range_x
            for satid in l_rem_sat:
                try:
                    df = df.loc[df['Sat'] != sats[satid]]
                    del sats[satid]
                except KeyError:
                    print("Unable to remove. "+sats[satid]+" not found in dataset.")

            figure, range_x = get_figure(df, range_x=range_x)

        elif btn_id == 'refresh_button':
            #update time and range_x 
            figure, range_x = get_figure(df)

        elif btn_id == 'update_local_button':
            #redownload every sats tpm file in the database
            tmpfiles = [file for file in os.listdir(path+'tmp') 
                             if file[0] =='.' and file[-4:] == '.tmp']
            for file in tmpfiles:
                os.remove(path+'tmp/'+file)
            df = get_df(sats)
            figure, range_x = get_figure(df, range_x=range_x)
        
        elif btn_id == 'dataset_dropdown':
            sats = get_sats(dataset)
            df = get_df(sats)
            figure, range_x = get_figure(df, range_x=range_x)
        
        else: #btn_id == 'interval-component'
            #update time only every 5min
            figure, range_x = get_figure(df, range_x=range_x)

        return figure

    
    @app.callback(
            dash.dependencies.Output('polar', 'figure'),
            dash.dependencies.Input('timeline', 'clickData'))
    def update_polar(clickData):
        if clickData is None:
            raise dash.exceptions.PreventUpdate
        print(clickData['points'][0])
        return get_polar(pd.DataFrame(clickData['points'][0]['customdata'][0]), clickData['points'][0]['y'])

    #os.system("sleep 2; xdg-open http://127.0.0.1:8050/")
    app.run_server(debug=True)

