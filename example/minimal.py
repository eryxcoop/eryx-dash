import dash_bootstrap_components as dbc
import pandas as pd
import metrics
from dash import Dash
from eryx_dash.metrics import MoneyMetric, IntegerMetric

from eryx_dash.components import EryxTab, BarChart, PlaceHolder
from eryx_dash.components import EryxRow as Row
from eryx_dash.components import EryxCol as Col
from eryx_dash.components import ChecklistFilter, Card
from eryx_dash.data_sources import DataSources


df_sales = pd.DataFrame({
    'Instrument': ['Guitar', 'Keyboard', 'Guitar', 'Saxophone', 'Bass'],
    'Price': [200, 450, 350, 500, 250]
})

data_sources = DataSources(dictionary={
    'sales': df_sales,
})


class Sales(MoneyMetric):
    def name(self):
        return 'Sales'

    def compute(self, data_sources):
        return data_sources.get('sales')['Price'].sum()


class Units(IntegerMetric):
    def name(self):
        return 'Sales'

    def compute(self, data_sources):
        return data_sources.get('sales').shape[0]


tab = EryxTab([Row([
    Col([
        Row([
            Col([ChecklistFilter(title='Instrument', filters=[("sales", "Instrument")])]),
        ])
    ], width=2),
    Col([
        Row([
            Col([Card(title="Units", metric=Units())], width=2),
            Col([Card(title="Sales", metric=Sales())], width=2),
            Col([PlaceHolder(100)], width=8),
            Col([BarChart('sales', 'Instrument', Sales(), title='Sales by Instrument', format='money')], width=4),
        ])
    ], width=10),
])], data_sources=data_sources)


app = Dash(external_stylesheets=[dbc.themes.DARKLY])
app.title = 'Dashboard | Sales'

tab.add_to_dash_app(app)

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col(dbc.Tabs([
            dbc.Tab(tab.dash_component(tab.data_sources), label="Report"),
        ]))], no_gutters=True),
    fluid=True)

app.run_server(debug=True)
