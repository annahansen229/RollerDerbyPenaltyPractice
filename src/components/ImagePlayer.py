

from dash import html, dcc


class ImagePlayer(html.Div):
    '''
        Renders the ImagePlayer component
    '''

    def __init__(self):
        '''

        '''
        self.id = 'image-player'
        self.store = 'image-player-store'
        self.image = 'image'
        self.title = 'title'

        super().__init__(
            id=self.id,
            hidden=False,
            children=[
                dcc.Store(id=self.store, storage_type='session', data=[]),
                html.Img(
                    id=self.image,
                    src='static/images/penalties/back_block.png',
                    hidden=False,
                ),
                html.H1(
                    'Back Block',
                    id=self.title,
                    hidden=False
                )
            ]
        )
