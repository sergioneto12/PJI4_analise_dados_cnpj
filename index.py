"""
Front end of project Analysis

Created By: PJI04 - Turma 001
Revised by: Sergio Neto, Anderson Santiago.
"""

import pandas_gbq as pg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, html, dcc, dash_table
from dash import html

from google.oauth2 import service_account
import json
import os
import base64
import logging

from dotenv import load_dotenv

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
        avg(capital_social) as med_capital_social,
        sit_cadastral,
        month, 
        year,
        
    from `civic-athlete-325820.pji4.dataset_analysis`

    where extract(year from dt_inicio_ativ) between 2018 and 2023

    group by 1, 2, 6, 7, 8
    order by 1 desc
"""

def get_data(sql_statement: str):
    """
    This functions makes requistion of data to feed the dashboard.

    - Parameters:
    (String) The entrance is done by a single sql statement, that can be used at the dashboard by any analysis necessary.

    For any 
    """

    try:
        credentials = service_account.Credentials.from_service_account_info(json.loads(base64.b64decode(os.environ.get('CRED'))))
        df = pg.read_gbq(sql_statement, project_id="civic-athlete-325820", credentials=credentials)
       
        return df
    
    except Exception as e:
        print(e)


def application():
    df_main = get_data(sql_no_com)

    v = df_main['CNPJs'].loc[pd.to_datetime(df_main['dt_inicio_ativ']).dt.year == 2023].sum()

    fig1 = go.Figure(
            go.Indicator(
                mode = "number",
                value = v,
                number = {'prefix': "#"},
                delta = {'position': "top", 'reference': 320},
                domain = {'x': [0, 1], 'y': [0, 1]}
            )
        )

    fig1.update_layout(paper_bgcolor = "lightgray")

    app.layout = html.Div([
        html.Div([
            html.Div(children='Dados Abertos: Cadastro de Empresas no Brasil: 2018 - 2023', style={'font-size': 40, 'textAlign': 'center', 'align-items': 'center', 'justify-content': 'center', 'font-weight': 'bold', 'display': 'flex', 'flex-direction': 'row'}),
            html.Hr(),
            # dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='my-radio-item'),
            # dash_table.DataTable(data=df.to_dict('records'), page_size=10),
            dcc.Graph(figure=px.histogram(df_main, x='year', y='CNPJs', histfunc='sum', labels=''), id='my-graph-1'),
            # dcc.Graph(figure=fig, id='my-graph-2')
        ]),

        html.Div([
            html.Div([    
                html.Div(children='Número de empresas em 2023', style={'font-size': 40, 'textAlign': 'center', 'align-items': 'center', 'justify-content': 'center', 'font-weight': 'bold', 'display': 'flex', 'flex-direction': 'row'}),
                html.Hr(),
                html.Div([
                    dcc.Graph(figure=fig1, id='my-graph-2')])
            ]),

            html.Div([    
                html.Div(children='Número de empresas em 2023', style={'font-size': 40, 'textAlign': 'center', 'align-items': 'center', 'justify-content': 'center', 'font-weight': 'bold', 'display': 'flex', 'flex-direction': 'row'}),
                html.Hr(),
                html.Div([
                    dcc.Graph(figure=fig1, id='my-graph-3')])
            ])
        ])
        
    ])

    return app.run_server(debug=True)

if __name__ == '__main__':
    application()