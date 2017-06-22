from typing import List

import dash_core_components as dcc
import dash_html_components as html


def main_header() -> List:
    return [html.H1('IB Trader Manager'),
            html.H2('Execution steps')]


def msg_div() -> List:
    return [html.Div(id='msg-div')]
