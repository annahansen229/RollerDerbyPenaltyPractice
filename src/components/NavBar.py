from typing import Dict, List, Union

import dash_mantine_components as dmc
from dash import Input, Output, State, callback, no_update
from dash_iconify import DashIconify

from src.clips import get_playlist
from src.components import Player
from src.models import AppStore, Format, Option, Topic


class FormatPicker(dmc.AccordionItem):
    def __init__(self):

        super().__init__(
            children=[
                dmc.AccordionControl('Practice Format'),
                dmc.AccordionPanel(
                    dmc.SegmentedControl(
                        id='format',
                        data=Format.get_options(),
                        value=Format.get_default_option()
                    )
                ),
            ],
            value='format',
        )


class TopicPicker(dmc.AccordionItem):
    '''
        Renders the Topic Picker input component

        Args:
            start_button (str): The identifier of the start button component
    '''

    def __init__(self, start_button: str):
        super().__init__(
            children=[
                dmc.AccordionControl('Topic Areas'),
                dmc.AccordionPanel([
                    dmc.InputWrapper(
                        dmc.CheckboxGroup(
                            id='topics',
                            children=dmc.Stack([
                                dmc.Checkbox(**option, size='sm')
                                for option in Topic.get_options()
                            ]),
                            value=Topic.all(),
                        ),
                        id='topics-wrapper',
                        error=None,
                    ),
                ])
            ],
            value='topic'
        )

        @callback(
            Input('topics', 'value'),
            output=dict(
                error=Output('topics-wrapper', 'error'),
                start_button_disabled=Output(start_button, 'disabled')
            )
        )
        def validate_topics(selected: List[Topic]) -> Dict[str, str | None | bool]:
            '''
                Displays an error message when at least one topic is not selected
            '''
            return dict(
                error=None if selected else "Select at least one topic",
                start_button_disabled=not selected
            )


class OptionPicker(dmc.AccordionItem):
    def __init__(self):

        super().__init__(
            children=[
                dmc.AccordionControl('Other Options'),
                dmc.AccordionPanel(
                    dmc.CheckboxGroup(
                        id='options',
                        children=dmc.Stack([
                            dmc.Checkbox(**option, size='sm')
                            for option in Option.get_options()
                        ]),
                        value=Option.all(),
                    ),
                )
            ],
            value='options'
        )


class NavBar(dmc.AppShellNavbar):
    '''
        Renders the Options control component

        Args:
            player (Player): The player component
            contact_form (str): The identifier of the contact form component
            app_store (str): The identifier of the app store
    '''

    def __init__(self, player: Player, contact_form: str, app_store: str):
        self.contact_button_id = 'contact_button'
        self.start_button_id = 'start_button'

        super().__init__(
            id='navbar',
            children=[
                dmc.Accordion(
                    children=[
                        FormatPicker(),
                        TopicPicker(self.start_button_id),
                        OptionPicker(),
                    ],
                    multiple=True,
                    variant='contained'
                ),

                dmc.Button(
                    'Start',
                    id=self.start_button_id,
                    rightSection=DashIconify(icon='flowbite:chevron-double-right-outline'),
                    variant='filled',
                    mt=10,
                ),

                dmc.Button(
                    'Contact Us',
                    id=self.contact_button_id,
                    mt='auto'
                )
            ],
            p='md'
        )

        @callback(
            output=dict(
                player_store=Output(player.store, 'data', allow_duplicate=True,),
                start_button_text=Output(self.start_button_id, 'children', allow_duplicate=True,),
                url=Output(player.video, 'url', allow_duplicate=True, ),
                mobile_burger=Output('mobile-burger', 'opened', allow_duplicate=True),
                desktop_burger=Output('desktop-burger', 'opened', allow_duplicate=True),
                app_store=Output(app_store, 'data', allow_duplicate=True)
            ),
            inputs=dict(
                btn=Input(self.start_button_id, 'n_clicks')
            ),
            state=dict(
                format=State('format', 'value'),
                topics=State('topics', 'value'),
                options=State('options', 'value'),
            ),
            prevent_initial_call=True
        )
        def start_button_click(format: Format, topics: List[Topic], options: List[Option], **kwargs) -> Dict[str, Union[bool, str, Dict]]:
            '''
                When the start button is clicked, get the playlist based on the selected options, and
                set the store contents and url of the first video
            '''
            first_video, *remaining_playlist = get_playlist(format, topics, options)

            return dict(
                player_store=remaining_playlist,
                start_button_text='Restart',
                url=first_video['url'],
                mobile_burger=False,
                desktop_burger=False,
                app_store=AppStore(active=player.id, last=None, finished=False),
            )

        @callback(
            output=dict(
                contact_button_text=Output(self.contact_button_id, 'children'),
                app_store=Output(app_store, 'data', allow_duplicate=True),
                playing=Output(player.video, 'playing', allow_duplicate=True)
            ),
            inputs=dict(
                btn=Input(self.contact_button_id, 'n_clicks')
            ),
            state=dict(
                currently_hidden=State(contact_form, 'hidden'),
                old_app_store=State(app_store, 'data'),
            ),
            prevent_initial_call=True
        )
        def contact_button_click(currently_hidden, old_app_store: Dict[str, str], **kwargs) -> Dict[str, Union[bool, str]]:
            '''
                Hides/Shows the contact form, modifies the contact button text based on new state, and
                pauses playback if mid-session
            '''
            if currently_hidden:
                last = old_app_store.get('active')
                return dict(
                    contact_button_text='Close Contact Form',
                    app_store=AppStore(
                        active=contact_form,
                        last=last,
                        finished=old_app_store.get('finished')
                    ),
                    playing=False if last == player.id else no_update
                )

            else:
                active = old_app_store.get('last')
                return dict(
                    contact_button_text='Contact Us',
                    app_store=AppStore(
                        active=active,
                        last=contact_form,
                        finished=old_app_store.get('finished')
                    ),
                    playing=True if active == player.id else no_update
                )
