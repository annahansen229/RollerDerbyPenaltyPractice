from src.models import Option


import dash_mantine_components as dmc


class IntroOutroPicker(dmc.AccordionItem):
    def __init__(self):

        super().__init__(
            id='intro-outro-picker',
            children=[
                dmc.AccordionControl('Include Intro/Outro'),
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
            value='options',
            hiddenFrom=None,
        )
