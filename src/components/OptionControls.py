from dataclasses import asdict
from typing import Dict, List, Union

import dash_mantine_components as dmc
from dash import Input, Output, State, callback
from dash_iconify import DashIconify

from src.clips import get_playlist
from src.components import Player
from src.models import Format, Option, Topic


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
    def __init__(self):
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
                start_button_disabled=Output('start_button', 'disabled')
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


class OptionControls(dmc.AppShellNavbar):
    '''
        Renders the Options control component

        Args:
            player (Player): The player component
            playlist (str): The identifier of the playlist store component
    '''

    def __init__(self, player: Player, playlist: str):

        super().__init__(
            id='navbar',
            children=[
                dmc.Accordion(
                    children=[
                        FormatPicker(),
                        TopicPicker(),
                        OptionPicker(),
                    ],
                    multiple=True,
                    variant='contained'
                ),

                dmc.Button(
                    'Start',
                    id='start_button',
                    rightSection=DashIconify(icon='flowbite:chevron-double-right-outline'),
                    variant='filled',
                    mt=10,
                ),
            ],
            p='md'
        )

        @callback(
            output=dict(
                playlist=Output(playlist, 'data', allow_duplicate=True,),
                start_button_text=Output('start_button', 'children', allow_duplicate=True,),
                url=Output(player.video, 'url', allow_duplicate=True, ),
                finished=Output(player.finished, 'data', allow_duplicate=True),
                mobile_burger=Output('mobile-burger', 'opened', allow_duplicate=True),
                desktop_burger=Output('desktop-burger', 'opened', allow_duplicate=True),),
            inputs=dict(
                btn=Input('start_button', 'n_clicks')
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
                When the start button is clicked, get the playlist based on the selected options and
                set the store contents and url of the first video
            '''
            first_video, *remaining_playlist = get_playlist(format, topics, options)

            return dict(
                playlist=[asdict(clip) for clip in remaining_playlist],
                start_button_text='Restart',
                url=first_video.url,
                finished=False,
                mobile_burger=False,
                desktop_burger=False,
            )
