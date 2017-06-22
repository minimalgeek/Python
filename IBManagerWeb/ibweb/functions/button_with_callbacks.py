import logging
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

logger = logging.getLogger(__name__)


def setup_app(app: dash.Dash):
    @app.callback(
        Output(component_id='msg-div', component_property='children'),
        [Input(component_id='zacks-button', component_property='children')]
    )
    def update_output_div(input_value):
        msg: str = 'You\'ve called ZACKS'
        logger.info(msg)
        return [msg]


def zacks() -> html.Button:
    return html.Button('Refresh dates from \'zacks.com\'', id='zacks-button')


def earnings_transcript_top() -> html.Button:
    return html.Button('Download actual earnings transcripts from \'seekingalpha.com\'', id='et-button')


def tone_calc() -> html.Button:
    return html.Button('Henry tone calculation', id='tc-button')


def run_strategy() -> html.Button:
    return html.Button('Run strategy', id='rs-button')
