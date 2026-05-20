from src.models import Option


import dash_mantine_components as dmc


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
