import logging
import dash
import dash_core_components as dcc
import dash_html_components as html

from ibweb import config as cfg

from ibweb.graphs import graph
from ibweb.layouts import column_layout as cl
from ibweb.statics import header_text as ht
from ibweb.functions import button_with_callbacks as bwc

logger = logging.getLogger(__name__)

style = {
    'align': 'center',
    'textAlign': 'center',
    'color': '#404040',
    # 'columnCount': 3
}


def main() -> dash.Dash:
    logger.debug('Enter main')
    cfg.say_hello()
    app = dash.Dash()
    app.layout = html.Div(
        style=style,
        children=
        ht.main_header() +
        # cl.layout_3([html.H3(i) for i in range(20)]) +
        cl.layout_3([bwc.zacks(),
                     bwc.earnings_transcript_top(),
                     bwc.tone_calc(),
                     bwc.run_strategy()]) +
        ht.msg_div()
    )
    bwc.setup_app_callbacks(app)
    return app


if __name__ == '__main__':
    app = main()
    app.run_server(debug=True)
