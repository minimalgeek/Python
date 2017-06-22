import logging
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

logger = logging.getLogger(__name__)


def add_styled_div(direction=None):
    def actual_decorator(func):
        def deco():
            return html.Div(children=[func()], style={
                'float': direction,
                'display': 'inline-block',
                'width': '465px',
                'padding': '20px',
                'margin': '10px',
                'backgroundColor': '#F9F9F9'
            })
        return deco
    return actual_decorator


def setup_app_callbacks(app: dash.Dash):
    @app.callback(
        Output(component_id='msg-div', component_property='children'),
        [Input(component_id='zacks-button', component_property='children')]
    )
    def update_output_div(input_value):
        msg: str = 'You\'ve called ZACKS'
        logger.info(msg)
        return [msg]


@add_styled_div()
def zacks() -> html.Button:
    return html.Button('Refresh dates from \'zacks.com\'', id='zacks-button')


@add_styled_div()
def earnings_transcript_top() -> html.Button:
    return html.Button('Download actual earnings transcripts from \'seekingalpha.com\'', id='ett-button')


@add_styled_div()
def tone_calc() -> html.Button:
    return html.Button('Henry tone calculation', id='tc-button')


@add_styled_div()
def run_strategy() -> html.Button:
    return html.Button('Run strategy', id='rs-button')
