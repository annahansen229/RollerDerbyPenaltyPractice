from typing import Dict, List, Union

import dash_mantine_components as dmc
from dash import Input, Output, State, callback, html
from dash_iconify import DashIconify

from src.components import Content
from src.models import AppStore, Format, Topic

CONTACT_BUTTON_ID = 'contact_button'
START_BUTTON_ID = 'start_button'


class Slider(html.Div):
    def __init__(self, id: str, title: str, initial_value: int = 5):

        self.control_id = id

        super().__init__(
            children=[
                dmc.Text(title, mb=10),
                dmc.Slider(
                    value=initial_value,
                    min=3,
                    max=10,
                    step=1,
                    mb='sm',
                    id=self.control_id
                )
            ],
            hidden=False,
            style={'marginBottom': 10}
        )


prompt_display = Slider('prompt-display', 'Prompt Display Seconds')
answer_display = Slider('answer-display', 'Answer Display Seconds')


class PlaybackControls(dmc.AccordionItem):
    def __init__(self):

        self.prompt_display = prompt_display
        self.answer_display = answer_display

        super().__init__(
            children=[
                dmc.AccordionControl('Playback Controls'),
                dmc.AccordionPanel(
                    children=[
                        self.prompt_display,
                        self.answer_display,
                    ]
                ),
            ],
            value='playback',
        )


class FormatPicker(dmc.AccordionItem):
    def __init__(self):
        self.control_id = 'format_picker'

        super().__init__(

            children=[
                dmc.AccordionControl('Practice Format'),
                dmc.AccordionPanel(
                    dmc.SegmentedControl(
                        id=self.control_id,
                        data=Format.get_options(),
                        value=Format.get_default_option(),
                        mb='sm'
                    ),
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
        self.control_id = 'topic_picker'

        super().__init__(
            children=[
                dmc.AccordionControl('Topic Areas'),
                dmc.AccordionPanel([
                    dmc.InputWrapper(
                        dmc.CheckboxGroup(
                            id=self.control_id,
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
            Input(self.control_id, 'value'),
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


format_picker = FormatPicker()
topic_picker = TopicPicker(START_BUTTON_ID)
playback_controls = PlaybackControls()


class NavBar(dmc.AppShellNavbar):
    '''
        Renders the Options control component

        Args:
            content_id (str): The identifier of the Content component
            interval_id (str): The identifier of the content interval component
            contact_form_id (str): The identifier of the ContactForm component
            app_store_id (str): The identifier of the app store component
    '''

    def __init__(self, content_id: Content, interval_id: str, contact_form_id: str, app_store_id: str):
        self.contact_button_id = CONTACT_BUTTON_ID
        self.start_button_id = START_BUTTON_ID

        self.format_picker = format_picker
        self.topic_picker = topic_picker
        self.playback_controls = playback_controls

        super().__init__(
            id='navbar',
            children=[
                dmc.Accordion(
                    children=[
                        self.format_picker,
                        self.topic_picker,
                        self.playback_controls,
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
                interval_disabled=Output(interval_id, 'disabled'),
                n_intervals=Output(interval_id, 'n_intervals'),
                start_button_text=Output(self.start_button_id, 'children', allow_duplicate=True,),
                mobile_burger=Output('mobile-burger', 'opened', allow_duplicate=True),
                desktop_burger=Output('desktop-burger', 'opened', allow_duplicate=True),
                app_store=Output(app_store_id, 'data', allow_duplicate=True)
            ),
            inputs=dict(
                btn=Input(self.start_button_id, 'n_clicks')
            ),
            prevent_initial_call=True
        )
        def start_button_click(btn: int) -> Dict[str, Union[bool, str, Dict]]:
            '''
                When the start button is clicked, enable the content interval and set the active display to content
            '''
            return dict(
                start_button_text='Restart',
                interval_disabled=False,
                n_intervals=0,
                mobile_burger=False,
                desktop_burger=False,
                app_store=AppStore(active=content_id, last=None, finished=False),
            )

        @callback(
            output=dict(
                contact_button_text=Output(self.contact_button_id, 'children'),
                interval_disabled=Output(interval_id, 'disabled', allow_duplicate=True),
                app_store=Output(app_store_id, 'data', allow_duplicate=True),
            ),
            inputs=dict(
                btn=Input(self.contact_button_id, 'n_clicks')
            ),
            state=dict(
                currently_hidden=State(contact_form_id, 'hidden'),
                old_app_store=State(app_store_id, 'data'),
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
                    interval_disabled=last == content_id,
                    app_store=AppStore(
                        active=contact_form_id,
                        last=last,
                        finished=old_app_store.get('finished')
                    ),
                )

            else:
                active = old_app_store.get('last')
                return dict(
                    contact_button_text='Contact Us',
                    interval_disabled=active != content_id,
                    app_store=AppStore(
                        active=active,
                        last=contact_form_id,
                        finished=old_app_store.get('finished')
                    ),
                )
