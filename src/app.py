

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc

from src.components import OptionControls, Player, Splash, ThemeToggle

app = Dash()

# Requires Dash 2.17.0 or later

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
                                'Roller Derby Hand Signals and Verbal Cues Practice',
                            ),
                        ]
                    ),
                    ThemeToggle(),
                ],
                justify='space-between',
                h="100%",
                px="md",
            )
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
            ), p="md")
    ],
    header={"height": 60},
    footer={"height": 60},
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
