from dash import Output, callback, Input

from src.models import MediaFormat


import dash_mantine_components as dmc


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
            Output('playback-mode-picker', 'hiddenFrom'),
            Input('media-format', 'value')
        )
        def toggle(value: str) -> str | None:
            '''
                Hides the playback mode selector when media format is video
            '''
            hide_playback_mode_picker = value == MediaFormat.get_default_option()

            return 'xs' if hide_playback_mode_picker else None
