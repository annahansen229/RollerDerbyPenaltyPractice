import dash_mantine_components as dmc
from dash import Input, Output, clientside_callback
from dash_iconify import DashIconify


class ThemeToggle(dmc.ActionIcon):
    '''
        Renders the ThemeToggle component
    '''

    def __init__(self,):
        super().__init__(
            [
                dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
                dmc.Paper(DashIconify(icon="radix-icons:moon", width=25), lightHidden=True),
            ],
            id="color-scheme-toggle",
            variant="transparent",
            color="yellow",
            size="lg",
        )

        clientside_callback(
            """
            (n) => {
                document.documentElement.setAttribute(
                    'data-mantine-color-scheme',
                    (n % 2) ? 'dark' : 'light'
                );
                return window.dash_clientside.no_update      
            }
            """,
            Output("color-scheme-toggle", "id"),
            Input("color-scheme-toggle", "n_clicks"),
        )
