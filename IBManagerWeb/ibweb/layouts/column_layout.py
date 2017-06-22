import dash_core_components as dcc
import dash_html_components as html

style = {
    # 'textAlign': 'center',
    # 'color': '#404040',
    'columnCount': 3
}


def layout_3(children):
    lay = html.Div(children=children, style=style)
    return [lay]
