

from typing import Dict

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback, dcc
from dotenv import load_dotenv

from src.components import ContactForm, Content, NavBar, Splash, ThemeToggle
from src.models import AppStore

load_dotenv()

app = Dash(__name__, title='Roller Derby Penalty Practice')

server = app.server

app_store_id = 'app_store'
content_id = 'content'
interval_id = 'content_interval'

splash = Splash(app_store_id=app_store_id)

contact_form = ContactForm()

nav_bar = NavBar(
    content_id=content_id,
    interval_id=interval_id,
    contact_form_id=contact_form.id,
    app_store_id=app_store_id
)

content = Content(
    id=content_id,
    interval_id=interval_id,
    app_store_id=app_store_id,
    splash_id=splash.id,
    nav_bar=nav_bar
)

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
        nav_bar,

        dmc.AppShellMain([
            splash,
            content,
            contact_form,
        ]),
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
        dcc.Store(id=app_store_id, storage_type='session', data=AppStore(active=splash.id, last=None, finished=False)),
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


@callback(
    Input(app_store_id, 'data'),
    output=dict(
        splash_hidden=Output(splash.id, 'hidden'),
        content_hidden=Output(content.id, 'hidden'),
        contact_form_hidden=Output(contact_form.id, 'hidden'),
    ),
    prevent_initial_call=True
)
def set_active_content(app_store: AppStore) -> Dict[str, bool]:
    active_id = app_store['active']
    return dict(
        splash_hidden=active_id != splash.id,
        content_hidden=active_id != content.id,
        contact_form_hidden=active_id != contact_form.id
    )


if __name__ == '__main__':
    app.run(debug=True)
