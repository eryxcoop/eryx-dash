# Install

Install by running the following command:

`$ pip install git+https://github.com/eryxcoop/eryx-dash#egg=eryx_dash`

# Create a simple report

### Read data
First read your dataset and put it on a pandas DataFrame:

```
df_sales = pd.DataFrame({
    'Instrument': ['Guitar', 'Keyboard', 'Guitar', 'Saxophone', 'Bass'],
    'Price': [200, 450, 350, 500, 250]
})

data_sources = DataSources(dictionary={
    'sales': df_sales,
})
```

### Define metrics
Define the metrics you have to compute, you can use anything on your data source:

```
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
```

### Define structure
Define your filters, charts and their position. You have to use the Bootstrap grid system:

```
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
```

### Create your app
Create your Dash app and run it. All the callbacks and styles are generated automatically.

```
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
```

# More examples
A folder with a more complete example can be found in the repository.