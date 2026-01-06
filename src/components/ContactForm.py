import os

from dash import html


class ContactForm(html.Div):
    '''
        Renders the Contact Form
    '''

    def __init__(self):
        self.id = 'contact_form'

        super().__init__(
            id=self.id,
            hidden=True,
            style={
                'width': '100%',
                'height': '80vh'
            },
            children=[
                html.Iframe(
                    src=f"https://docs.google.com/forms/d/e/{os.getenv('CONTACT_FORM_ID')}/viewform?embedded=true",
                    style={'border': 0},
                    width='100%',
                    height='100%',
                ),
            ]
        )
