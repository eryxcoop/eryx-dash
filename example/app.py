import dash_bootstrap_components as dbc
import pandas as pd
import metrics
from dash import Dash
from eryx_dash.components import EryxTab, HorizontalBarChart, PieChart, LineChart, TreeMapChart, BarLineChart, \
    ChecklistFilter, BarChart
from eryx_dash.components import EryxRow as Row
from eryx_dash.components import EryxCol as Col
from eryx_dash.components import DropdownFilter, Card
from eryx_dash.data_sources import DataSources

app = Dash(external_stylesheets=[dbc.themes.DARKLY])
app.title = 'Dashboard | Sales'

df_sales = pd.read_csv("supermarket_sales.csv")
df_sales['Timestamp'] = pd.to_datetime(df_sales['Date'] + ' ' + df_sales['Time'], format='%m/%d/%Y %H:%M')
df_sales['Date'] = pd.to_datetime(df_sales['Date'], format='%m/%d/%Y')
df_sales['Year_Month'] = df_sales['Timestamp'].dt.month.astype(str) + '-' + df_sales['Timestamp'].dt.year.astype(str)
df_sales['Hour'] = df_sales['Timestamp'].dt.hour
df_sales['Day'] = df_sales['Timestamp'].dt.day
df_sales['DayOfWeek'] = df_sales['Timestamp'].dt.day_name()

data_sources = DataSources(dictionary={
    'sales': df_sales,
})

height = 350

monthly_tab = EryxTab([Row([
    Col([
        Row([
            Col([DropdownFilter(title='Month', filters=[("sales", "Year_Month")])]),
            Col([ChecklistFilter(title='City', filters=[("sales", "City")])]),
            Col([ChecklistFilter(title='Branch', filters=[("sales", "Branch")])]),
            Col([ChecklistFilter(title='Product line', filters=[("sales", "Product line")])]),
            Col([ChecklistFilter(title='Customer type', filters=[("sales", "Customer type")])]),
            Col([ChecklistFilter(title='Gender', filters=[("sales", "Gender")])]),
            Col([ChecklistFilter(title='Payment', filters=[("sales", "Payment")])]),
            Col([PieChart('sales', 'Customer type', metrics.Sales(), height=181, title='Sales by payment')], width=12),
        ])
    ], width=2),
    Col([
        Row([
            Col([Card(title="Invoices", metric=metrics.Invoices())], width=2),
            Col([Card(title="Sales", metric=metrics.Sales())], width=2),
            Col([Card(title="Income per purchase", metric=metrics.IncomePerPurchase())], width=2),
            Col([Card(title="Units", metric=metrics.Units())], width=2),
            Col([Card(title="Units per purchase", metric=metrics.UnitsPerPurchase())], width=2),
            Col([Card(title="Rating", metric=metrics.Rating())], width=2),

            Col([LineChart('sales', 'Date', metrics.Sales(), skip_ticks=3, title='Sales by date')], width=8),
            Col([TreeMapChart('sales', 'City', 'Total', title='Sales by city')], width=4),
            Col([BarLineChart('sales', 'Product line', metrics.Sales(), metrics.PercentMembers(), height=height, title='Sales by category')], width=4),
            Col([HorizontalBarChart('sales', 'Payment', metrics.IncomePerPurchase(), top_n=10, height=height, title='Average purchase by payment')], width=4),
            Col([BarChart('sales', 'DayOfWeek', metrics.Sales(), height=height, title='Sales by day of week', format='money')], width=4),
        ])
    ], width=10),
])], data_sources=data_sources)

monthly_tab.add_to_dash_app(app)

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col(dbc.Tabs([
            dbc.Tab(monthly_tab.dash_component(monthly_tab.data_sources), label="Montly"),
        ]))], no_gutters=True),
    fluid=True)

app.run_server(debug=True)
