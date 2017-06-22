import logging
import dash
import dash_core_components as dcc
import dash_html_components as html

from ibweb import config as cfg

from ibweb.graphs import graph
from ibweb.layouts import column_layout as cl

logger = logging.getLogger(__name__)

style = {
    'textAlign': 'center',
    'color': '#404040',
    #'columnCount': 3
}


def main() -> dash.Dash:
    logger.debug('Enter main')
    cfg.say_hello()
    app = dash.Dash()
    app.layout = html.Div(
        style=style,
        children=[
            html.H1('IB Trader Manager'),
            html.H2('Execution steps'),
            cl.layout_3([html.H3(i) for i in range(20)])
        ])
    return app


if __name__ == '__main__':
    app = main()
    app.run_server(debug=True)
