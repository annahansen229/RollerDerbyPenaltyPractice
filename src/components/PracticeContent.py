from dash import html, Output, Input, callback

from src.models import MediaFormat
from src.components import VideoPlayer, ImagePlayer


class PracticeContent(html.Div):
    '''
        Renders the PracticeContent component
    '''

    def __init__(self, app_store: str, splash: str):
        '''
            Args:
                app_store (str): The identifier of the app_store component
                splash (str): The identifier of the splash component

        '''

        self.id = 'practice-content'

        video_player = VideoPlayer(app_store=app_store, splash=splash)
        image_player = ImagePlayer()

        self.video_player = video_player

        super().__init__(
            id=self.id,
            children=video_player
        )

        @callback(
            Output(self.id, 'children'),
            Input('media-format', 'value'),
            prevent_initial_call=True
        )
        def toggle_content(media_format: MediaFormat) -> html.Div:
            '''
                Sets the content to VideoPlayer or ImagePlayer based on the selected MediaFormat
            '''

            if media_format == MediaFormat.get_default_option():
                return video_player
            else:
                return image_player
