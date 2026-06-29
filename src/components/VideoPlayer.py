
import dash_player as dp
from dash import Input, Output, State, callback, html, no_update, ctx

from src.models import AppStore


class VideoPlayer(html.Div):
    '''
        Renders the VideoPlayer component
    '''

    def __init__(self, app_store_id: str, splash: str):
        '''
            Args:
                app_store (str): The identifier of the app_store component
                splash (str): The identifier of the splash component
        '''
        self.id = 'video-player'
        self.video = 'video'
        self.store = 'video-player-store'

        super().__init__(
            id=self.id,
            hidden=True,
            children=[
                dp.DashPlayer(
                    id=self.video,
                    url=None,
                    playing=False,
                    controls=True,
                    intervalCurrentTime=500,
                    style={'maxWidth': '100%'}
                ),
            ]
        )

        @callback(
            Output(self.video, 'playing'),
            Input(self.video, 'url'),
            Input(app_store_id, 'data.playing'),
        )
        def toggle_playing(url: str, app_store_playing: bool) -> bool:
            '''
                Toggles the playing state when the url is set or cleared, and when the app_store playing state changes    
            '''
            trigger_id = ctx.triggered_id

            if trigger_id == self.video:
                return bool(url)

            if trigger_id == app_store_id:
                return app_store_playing

        @callback(
            output=dict(
                player_url=Output(self.video, 'url', allow_duplicate=True,),
                app_store=Output(app_store_id, 'data', allow_duplicate=True),
            ),
            inputs=dict(
                current_time=Input(self.video, 'currentTime'),
            ),
            state=dict(
                duration=State(self.video, 'duration'),
                url=State(self.video, 'url'),
                app_store=State(app_store_id, 'data')
            ),
            prevent_initial_call=True
        )
        def play_next_video(current_time: float, duration: float, old_player_url: None | str, old_app_store: AppStore) -> dict[str, dict | bool]:
            '''
                When the current_time changes, check if the full video time has elapsed.

                If so, and the playlist has items remaining, set the next video url and advance the playlist

                If the playlist is empty, clear the video url and the playlist

                If the full video time has not yet elapsed, do nothing.
            '''
            player_url = no_update
            app_store = no_update

            if current_time == duration and old_player_url is not None:
                # video has reached the end
                try:
                    next_video, *remaining_playlist = old_app_store.get('playlist', [])
                    player_url = next_video['url']
                    new_playlist = remaining_playlist

                    app_store_updates = dict(
                        playlist=new_playlist,
                        url=player_url,
                    )

                    app_store = AppStore(
                        **old_app_store,
                        **app_store_updates
                    )

                except ValueError:
                    # end of the playlist
                    player_url = None
                    app_store = AppStore(
                        playlist=[],
                        url=player_url,
                        playing=False,
                        active=splash,
                        last=None,
                        finished=True
                    )

            return dict(
                player_url=player_url,
                app_store=app_store,
            )
