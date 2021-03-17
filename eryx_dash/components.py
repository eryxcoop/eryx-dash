import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Output, Input
from eryx_dash.plots import card_chart, empty_card, LoadingGraph, line_chart, dropdown_filter, hbar_chart, \
    pie_chart, treemap_chart, bar_line_chart, plotly_wordcloud, checklist_filter, bar_chart


class EryxComponent(object):
    def get_id(self):
        return self.__class__.__name__ + '-' + str(id(self))

    def is_filter(self):
        return False

    def is_chart(self):
        return False

    def get_filters(self):
        filters = [self] if self.is_filter() else []
        if hasattr(self, 'children'):
            for children in self.children:
                filters = filters + children.get_filters()
        return filters

    def get_charts(self):
        filters = [self] if self.is_chart() else []
        if hasattr(self, 'children'):
            for children in self.children:
                filters = filters + children.get_charts()
        return filters

    def dash_component(self, data_sources):
        raise Exception('Subclass responsibility')


class ChartComponent(EryxComponent):
    def is_chart(self):
        return True

    def callback(self, data_sources):
        raise Exception("Subclass responsibility")


class FilterComponent(EryxComponent):
    def is_filter(self):
        return True

    def filter(self, data_sources, filter_config):
        raise Exception("Subclass responsibility")


class EryxRow(EryxComponent):
    def __init__(self, children):
        self.children = children

    def dash_component(self, data_sources):
        return dbc.Row([c.dash_component(data_sources) for c in self.children], no_gutters=True)


class EryxCol(EryxComponent):
    def __init__(self, children, width=12):
        self.children = children
        self.width = width

    def dash_component(self, data_sources):
        return dbc.Col([c.dash_component(data_sources) for c in self.children], lg=self.width)


class PlaceHolder(EryxComponent):
    def __init__(self, height):
        self.height = height

    def dash_component(self, data_sources):
        return LoadingGraph(id=self.get_id(), height=self.height)


class DropdownFilter(FilterComponent):
    def __init__(self, title, filters):
        self.title = title
        self.filters = filters

    def is_filter(self):
        return True

    def dash_component(self, data_sources):
        return dropdown_filter(self.title, self.get_id(), data_sources.get(self.filters[0][0]), self.filters[0][1])

    def filter(self, data_sources, filter_config):
        for table, column in self.filters:
            df = data_sources.get(table)
            data_sources.set_filter(table, df[df[column] == filter_config])


class ChecklistFilter(FilterComponent):
    def __init__(self, title, filters, **kwargs):
        self.title = title
        self.filters = filters
        self.extra_args = kwargs

    def is_filter(self):
        return True

    def dash_component(self, data_sources):
        return checklist_filter(self.title, self.get_id(), data_sources.get(self.filters[0][0]), self.filters[0][1], **self.extra_args)

    def filter(self, data_sources, filter_config):
        if filter_config:
            for table, column in self.filters:
                df = data_sources.get(table)
                data_sources.set_filter(table, df[df[column].isin(filter_config)])


class Card(ChartComponent):
    def __init__(self, title, metric):
        self.title = title
        self.metric = metric

    def get_property(self):
        return 'children'

    def dash_component(self, data_sources):
        return empty_card(self.title, self.get_id())

    def callback(self, data_sources):
        return self.metric.formatted(data_sources)


class HorizontalBarChart(ChartComponent):
    def __init__(self, src, field, metric, height=None, top_n=15, percentage_of_total=False, **kwargs):
        self.data_source = src
        self.field = field
        self.metric = metric
        self.height = height
        self.top_n = top_n
        self.percentage_of_total = percentage_of_total
        self.extra_args = kwargs

    def get_property(self):
        return 'figure'

    def dash_component(self, data_sources):
        return LoadingGraph(id=self.get_id(), height=self.height)

    def callback(self, data_sources):
        def compute_group(group):
            data_sources.set_group_filter(self.data_source, group)
            metric = self.metric.compute(data_sources)
            data_sources.clear_group_filter()
            return metric

        df = data_sources.get(self.data_source)
        df = df.groupby(self.field).apply(compute_group).rename(self.metric.name())

        if self.percentage_of_total:
            df = df / df.sum()
        return hbar_chart(df.reset_index().sort_values(self.metric.name()).tail(self.top_n), self.metric.name(), self.field, height=self.height, **self.extra_args)


class BarChart(ChartComponent):
    def __init__(self, src, field, metric, height=None, top_n=15, sort_by_column=False, **kwargs):
        self.data_source = src
        self.field = field
        self.metric = metric
        self.height = height
        self.top_n = top_n
        self.sort_by_column = sort_by_column
        self.extra_args = kwargs

    def get_property(self):
        return 'figure'

    def dash_component(self, data_sources):
        return LoadingGraph(id=self.get_id(), height=self.height)

    def callback(self, data_sources):
        def compute_group(group):
            data_sources.set_group_filter(self.data_source, group)
            metric = self.metric.compute(data_sources)
            data_sources.clear_group_filter()
            return metric

        df = data_sources.get(self.data_source)
        df = df.groupby(self.field).apply(compute_group).rename(self.metric.name())
        return bar_chart(df.reset_index().sort_values(self.metric.name(), ascending=False).head(self.top_n), self.field, self.metric.name(), height=self.height, **self.extra_args)


class WordCloudChart(ChartComponent):
    def __init__(self, src, field, metric, height=None, top_n=15, **kwargs):
        self.data_source = src
        self.field = field
        self.metric = metric
        self.height = height
        self.top_n = top_n
        self.extra_args = kwargs

    def get_property(self):
        return 'figure'

    def dash_component(self, data_sources):
        return LoadingGraph(id=self.get_id(), height=self.height)

    def callback(self, data_sources):
        def compute_group(group):
            data_sources.set_group_filter(self.data_source, group)
            metric = self.metric.compute(data_sources)
            data_sources.clear_group_filter()
            return metric

        df = data_sources.get(self.data_source)
        df = df.groupby(self.field).apply(compute_group).rename(self.metric.name())
        return plotly_wordcloud(df.reset_index(), self.field, self.metric.name(), height=self.height)


class PieChart(ChartComponent):
    def __init__(self, src, field, metric, height=None, **kwargs):
        self.data_source = src
        self.field = field
        self.metric = metric
        self.height = height
        self.extra_args = kwargs

    def get_property(self):
        return 'figure'

    def dash_component(self, data_sources):
        return LoadingGraph(id=self.get_id(), height=self.height)

    def callback(self, data_sources):
        def compute_group(group):
            data_sources.set_group_filter(self.data_source, group)
            metric = self.metric.compute(data_sources)
            data_sources.clear_group_filter()
            return metric

        df = data_sources.get(self.data_source)
        df = df.groupby(self.field).apply(compute_group).rename(self.metric.name())
        return pie_chart(df.reset_index().sort_values(self.metric.name()), self.field, self.metric.name(), height=self.height)


class MetricsPieChart(ChartComponent):
    def __init__(self, src, metrics, height, **kwargs):
        self.data_source = src
        self.metrics = metrics
        self.height = height
        self.extra_args = kwargs

    def get_property(self):
        return 'figure'

    def dash_component(self, data_sources):
        return LoadingGraph(id=self.get_id(), height=self.height)

    def callback(self, data_sources):
        rows = []
        for metric in self.metrics:
            rows.append([metric.name(), metric.compute(data_sources)])
        df = pd.DataFrame(rows, columns=['Métrica', 'Total'])
        return pie_chart(df, 'Métrica', 'Total', height=self.height, **self.extra_args)


class LineChart(ChartComponent):
    def __init__(self, src, field, metric, height=None, **kwargs):
        self.data_source = src
        self.field = field
        self.metric = metric
        self.height = height
        self.extra_args = kwargs

    def get_property(self):
        return 'figure'

    def dash_component(self, data_sources):
        return LoadingGraph(id=self.get_id(), height=self.height)

    def callback(self, data_sources):
        def compute_group(group):
            data_sources.set_group_filter(self.data_source, group)
            metric = self.metric.compute(data_sources)
            data_sources.clear_group_filter()
            return metric

        df = data_sources.get(self.data_source)
        df = df.groupby(self.field).apply(compute_group).rename(self.metric.name())
        return line_chart(df.reset_index().sort_values(self.field), self.field, self.metric.name(), height=self.height, **self.extra_args)


class BarLineChart(ChartComponent):
    def __init__(self, src, field, metric_1, metric_2, height=None, **kwargs):
        self.data_source = src
        self.field = field
        self.metric_1 = metric_1
        self.metric_2 = metric_2
        self.height = height
        self.extra_args = kwargs

    def get_property(self):
        return 'figure'

    def dash_component(self, data_sources):
        return LoadingGraph(id=self.get_id(), height=self.height)

    def callback(self, data_sources):
        def compute_group_1(group):
            data_sources.set_group_filter(self.data_source, group)
            metric = self.metric_1.compute(data_sources)
            data_sources.clear_group_filter()
            return metric

        def compute_group_2(group):
            data_sources.set_group_filter(self.data_source, group)
            metric = self.metric_2.compute(data_sources)
            data_sources.clear_group_filter()
            return metric

        df = data_sources.get(self.data_source)
        df1 = df.groupby(self.field).apply(compute_group_1).rename(self.metric_1.name()).reset_index()
        df2 = df.groupby(self.field).apply(compute_group_2).rename(self.metric_2.name()).reset_index()
        df3 = df1.merge(df2, on=self.field)

        return bar_line_chart(df3.reset_index().sort_values(self.field), self.field, self.metric_1.name(), self.metric_2.name(), self.metric_1.name(), self.metric_2.name(), height=self.height, **self.extra_args)


class TreeMapChart(ChartComponent):
    def __init__(self, src, category, aggregate, height=None, **kwargs):
        self.data_source = src
        self.category = category
        self.aggregate = aggregate
        self.height = height
        self.extra_args = kwargs

    def get_property(self):
        return 'figure'

    def dash_component(self, data_sources):
        return LoadingGraph(id=self.get_id(), height=self.height)

    def callback(self, data_sources):
        df = data_sources.get(self.data_source)
        return treemap_chart(df, [self.category], self.aggregate, self.category, height=self.height)


class EryxTab(EryxComponent):
    def __init__(self, children, data_sources):
        self.children = children
        self.data_sources = data_sources

    def dash_component(self, data_sources):
        return dbc.Container([c.dash_component(data_sources) for c in self.children], fluid=True)

    def callback(self, *args, **kwargs):
        self.data_sources.clear()

        for filter_config, filter in zip(args, self.get_filters()):
            filter.filter(self.data_sources, filter_config)

        outputs = []
        for chart in self.get_charts():
            outputs.append(chart.callback(self.data_sources))

        return outputs

    def add_to_dash_app(self, app, preprocessing=None):
        if preprocessing is None:
            preprocessing = lambda x: x

        inputs = [Input(filter.get_id(), "value") for filter in self.get_filters()]
        outputs = [Output(chart.get_id(), chart.get_property()) for chart in self.get_charts()]

        app.callback(*(tuple(outputs) + tuple(inputs)))(preprocessing(self.callback))
