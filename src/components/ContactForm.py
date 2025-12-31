import os

from dash import html


class ContactForm(html.Iframe):
    '''
        Renders the Contact Form
    '''

    def __init__(self):
        self.id = 'contact_form'

        super().__init__(
            id=self.id,
            src=f"https://docs.google.com/forms/d/e/{os.getenv('CONTACT_FORM_ID')}/viewform?embedded=true",
            hidden=True
            # width="640",
            # height="649",
            # frameborder="0",
            # marginheight="0",
            # marginwidth="0"
            # marginwidth="0"
        )
