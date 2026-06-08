from dash import Output, callback, Input

from src.models import MediaFormat


import dash_mantine_components as dmc

from src.utils import accordion_hidden_from


class MediaFormatPicker(dmc.AccordionItem):
    def __init__(self):
        super().__init__(
            children=[
                dmc.AccordionControl('Media Format'),
                dmc.AccordionPanel(
                    dmc.SegmentedControl(
                        id='media-format',
                        data=MediaFormat.get_options(),
                        value=MediaFormat.get_default_option(),
                        fullWidth=True
                    )
                ),
            ],
            value='media-format',
        )

        @callback(
            Input('media-format', 'value'),
            output=dict(
                playback_mode_hiddenFrom=Output('playback-mode-picker', 'hiddenFrom'),
                other_options_hiddenFrom=Output('intro-outro-picker', 'hiddenFrom'),

            )
        )
        def toggle(value: str) -> str | None:
            '''
                Hides or shows other picker components based on the selected MediaFormat
            '''
            video_mode = value == MediaFormat.get_default_option()
            image_mode = not video_mode

            return dict(
                playback_mode_hiddenFrom=accordion_hidden_from(video_mode),
                other_options_hiddenFrom=accordion_hidden_from(image_mode),
            )
