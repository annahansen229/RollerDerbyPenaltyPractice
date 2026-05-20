import dash_mantine_components as dmc

from src.models import PlaybackMode
from dash import Input, Output, callback, html


class Slider(html.Div):
    def __init__(self, id: str, title: str):
        super().__init__(
            children=[
                dmc.Text(title, mb=10),
                dmc.Slider(
                    value=10,
                    min=5,
                    max=30,
                    step=5,
                )
            ],
            id=id,
            hidden=True,
            style={'marginBottom': 10}
        )


class PlaybackModePicker(dmc.AccordionItem):
    def __init__(self):
        super().__init__(
            id='playback-mode-picker',
            children=[
                dmc.AccordionControl('Playback Mode'),
                dmc.AccordionPanel(
                    children=[
                        dmc.SegmentedControl(
                            id='playback-mode',
                            data=PlaybackMode.get_options(),
                            value=PlaybackMode.get_default_option(),
                            fullWidth=True,
                            mb=5
                        ),
                        Slider('slider-prompt', 'Prompt Display Interval'),
                        Slider('slider-answer', 'Answer Display Interval')
                    ]
                )
            ],
            value='playback-mode-picker',
            hiddenFrom='xs',
        )

        @callback(
            Output('slider-prompt', 'hidden'),
            Output('slider-answer', 'hidden'),
            Input('playback-mode', 'value'),
        )
        def toggle(value) -> tuple[bool, bool]:
            '''
                Hides the slider inputs when playback format is automatic
            '''
            hide_slider = value != PlaybackMode.get_default_option()
            return hide_slider, hide_slider
