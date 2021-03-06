
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# icustay_id
app = dash.Dash(__name__)
server = app.server

## umap csv
df = pd.read_csv('umap_appended.csv')

## tsne csv
df_2 = pd.read_csv('tsne_appended.csv')

## Split into dataframes based on labels (umap)
df_umap_1 = df.loc[df['labels'] == 0]
df_umap_2 = df.loc[df['labels'] == 1]
df_umap_3 = df.loc[df['labels'] == 2]
df_umap_1_describe = df_umap_1.describe()
df_umap_2_describe = df_umap_2.describe()
df_umap_3_describe = df_umap_3.describe()

## umap initial plot
fig_2d = px.scatter(
    df, x='umap_0', y='umap_1',
    color=df['labels'], labels={'color': df['labels']},
    hover_data=['icustay_id']
)

## tsne initial plot
fig_tsne = px.scatter(
    df_2, x='tsne_0', y='tsne_1',
    color=df_2['labels'], labels={'color': df_2['labels']},
    hover_data=['icustay_id']
)

def find_mean_median(df, features):
    mean_df = df.loc[['mean'], df.columns.to_series().str.contains(features)]
    median_df = df.loc[['50%'], df.columns.to_series().str.contains(features)]
    mean_Transpose = mean_df.transpose()
    median_Transpose = median_df.transpose()
    mean_median_Transpose = pd.merge(mean_Transpose, median_Transpose, left_index=True, right_index=True)
    mean_median_Transpose.columns = ['mean', 'median']
    return mean_median_Transpose

def plot_feature_label(features, label1, label2, label3, y_label, stat='mean'):
    mean_median_1 = find_mean_median(label1, features)
    mean_median_2 = find_mean_median(label2, features)
    mean_median_3 = find_mean_median(label3, features)
    ## plot mean for different labels
    if stat == 'mean':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=mean_median_1.index, y=mean_median_1['mean'], name=label1, line=dict(color='firebrick', width=2)))
        fig.add_trace(go.Scatter(x=mean_median_2.index, y=mean_median_2['mean'], name=label2, line=dict(color='royalblue', width=2)))
        fig.add_trace(go.Scatter(x=mean_median_3.index, y=mean_median_3['mean'], name=label3, line=dict(color='green', width=2)))
        fig.update_layout(xaxis_title='Time', yaxis_title=y_label, title=y_label+'_mean')
    
    ## plot median for different labels
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=mean_median_1.index, y=mean_median_1['median'], name=label1, line=dict(color='firebrick', width=2)))
        fig.add_trace(go.Scatter(x=mean_median_2.index, y=mean_median_2['median'], name=label2, line=dict(color='royalblue', width=2)))
        fig.add_trace(go.Scatter(x=mean_median_3.index, y=mean_median_3['median'], name=label3, line=dict(color='green', width=2)))
        fig.update_layout(xaxis_title='Time', yaxis_title=y_label, title=y_label+'_median')
    
    return fig


## Bootstrap template
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]) 


index_page = html.Div([
    dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("UMAP analysis", href="/page-1")),
        dbc.NavItem(dbc.NavLink("TSNE analysis", href="/page-2")),
    ],
    brand="MIMIC Visualization",
    brand_href="/",
    color="primary",
    dark=True,),

    dbc.Container([

        dbc.Col([

            dbc.Row([html.H5(children = "UMAP plots", style={'text-align': 'center'}),]),

            dbc.Row([
            html.Div([
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                figure = fig_2d,
                hoverData={'points': [{'customdata': [200001]}]}
            )])]),

            dbc.Row([html.H5(children = "TSNE plots", style={'text-align': 'center'}),]),

            dbc.Row([
            html.Div([
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                figure = fig_tsne,
                hoverData={'points': [{'customdata': [200001]}]}
            )])]),
            
        
        ], width= 6, sm = 12, md = 12, lg = 6, xl = 6),

        
        
        dbc.Col([

            dbc.Row([
                html.H5(children = "Updates", style={'text-align': 'center'}),

                html.p(children="(14 Feb: Updated UMAP and TSNE plots)")
             ]),
            
        
        ], width= 6, sm = 12, md = 12, lg = 6, xl = 6),

    ]),
])

app.layout = dbc.Container([

    html.Br(),
    
    dbc.Row([html.H1(children='UMAP label analysis', style={'textAlign': 'center'})], style={'padding': '10px'}),

    dbc.Row
    ([
         dbc.Col([
            
            dbc.Row([

                html.H5('Mean', style={'textAlign': 'center'}),

                html.Div([dcc.Graph(figure = plot_feature_label('heart_rate', df_umap_1, df_umap_2, df_umap_3, 'heart_rate', 'mean'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),

            dbc.Row([

                
                html.Div([dcc.Graph(figure = plot_feature_label('respiratory_rate', df_umap_1, df_umap_2, df_umap_3, 'respiratory rate', 'mean'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),

            dbc.Row([

                
                html.Div([dcc.Graph(figure = plot_feature_label('hematocrit', df_umap_1, df_umap_2, df_umap_3, 'hematocrit', 'mean'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),

            dbc.Row([

                
                html.Div([dcc.Graph(figure = plot_feature_label('fraction_inspired_oxygen', df_umap_1, df_umap_2, df_umap_3, 'fraction inspired oxygen', 'mean'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),

            dbc.Row([

                
                html.Div([dcc.Graph(figure = plot_feature_label('creatinine', df_umap_1, df_umap_2, df_umap_3, 'creatinine', 'mean'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),

            dbc.Row([

                
                html.Div([dcc.Graph(figure = plot_feature_label('mean_blood_pressure', df_umap_1, df_umap_2, df_umap_3, 'mean blood pressure', 'mean'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),

            dbc.Row([

                
                html.Div([dcc.Graph(figure = plot_feature_label('sodium', df_umap_1, df_umap_2, df_umap_3, 'sodium', 'mean'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),
        ],width=6, sm=6, md=6, lg=6),
        
        
        dbc.Col([
            
            dbc.Row([

                html.H5('Median', style={'textAlign': 'center'}),

                html.Div([dcc.Graph(figure = plot_feature_label('heart_rate', df_umap_1, df_umap_2, df_umap_3, 'heart_rate', 'median'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),

            dbc.Row([

                
                html.Div([dcc.Graph(figure = plot_feature_label('respiratory_rate', df_umap_1, df_umap_2, df_umap_3, 'respiratory rate', 'median'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),

            dbc.Row([

                
                html.Div([dcc.Graph(figure = plot_feature_label('hematocrit', df_umap_1, df_umap_2, df_umap_3, 'hematocrit', 'median'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),

            dbc.Row([

                
                html.Div([dcc.Graph(figure = plot_feature_label('fraction_inspired_oxygen', df_umap_1, df_umap_2, df_umap_3, 'fraction inspired oxygen', 'median'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),

            dbc.Row([

                
                html.Div([dcc.Graph(figure = plot_feature_label('creatinine', df_umap_1, df_umap_2, df_umap_3, 'creatinine', 'median'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),

            dbc.Row([

                
                html.Div([dcc.Graph(figure = plot_feature_label('mean_blood_pressure', df_umap_1, df_umap_2, df_umap_3, 'mean blood pressure', 'median'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),

            dbc.Row([

                
                html.Div([dcc.Graph(figure = plot_feature_label('sodium', df_umap_1, df_umap_2, df_umap_3, 'sodium', 'median'))],
                style={'width': '100%', 'display': 'inline-block'})
            ]),
        ],width=6, sm=6, md=6, lg=6),
    ]),

])

if __name__ == '__main__':
    app.run_server(debug=True)