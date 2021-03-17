from eryx_dash.formats import format_money


def update_layout(fig):
    fig.update_layout(
        plot_bgcolor='#303030',
        paper_bgcolor='#303030',

        margin=dict(l=20, r=20, t=20, b=20),

        font_family="Lato",
        font_size=14,

        legend=dict(
            title_font_family="Lato",
            font=dict(
                family="Lato",
                size=12,
                color="white"
            ),
        ),

        xaxis={'showgrid': False, 'tickfont': dict(
            family='Lato',
            size=12,
            color='rgb(255, 255, 255)',
        ), 'showline': False},
        yaxis={'showgrid': False, 'tickfont': dict(
            family='Lato',
            size=12,
            color='rgb(255, 255, 255)',
        ), 'showline': False, 'zeroline': False},
        yaxis2={'showgrid': False, 'tickfont': dict(
            family='Lato',
            size=12,
            color='rgb(255, 255, 255)',
        ), 'showline': False, 'zeroline': False},

        font=dict(
            family="Lato",
            size=18,
            color="white"
        )
    )

    fig.update_xaxes(showline=False, linecolor='#303030', zeroline=False)
    fig.update_yaxes(showline=False, linecolor='#303030', zeroline=False)

    return fig


def customize_figure(fig, title=None, height=None):
    if title is not None:
        fig.update_layout(
            title={
                'text': title,
                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            # xaxis_title="X Axis Title",
            # yaxis_title="Y Axis Title",
            # legend_title="Legend Title",
        )

    if height is not None:
        fig.update_layout(height=height)

    return fig


def format_templates(format_type):
    all_templates = {
        'money': {
            'format_text': '$%{y:.3s}',
            'format_hover': '$%{y:.3s} | %{x}',
            'format_tick': '$2s',
            'format_annotation': lambda x: format_money(x),
        },
        'number': {
            'format_text': '%{text:.d}',
            'format_hover': '%{y:.d} | %{x}',
            'format_tick': 'd',
            'format_annotation': lambda x: int(x),
        },
        'percentage': {
            'format_text': '%{text:.0%}',
            'format_hover': '%{y:.0%} | %{x}',
            'format_tick': '%',
            'format_annotation': lambda x: '%.0f%%' % (100 * x),
        },
    }

    return all_templates[format_type]
