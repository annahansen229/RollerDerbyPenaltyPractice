

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc

from src.components import OptionControls, Player, Splash, ThemeToggle

app = Dash(__name__, title='Roller Derby Penalty Practice')

server = app.server

playlist_id = 'store'

player = Player(id='player', playlist=playlist_id)

splash = Splash(player)

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
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
                            dmc.Title(
                                'Roller Derby Signals and Cues Practice',
                                id='mobile-title',
                                order=6,
                                hiddenFrom='sm'
                            ),
                            dmc.Title(
                                'Roller Derby Hand Signals and Verbal Cues Practice',
                                id='desktop-title',
                                order=3,
                                visibleFrom='sm'
                            ),

                        ],
                        gap='xs',
                        wrap='nowrap',
                    ),
                    ThemeToggle(),
                ],
                gap='xs',
                wrap='nowrap',
                justify='space-between',
                h="100%",
                px="md",
            ),
        ),
        OptionControls(player, playlist_id),
        dmc.AppShellMain([
            splash,
            player,
        ]),
        dmc.AppShellFooter(
            dmc.Text(children=[
                'Thank you to ',
                dmc.Anchor(
                    "Axis of Stevil",
                    href="https://www.youtube.com/feed/subscriptions/UCgxwwxOVwKbMNmivt-ImKJQ",
                    c='grape'
                ),
                ', who graciously allowed me to use his video content to create this app.',
            ]
            ),
            px="md",
            display='flex',
            style={'align-items': 'center'},
        )
    ],
    header={
        "height": 60,
        "offset": True,
    },
    footer={
        "height": {'sm': 80, 'lg': 60},
        "offset": True,
    },
    navbar={
        "width": 300,
        "breakpoint": "sm",
        "collapsed": {"mobile": True, "desktop": False},
    },
    padding="md",
    id="appshell",
)

app.layout = dmc.MantineProvider(
    [
        dcc.Store(id=playlist_id, storage_type='session', data=[]),
        layout
    ],
    id='provider',
    theme={
        "primaryColor": 'grape',
    },
)


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


if __name__ == '__main__':
    app.run(debug=True)
