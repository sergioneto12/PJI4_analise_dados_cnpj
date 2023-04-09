"""
Front end of project Analysis

Created By: PJI04 - Turma 001
Revised by: Sergio Neto, Anderson Santiago.
"""

import base64
import json
import logging
import os
import traceback

import numpy as np
import pandas as pd
import pandas_gbq as pg
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dash_table, dcc, html
from dotenv import load_dotenv
from google.oauth2 import service_account

# environment variables loading
load_dotenv()

logger = logging.getLogger()
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# starting app
app = Dash(__name__)

sql_no_com = """
    select 
        date(dt_inicio_ativ) as dt_inicio_ativ, 
        date(dt_sit_cadastral) as dt_sit_cadastral, 
        count(cnpj_basico) as CNPJs,
        sum(capital_social) as capital_social,
        round(avg(capital_social),2) as med_capital_social,
        sit_cadastral,
        month, 
        year,
        UF,
        natureza_juridica,
        
    from `civic-athlete-325820.pji4.dataset_analysis`

    where extract(year from dt_inicio_ativ) between 2018 and 2023

    group by 1, 2, 6, 7, 8, 9, 10
    order by 1 desc
"""

def get_data():
    """
    This functions makes requistion of data to feed the dashboard.

    - Parameters:
    (String) The entrance is done by a single sql statement, that can be used at the dashboard by any analysis necessary.

    For any 
    """

    try:
        print('Running')

        credentials = service_account.Credentials.from_service_account_info(json.loads(base64.b64decode(os.environ.get('CRED'))))
        df = pg.read_gbq(sql_no_com, project_id="civic-athlete-325820", credentials=credentials)

        df = df.rename(columns={
            'dt_inicio_ativ': 'Data De Início da Atividade', 
            'dt_sit_cadastral': 'Data Da Ult. Situação Cadastral', 
            'CNPJs': 'CNPJs',
            'capital_social': 'Capital Total',
            'med_capital_social': 'Média do Capital Registrado',
            'sit_cadastral': 'Situação Cadastral',
            'month': 'Mês', 
            'year': 'Ano',
            'UF': 'Estado',
            'natureza_juridica': 'Natureza Juridica',
        })

        print('Query done')
        
        return df

    except Exception as e:
        print(e)
        print(traceback.format_exc())

def application():
    """
    This application initializes the main dashboard page

    The dashboard is produced by dash library o python, starting from the dataframe generated by the function 'get_data'

    In order to maintain this code, be sure all HTML components will be placed inside the app.layout variable
    A new div element can be created below after the last component, adding a new row to contain a new chart.

    Charts can be manipulated before app.layout to keep a code pattern inside the app structure
    """

    # Generating our dataframe
    df_main = get_data()

    # Both variables are set up to be stored at the charts created below in figure variables.
    v_2023 = df_main['CNPJs'].loc[pd.to_datetime(df_main['Data De Início da Atividade']).dt.year < 2020].count()
    v_2022 = df_main['CNPJs'].loc[(pd.to_datetime(df_main['Data De Início da Atividade']).dt.year > 2019) & (pd.to_datetime(df_main['Data De Início da Atividade']).dt.year < 2022)].count()

    df_nat = df_main.groupby(['Natureza Juridica']).sum(['CNPJs']).sort_values(by='CNPJs', ascending=False).head(5)
    # print(df_nat.index)

    # First KPI view
    fig1 = go.Figure(
            go.Indicator(
                mode = "number",
                value = v_2023,
                number = {'prefix': "#"},
                domain = {'x': [0, 1], 'y': [0, 1]},
            )   
        )

    # Second KPI view
    fig2 = go.Figure(
            go.Indicator(
                mode = "number",
                value = v_2022,
                number = {'prefix': "#"},
                domain = {'x': [0, 1], 'y': [0, 1]},   
            )
        )

    # layout of KPIs background
    fig1.update_layout(paper_bgcolor = "LightSteelBlue", width=400, height=250)
    fig2.update_layout(paper_bgcolor = "LightSteelBlue", width=400, height=250)

    # This variable starts the application design, mainly using HTML keywords
    app.layout = html.Div([

        # Top chart (bar chart) set up
        html.Div([
            html.Div(
                children='Dados Abertos: Cadastro de Empresas no Brasil: 2018 - 2023', 
                style={
                    'font-family': 'Roboto', 
                    'font-size': 40, 
                    'textAlign': 'center', 
                    'align-items': 'center', 
                    'justify-content': 'center', 
                    'font-weight': 'bold', 
                    'display': 'flex', 
                    'flex-direction': 'row'
                    }
                ),
            html.Hr(),
            html.Div(
                [
                    html.Div([
                        dcc.Graph(
                            figure=px.histogram(df_main, x='Ano', y='CNPJs', histfunc='count', text_auto=True).update_layout(paper_bgcolor = "LightSteelBlue", width=600, height=400, yaxis_title='Nº de Empresas')),
                    ], style={'margin': 15}),
                    html.Div([
                        dcc.Graph(figure=px.bar(df_nat, y=df_nat.index, x='CNPJs', orientation='h', text='CNPJs').update_layout(paper_bgcolor = "LightSteelBlue", width=600, height=400), id='my-bar-2'),       
                    ], style={'margin': 15}
                    )
                ], 
                style={
                    'padding': 0, 
                    'margin': 15, 
                    'text-align': 'center', 
                    'align-items': 'center', 
                    'justify-content': 'center', 
                    'font-weight': 'bold', 
                    'display': 'flex', 
                    'flex-direction': 'row'
                }
            ),
        ], 
        style={
            'margin': 15, 
            'textAlign': 'center', 
            'align-items': 'center', 
            'justify-content': 'center','margin-bottom': 50
            }
        ),

        html.Div([
            # KPIs set up
            html.Div([    
                html.Div(children='Número de empresas criadas entre 2018 e 2019'),
                html.Hr(),
                html.Div([
                    dcc.Graph(figure=fig1, id='my-graph-2')], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'font-weight': 'bold'})
            ], 
            style={
                'margin': 20, 
                'font-family': 'Roboto', 
                'font-size': 25, 
                'font-weight': 'bold', 
                'align-items': 'center', 
                'text-align': 'center'
                }
            ),

            html.Div([    
                html.Div(children='Número de empresas criadas entre 2020 e 2021'),
                html.Hr(),
                html.Div(
                    [
                        dcc.Graph(figure=fig2, id='my-graph-3')
                    ], 
                    style={
                        'display': 'flex', 
                        'align-items': 'center', 
                        'justify-content': 'center', 
                        'font-weight': 'bold'
                        }
                    )
            ], 
            style={
                'margin': 20, 
                'font-family': 'Roboto', 
                'font-size': 25, 
                'font-weight': 'bold', 
                'align-items': 'center', 
                'text-align': 'center'
                }
            ),

        ], 
        style={
            'margin': 20, 
            'display': 'flex', 
            'flex-direction': 'row', 
            'justify-content': 'center'
            }
        ),

        html.Div([
            html.Div(
                children='Tabela Geral de Dados', 
                style={
                    'font-family': 'Roboto', 
                    'font-size': 40, 
                    'textAlign': 'center', 
                    'align-items': 'center', 
                    'justify-content': 'center', 
                    'font-weight': 'bold', 
                    'display': 'flex', 
                    'flex-direction': 'row'
                    }
                ),
            html.Hr(),
            dash_table.DataTable(data=df_main.to_dict('records'), page_size=10),
        ], 
        style={
            'margin': 15, 
            'textAlign': 'center', 
            'align-items': 'center', 
            'justify-content': 'center', 
            'margin': 30
            }
        ),        
    ], style={'background': '#e8f0fa'})

    # Return the app run server, starting automatically the application as the function is triggered
    return app.run_server(debug=True) #app.run_server(debug=False, host="0.0.0.0", port=8080)

if __name__ == '__main__':
    application()