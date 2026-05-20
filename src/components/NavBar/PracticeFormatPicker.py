from src.models import PracticeFormat


import dash_mantine_components as dmc


class PracticeFormatPicker(dmc.AccordionItem):
    def __init__(self):
        super().__init__(
            children=[
                dmc.AccordionControl('Practice Format'),
                dmc.AccordionPanel(
                    dmc.SegmentedControl(
                        id='practice-format',
                        data=PracticeFormat.get_options(),
                        value=PracticeFormat.get_default_option()
                    )
                )
            ],
            value='practice-format',
        )
