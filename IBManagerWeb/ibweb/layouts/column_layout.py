import dash_core_components as dcc
import dash_html_components as html

style = {
    # 'textAlign': 'center',
    # 'color': '#404040',
    'width': '1050px',
    'margin': '10px 0px 10px 0px',
    'padding': '20px',
    'display': 'inline-block',
    'backgroundColor': '#F0F0F0'
}


def layout_3(children):
    prev = None
    for child in children:
        if child.style is not None:
            if prev == 'left':
                prev = 'rigt'
            else:
                prev = 'left'
            child.style['float'] = prev
    lay = html.Div(children=children, style=style)
    return [lay]
