

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc

from src.components import OptionControls, Player

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
        OptionControls(player),
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


if __name__ == '__main__':
    app.run(debug=True)
