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
                        value=MediaFormat.get_default_option()
                    )
                ),
            ],
            value='media-format',
        )
