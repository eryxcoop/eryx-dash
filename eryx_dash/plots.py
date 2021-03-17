import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import random
import plotly.graph_objs as go
import plotly.express as px
import plotly as py
import numpy as np
from eryx_dash.layout import update_layout, customize_figure, format_templates
from eryx_dash.formats import format_money
from plotly.subplots import make_subplots


def empty_card(title, an_id):
    return dcc.Loading(dbc.Card(
        dbc.CardBody(
            [
                html.H1("...", id=an_id, className="card-title"),
                html.P(title),
            ]
        ),
        className="text-center",
        style={"height": "7.8rem"}
    ), className='loading-spinner')


def card_chart(title, number):
    return dcc.Loading(dbc.Card(
        dbc.CardBody(
            [
                html.H1(number, className="card-title"),
                html.P(title),
            ]
        ),
        className="text-center",
        style={"height": "7.8rem"}
    ), className='loading-spinner')


def pie_chart(data, x_axis, y_axis, height=250, title=None):
    fig = go.Figure(data=[go.Pie(labels=data[x_axis], values=data[y_axis])])

    fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=12, textposition='inside')

    fig = update_layout(fig)
    fig = customize_figure(fig, title, height)
    return fig


def treemap_chart(data, path, values, color, height=400, title=None):
    fig = px.treemap(
        data,
        path=path,
        values=values,
        color=color,
        color_discrete_sequence=px.colors.sequential.Plasma_r
    )

    fig.update_layout(
        showlegend=False
    )

    fig = update_layout(fig)
    fig = customize_figure(fig, title, height)

    return fig


def bar_chart(data, x_axis, y_axis, height=None, skip_ticks=None, title=None, format='number', x_tick_format='"%d %b"'):
    format = format_templates(format)

    fig = go.Figure(go.Bar(
        x=data[x_axis],
        y=data[y_axis],
        hovertemplate=format['format_hover'],
        marker={'color': 'rgb(112, 176, 224)', 'line': dict(color='rgb(112, 176, 224)', width=3)}))

    annotations = []

    i = 0
    for xd, yd in zip(data[x_axis], data[y_axis]):
        if skip_ticks is None or i % skip_ticks == 0:
            annotations.append(dict(xref='x1', yref='y1',
                                    x=xd, y=yd + (data[y_axis].mean() * 0.15),
                                    text=format['format_annotation'](yd),
                                    font=dict(family='Lato', size=14,
                                              color='rgb(255, 255, 255)'),
                                    showarrow=False))
        i += 1

    fig.update_layout(
        showlegend=False,
        annotations=annotations,
    )

    fig = update_layout(fig)
    fig = customize_figure(fig, title, height)
    fig.update_xaxes(tickformat=x_tick_format)
    fig.update_yaxes(tickformat=format['format_tick'])

    return fig


def hbar_chart(data, x_axis, y_axis, height=None, title=None, format='money'):
    format = format_templates(format)

    fig = go.Figure(go.Bar(
        x=data[x_axis],
        y=data[y_axis],
        hovertemplate=format['format_hover'].replace('y', 'X').replace('x', 'y').replace('X', 'x'),
        orientation='h',
        marker={'color': 'rgb(112, 176, 224)', 'line': dict(color='rgb(112, 176, 224)', width=3)}))

    annotations = []

    for yd, xd in zip(data[x_axis], data[y_axis]):
        annotations.append(dict(xref='x1', yref='y1',
                                y=xd, x=yd + (data[x_axis].mean() * 0.1),
                                text=format['format_annotation'](yd),
                                font=dict(family='Lato', size=14,
                                          color='rgb(255, 255, 255)'),
                                showarrow=False))

    fig = update_layout(fig)

    fig.update_layout(
        showlegend=False,
        annotations=annotations,
    )

    fig.update_xaxes(tickformat=format['format_tick'], nticks=2)
    fig = customize_figure(fig, title, height)

    return fig


def line_line_chart(data, x_axis, line_1_axis, line_2_axis, line_1_legend, line_2_legend, title=None, height=290,
                   format_bar='money', format_line='percentage', format_x_axis='d', secondary_y_axis=True):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    format_bar = format_templates(format_bar)
    format_line = format_templates(format_line)

    fig.add_trace(
        go.Scatter(
            name=line_2_legend,
            x=data[x_axis],
            y=data[line_2_axis],
            text=data[line_2_axis],
            mode='lines+markers+text',
            textposition="top right",
            hovertemplate=format_line['format_hover'],
            textfont=dict(
                family="Lato",
                size=12,
                color="white"
            ),
            line=dict(color='rgb(252, 183, 20)', width=4),
            connectgaps=True,
            line_shape='linear',
            texttemplate=format_line['format_text']),
        secondary_y=secondary_y_axis)

    fig.add_trace(
        go.Scatter(
            name=line_1_axis,
            x=data[x_axis],
            y=data[line_1_axis],
            text=data[line_1_axis],
            texttemplate=format_bar['format_text'],
            textposition='top right',
            mode='lines+markers+text',
            hovertemplate=format_bar['format_hover'],
            textfont=dict(
                family="Lato",
                size=12,
                color="white"
            ),
            marker={'color': 'rgb(112, 176, 224)', 'line': dict(color='rgb(112, 176, 224)', width=3)}
        ))

    fig = update_layout(fig)

    fig.update_layout(yaxis_tickformat=format_bar['format_tick'])
    fig.update_layout(yaxis2_tickformat=format_line['format_tick'])
    fig.update_layout(xaxis_tickformat=format_x_axis)

    fig = customize_figure(fig, title, height)

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.95,
        xanchor="left",
        x=0,
        orientation="h",
    ))

    if secondary_y_axis:
        fig.update_layout(yaxis={'range': (0, data[line_1_axis].max() * 1.35)}, yaxis2={'range': (0, data[line_2_axis].max() * 1.35)})
    else:
        fig.update_layout(yaxis={'range': (0, max(data[line_1_axis].max() * 1.35, data[line_2_axis].max() * 1.35))})

    return fig


def bar_line_chart(data, x_axis, bar_axis, line_axis, bar_legend, line_legend, title=None, height=290,
                   format_bar='money', format_line='percentage', format_x_axis='d', secondary_y_axis=True):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    format_bar = format_templates(format_bar)
    format_line = format_templates(format_line)

    fig.add_trace(
        go.Scatter(
            name=line_legend,
            x=data[x_axis],
            y=data[line_axis],
            text=data[line_axis],
            mode='lines+markers+text',
            textposition="top right",
            hovertemplate=format_line['format_hover'],
            textfont=dict(
                family="Lato",
                size=12,
                color="white"
            ),
            line=dict(color='rgb(252, 183, 20)', width=4),
            connectgaps=True,
            line_shape='linear',
            texttemplate=format_line['format_text']),
        secondary_y=secondary_y_axis)

    fig.add_trace(
        go.Bar(
            name=bar_legend,
            x=data[x_axis],
            y=data[bar_axis],
            text=data[bar_axis],
            texttemplate=format_bar['format_text'], textposition='outside',
            hovertemplate=format_bar['format_hover'],
            textfont=dict(
                family="Lato",
                size=12,
                color="white"
            ),
            marker={'color': 'rgb(112, 176, 224)', 'line': dict(color='rgb(112, 176, 224)', width=3)}
        ))

    fig = update_layout(fig)

    fig.update_layout(yaxis_tickformat=format_bar['format_tick'])
    fig.update_layout(yaxis2_tickformat=format_line['format_tick'])
    fig.update_layout(xaxis_tickformat=format_x_axis)

    fig = customize_figure(fig, title, height)

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.95,
        xanchor="left",
        x=0,
        orientation="h",
    ))

    if secondary_y_axis:
        fig.update_layout(yaxis={'range': (0, data[bar_axis].max() * 1.35)}, yaxis2={'range': (0, data[line_axis].max() * 1.35)})
    else:
        fig.update_layout(yaxis={'range': (0, max(data[bar_axis].max() * 1.35, data[line_axis].max() * 1.35))})

    return fig


def line_chart(data, x_axis, y_axis, height=None, skip_ticks=None, title=None, format='money'):
    fig = go.Figure()

    format = format_templates(format)

    fig.add_trace(go.Scatter(
        x=data[x_axis],
        y=data[y_axis],
        mode='lines+markers',
        hovertemplate=format['format_hover'],
        line=dict(color='rgb(112, 176, 224)', width=4),
        connectgaps=True,
        line_shape='linear',
        marker={'size': 12}
    )
    )

    annotations = []
    i = 0

    for yd, xd in zip(data[y_axis], data[x_axis]):
        if skip_ticks is None or i % skip_ticks == 0:
            annotations.append(dict(xref='x1', yref='y1',
                                    y=yd + (data[y_axis].mean() * 0.05), x=xd,
                                    text=format['format_annotation'](yd),
                                    font=dict(family='Lato', size=14,
                                              color='rgb(255, 255, 255)'),
                                    showarrow=False))
        i += 1

    fig.update_layout(
        showlegend=False,
        annotations=annotations
    )

    fig.update_layout(yaxis_tickformat=format['format_tick'])
    fig.update_layout(xaxis_tickformat='%d %b')

    fig = update_layout(fig)
    fig = customize_figure(fig, title, height)

    return fig


def plotly_wordcloud(data, text_column, freq_column, height=290, title=None):
    words = data[text_column]
    frequency = data[freq_column]

    lower, upper = 15, 45
    original_frequency = frequency
    frequency = [((x - min(frequency)) / (max(frequency) - min(frequency))) * (upper - lower) + lower for x in
                 frequency]

    lenth = len(words)
    colors = [py.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(lenth)]

    data = go.Scatter(
        x=list(range(lenth)),
        y=random.choices(range(lenth), k=lenth),
        mode='text',
        text=words,
        hovertext=['{0}: ${1}'.format(w, format_money(f)) for w, f in zip(words, original_frequency)],
        hoverinfo='text',
        textfont={'size': frequency, 'color': colors, 'family': 'Lato'})

    fig = go.Figure(data=[data])

    fig.update_layout(
        showlegend=False,
        xaxis={'showticklabels': False},
        yaxis={'showticklabels': False},
    )

    fig = update_layout(fig)
    fig = customize_figure(fig, title, height)

    return fig


def checklist_filter(title, an_id, data, column, max_height=17):
    sorted_data = np.flip(np.sort(data[column].unique()))

    return dbc.FormGroup(
        [
            dbc.Label(title),
            dbc.Checklist(
                options=[
                    {"label": item, "value": item} for item in sorted_data
                ],
                value=[],
                id=an_id
            ),
        ], style={'maxHeight': '%sem' % max_height, 'overflow': 'auto', 'backgroundColor': '#303030', 'margin': 1}
    )


def dropdown_filter(title, an_id, data, column):
    sorted_data = np.flip(np.sort(data[column].unique()))
    return dbc.Card(dbc.FormGroup([
        dbc.Label(title),
        dcc.Dropdown(
            id=an_id,
            options=[
                {"label": item, "value": item} for item in sorted_data
            ],
            value=sorted_data[0],
            style={'color': '#212121'}
        ), ]
    ), body=True)


class LoadingGraph(dcc.Loading):
    def __init__(self, *args, **kwargs):
        fig = go.Figure(data=[go.Scatter(x=[], y=[])])

        annotations = [dict(xref='x1', yref='y1',
                            y=1, x=1,
                            text="...",
                            font=dict(family='Lato', size=36,
                                      color='rgb(255, 255, 255)'),
                            showarrow=False)]

        fig = update_layout(fig)

        fig.update_layout(
            xaxis={'showticklabels': False},
            yaxis={'showticklabels': False},
            annotations=annotations
        )

        if 'height' in kwargs:
            fig.update_layout(height=kwargs.pop('height'))

        graph = dcc.Graph(*args, **{'figure': fig, 'config': {'displayModeBar': False}, 'id': kwargs.pop('id')})
        kwargs['children'] = [graph]
        kwargs['className'] = 'loading-spinner'

        super(LoadingGraph, self).__init__(*args, **kwargs)
