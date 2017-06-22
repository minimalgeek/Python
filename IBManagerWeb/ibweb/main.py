import logging
import dash
import dash_core_components as dcc
import dash_html_components as html

from ibweb import config as cfg

from ibweb.graphs import graph

logger = logging.getLogger(__name__)

colors = {
    'text': '#505050'
}


def main() -> dash.Dash:
    logger.debug('Enter main')
    cfg.say_hello()
    app = dash.Dash()
    app.layout = html.Div(
        style={'textAlign': 'center',
               'color': colors['text']},
        children=[
            html.H1('IB Trader Manager'),
            html.H2('Execution steps'),
            graph.sample_graph()
        ])
    return app


if __name__ == '__main__':
    app = main()
    app.run_server(debug=True)
