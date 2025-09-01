
from dataclasses import asdict
from typing import Dict, Union

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc, html

from src.clips import clips, get_playlist
from src.components import Player
from src.models import Category, Format, Option

app = Dash()

# Requires Dash 2.17.0 or later

player = Player(id='player', store='store')

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(
                        id='mobile-burger',
                        size='sm',
                        hiddenFrom='sm',
                        opened=False,
                    ),
                    dmc.Burger(
                        id="desktop-burger",
                        size="sm",
                        visibleFrom="sm",
                        opened=True,
                    ),
                    dmc.Title('Roller Derby Hand Signals and Verbal Cues Practice')
                ],
                h="100%",
                px="md",
            )
        ),
        dmc.AppShellNavbar(
            id='navbar',
            children=[
                html.Div(
                    dcc.RadioItems(
                        id='format',
                        options=Format.get_options(clips),
                        value=Format.get_default_option(),
                    ),
                    hidden=True
                ),
                dcc.Checklist(
                    id='categories',
                    options=Category.get_options(clips),
                    value=Category.get_all(),
                ),
                dcc.Checklist(
                    id='options',
                    options=Option.all(),
                    value=[],
                ),
                html.Button(
                    id='start_button',
                    children='Start'
                ),
            ],
            p='md'
        ),
        dmc.AppShellMain(
            player,
        ),
    ],
    header={"height": 60},
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True, "desktop": False},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider([
    dcc.Store(id='store', storage_type='session', data=[]),
    layout
])


@callback(
    Output("appshell", "navbar"),
    Input("mobile-burger", "opened"),
    Input("desktop-burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(mobile_opened, desktop_opened, navbar):
    navbar["collapsed"] = {
        "mobile": not mobile_opened,
        "desktop": not desktop_opened,
    }
    return navbar


@callback(
    output=dict(
        store=Output('store', 'data', allow_duplicate=True,),
        start_button_text=Output('start_button', 'children', allow_duplicate=True,),
        url=Output(player.video, 'url', allow_duplicate=True, ),
    ),
    inputs=dict(
        btn=Input('start_button', 'n_clicks')
    ),
    state=dict(
        format=State('format', 'value'),
        categories=State('categories', 'value'),
        options=State('options', 'value'),
    ),
    prevent_initial_call=True
)
def start_button_click(format, categories, options, **kwargs) -> Dict[str, Union[bool, str, Dict]]:
    '''
        When the start button is clicked, get the playlist based on the selected options and
        set the store contents and url of the first video
    '''
    first_video, *remaining_playlist = get_playlist(format, categories, options)

    return dict(
        store=[asdict(clip) for clip in remaining_playlist],
        start_button_text='Restart',
        url=first_video.url
    )


if __name__ == '__main__':
    app.run(debug=True)
