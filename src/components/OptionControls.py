from dataclasses import asdict
from typing import Dict, List, Union

import dash_mantine_components as dmc
from dash import Input, Output, State, callback

from src.clips import clips, get_playlist
from src.models import Format, Option, Topic


class FormatPicker(dmc.AccordionItem):
    def __init__(self):

        self.intial_format = Format.get_default_option()

        super().__init__(
            children=[
                dmc.AccordionControl('Practice Format'),
                dmc.AccordionPanel(
                    dmc.SegmentedControl(
                        id='format',
                        data=Format.get_options(clips),
                        value=self.intial_format
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
                                dmc.Checkbox(label=option['label'], value=option['value'], size='sm')
                                for option in Topic.get_options(clips)
                            ]),
                            value=Topic.get_all(),
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
        def validate_topics(selected):
            '''
                Displays an error message when at least one topic is not selected
            '''
            return dict(
                error=None if selected else "Select at least one topic",
                start_button_disabled=not selected
            )


class OptionPicker(dmc.AccordionItem):
    def __init__(self, initial_format):

        self.initial_options = Option.get_options(clips, initial_format)
        self.initial_children = self.get_checkboxes(self.initial_options)
        self.initial_value = [option['value'] for option in self.initial_options]

        super().__init__(
            children=[
                dmc.AccordionControl(
                    'Other Options',
                    disabled=not self.initial_options,
                    id='options_accordion_control'
                ),
                dmc.AccordionPanel(
                    dmc.CheckboxGroup(
                        id='options',
                        children=self.initial_children,
                        value=self.initial_value,
                    ),
                )
            ],
            value='options'
        )

        @callback(
            Input('format', 'value'),
            State('options', 'value'),
            ouput=dict(
                children=Output('options', 'children'),
                value=Output('options', 'value'),
                disabled=Output('options_accordion_control', 'value')
            ),
        )
        def update_available_options(selected_format, selected_options) -> Dict[str, dmc.Stack | List[Option] | bool]:
            '''
                Updates the available Options when the selected Format changes
            '''
            available_options = Option.get_options(clips, selected_format)
            values = [option['value'] for option in available_options if option in selected_options]

            children = self.get_checkboxes(available_options)

            return dict(children=children, value=values, disabled=not available_options)

    def get_checkboxes(self, options) -> dmc.Stack:
        '''
            Returns a stack of dmc.Checkbox controls for the given options
        '''
        return dmc.Stack([
            dmc.Checkbox(label=option['label'], value=option['value'], size='sm')
            for option in options
        ])


class OptionControls(dmc.AppShellNavbar):

    def __init__(self, player):
        self.format_picker = FormatPicker()
        self.topic_picker = TopicPicker()
        self.option_picker = OptionPicker(self.format_picker.intial_format)

        super().__init__(
            id='navbar',
            children=[
                dmc.Accordion(
                    children=[
                        self.format_picker,
                        self.topic_picker,
                        self.option_picker,
                    ],
                    multiple=True,
                    variant='contained'
                ),

                dmc.Button(
                    id='start_button',
                    children='Start',
                    variant='filled',
                    mt=10,
                ),
            ],
            p='md'
        )

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
                topics=State('topics', 'value'),
                options=State('options', 'value'),
            ),
            prevent_initial_call=True
        )
        def start_button_click(format, topics, options, **kwargs) -> Dict[str, Union[bool, str, Dict]]:
            '''
                When the start button is clicked, get the playlist based on the selected options and
                set the store contents and url of the first video
            '''
            first_video, *remaining_playlist = get_playlist(format, topics, options)

            return dict(
                store=[asdict(clip) for clip in remaining_playlist],
                start_button_text='Restart',
                url=first_video.url
            )
