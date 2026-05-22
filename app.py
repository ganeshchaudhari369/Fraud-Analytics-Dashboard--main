import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize the Dash app with a clean light theme
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
server = app.server

# ----------------------------------------------------------------------------------
# Data Loading & Preprocessing
# ----------------------------------------------------------------------------------
def load_data():
    df = pd.read_csv('fraud.csv')
    df['transaction_amount'] = df['transaction_amount'].fillna(df['transaction_amount'].median())
    df['Fraud_Status'] = df['is_fraud'].map({1: 'Fraud', 0: 'Legitimate'})
    df_fraud = df[df['is_fraud'] == 1].sort_values('transaction_amount', ascending=False)
    return df, df_fraud

df, df_fraud_top = load_data()

# ----------------------------------------------------------------------------------
# UI Components
# ----------------------------------------------------------------------------------

def create_kpi_card(title, value, icon, color="primary"):
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.I(className=f"fas {icon} fa-2x text-{color}")
                ], width=3),
                dbc.Col([
                    html.H6(title, className="card-title text-uppercase mb-0 fw-bold", style={"color": "#000000"}),
                    html.H3(value, className=f"fw-bold mb-0 text-{color}"),
                ], width=9)
            ], align="center")
        ])
    ], className="mb-4 shadow-sm border-0 bg-white rounded-3")

# ----------------------------------------------------------------------------------
# Sidebar Design (Light Sidebar)
# ----------------------------------------------------------------------------------
sidebar = html.Div(
    [
        html.H2("FRAUD AI", className="display-4 text-primary text-center py-4 fw-bold"),
        html.Hr(),
        html.P("Managerial Insights & Risk Assessment", className="lead text-center text-dark fw-bold"),
        html.Br(),
        dbc.Nav(
            [
                html.Label("Filter by Store Type", className="text-dark fw-bold mt-3"),
                dcc.Dropdown(
                    id='category-filter',
                    options=[{'label': str(c), 'value': c} for c in sorted(df['store_type'].dropna().unique())],
                    multi=True,
                    placeholder="All Store Types",
                    className="mb-4"
                ),
                html.Label("Hour of Day Window", className="text-dark fw-bold mt-3"),
                dcc.RangeSlider(
                    id='hour-slider',
                    min=0, max=23, step=1,
                    value=[0, 23],
                    marks={i: {'label': f'{i}h', 'style': {'color': 'black', 'fontWeight': 'bold'}} for i in range(0, 24, 4)},
                    className="mb-4"
                ),
            ],
            vertical=True,
            pills=True,
        ),
        html.Div([
            html.P("© 2026 Antigravity Analytics", className="text-muted small")
        ], style={"position": "absolute", "bottom": "20px", "left": "20px"})
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "20rem",
        "padding": "2rem 1rem",
        "backgroundColor": "#f8f9fa",
        "borderRight": "1px solid #dee2e6"
    },
)

# ----------------------------------------------------------------------------------
# Content Layout
# ----------------------------------------------------------------------------------
content = html.Div(
    [
        # Header Row with High Visibility (Light Header Bar)
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H1("REAL-TIME FRAUD ANALYTICS CONSOLE", 
                            className="fw-bold mb-0 text-black"),
                    html.P("Operational Intelligence & Risk Monitoring", 
                           className="text-muted mb-0", 
                           style={"fontSize": "1.1rem", "fontWeight": "700", "color": "#000000"})
                ], className="bg-white p-4 rounded-3 shadow-sm border-start border-primary border-5"), 
                width=12
            )
        ], className="mb-5"),

        # KPI Row
        dbc.Row([
            dbc.Col(id='kpi-total-transactions', width={"size": 3}),
            dbc.Col(id='kpi-fraud-cases', width={"size": 3}),
            dbc.Col(id='kpi-fraud-rate', width={"size": 3}),
            dbc.Col(id='kpi-potential-loss', width={"size": 3}),
        ]),

        # Charts Row 1
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id='hourly-trend-chart'), className="p-3 bg-white border-0 shadow-sm"), width=8),
            dbc.Col(dbc.Card(dcc.Graph(id='category-risk-chart'), className="p-3 bg-white border-0 shadow-sm"), width=4),
        ], className="mb-4"),

        # Charts Row 2 & Table
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id='amount-dist-chart'), className="p-3 bg-white border-0 shadow-sm"), width=4),
            dbc.Col(dbc.Card(dcc.Graph(id='distance-risk-chart'), className="p-3 bg-white border-0 shadow-sm"), width=4),
            dbc.Col(dbc.Card([
                html.H5("Top High-Value Fraud Cases", className="fw-bold text-black mb-3"),
                dash_table.DataTable(
                    id='fraud-table',
                    columns=[
                        {"name": "Amount", "id": "transaction_amount"},
                        {"name": "Store", "id": "store_type"},
                        {"name": "Distance", "id": "distance_from_home"}
                    ],
                    data=df_fraud_top.head(10).to_dict('records'),
                    style_header={'backgroundColor': '#f8f9fa', 'color': 'black', 'fontWeight': 'bold'},
                    style_cell={'backgroundColor': 'white', 'color': 'black', 'textAlign': 'left'},
                    page_size=5,
                )
            ], className="p-3 bg-white border-0 shadow-sm"), width=4),
        ]),
    ],
    style={"marginLeft": "22rem", "marginRight": "2rem", "marginTop": "2rem"},
)

app.layout = html.Div([sidebar, content], style={"backgroundColor": "#f4f7f6", "minHeight": "100vh"})

# ----------------------------------------------------------------------------------
# Callbacks
# ----------------------------------------------------------------------------------

@app.callback(
    [Output('kpi-total-transactions', 'children'),
     Output('kpi-fraud-cases', 'children'),
     Output('kpi-fraud-rate', 'children'),
     Output('kpi-potential-loss', 'children'),
     Output('hourly-trend-chart', 'figure'),
     Output('category-risk-chart', 'figure'),
     Output('amount-dist-chart', 'figure'),
     Output('distance-risk-chart', 'figure')],
    [Input('category-filter', 'value'),
     Input('hour-slider', 'value')]
)
def update_dashboard(selected_categories, hour_range):
    dff = df[(df['hour_of_day'] >= hour_range[0]) & (df['hour_of_day'] <= hour_range[1])]
    if selected_categories:
        dff = dff[dff['store_type'].isin(selected_categories)]

    # KPIs
    total_tx = len(dff)
    fraud_cases = dff['is_fraud'].sum()
    fraud_rate = (fraud_cases / total_tx * 100) if total_tx > 0 else 0
    potential_loss = dff[dff['is_fraud'] == 1]['transaction_amount'].sum()

    kpi_1 = create_kpi_card("Total Volume", f"{total_tx:,}", "fa-exchange-alt", "primary")
    kpi_2 = create_kpi_card("Fraud Detected", f"{fraud_cases:,}", "fa-user-shield", "danger")
    kpi_3 = create_kpi_card("Risk Probability", f"{fraud_rate:.2f}%", "fa-percent", "warning")
    kpi_4 = create_kpi_card("Exposure (USD)", f"${potential_loss:,.0f}", "fa-dollar-sign", "danger")

    # Layout common styling
    chart_layout = dict(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black', weight='bold'),
        title=dict(font=dict(color='black', size=18, weight='bold'))
    )

    # Hourly Trend
    hourly_data = dff.groupby(['hour_of_day', 'Fraud_Status']).size().reset_index(name='Count')
    fig_hourly = px.line(hourly_data, x='hour_of_day', y='Count', color='Fraud_Status',
                         title='Intraday Transaction Volume',
                         template='plotly_white',
                         color_discrete_map={'Fraud': '#e74c3c', 'Legitimate': '#2980b9'})
    fig_hourly.update_layout(**chart_layout)

    # Store Risk
    cat_fraud = dff[dff['is_fraud'] == 1].groupby('store_type').size().reset_index(name='Fraud_Count')
    cat_fraud = cat_fraud.sort_values('Fraud_Count', ascending=True)
    fig_cat = px.bar(cat_fraud, y='store_type', x='Fraud_Count', orientation='h',
                     title='High-Risk Store Types',
                     template='plotly_white')
    fig_cat.update_traces(marker_color='#e74c3c')
    fig_cat.update_layout(**chart_layout)

    # Amount Distribution
    fig_amount = px.violin(dff, x='Fraud_Status', y='transaction_amount', color='Fraud_Status',
                         title='Value Distribution Analysis',
                         template='plotly_white',
                         color_discrete_map={'Fraud': '#e74c3c', 'Legitimate': '#2980b9'})
    fig_amount.update_layout(showlegend=False, **chart_layout)

    # Distance Risk
    fig_dist = px.histogram(dff, x='distance_from_home', color='Fraud_Status', barmode='overlay',
                              title='Geographic Risk Profile',
                              template='plotly_white',
                              color_discrete_map={'Fraud': '#e74c3c', 'Legitimate': '#2980b9'})
    fig_dist.update_layout(**chart_layout)

    return kpi_1, kpi_2, kpi_3, kpi_4, fig_hourly, fig_cat, fig_amount, fig_dist

if __name__ == '__main__':
    print("Professional Light Mode Dashboard starting on http://0.0.0.0:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)

