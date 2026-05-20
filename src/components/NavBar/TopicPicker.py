from src.models import Topic


import dash_mantine_components as dmc
from dash import Input, Output, callback


from typing import Dict, List


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
