from typing import Dict, List

import dash_player as dp
from dash import Input, Output, State, callback, dcc, html, no_update

from src.models import AppStore, Clip


class Player(html.Div):
    '''
        Renders the Player component
    '''

    def __init__(self, app_store: str, splash: str):
        '''
            Args:
                app_store (str): The identifier of the app_store component
                splash (str): The identifier of the splash component
        '''
        self.id = 'player'
        self.video = 'video'
        self.store = 'player_store'

        super().__init__(
            id=self.id,
            hidden=True,
            children=[
                dcc.Store(id=self.store, storage_type='session', data=[]),
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
            Input(self.video, 'url')
        )
        def toggle_playing(url: str) -> bool:
            return bool(url)

        @callback(
            output=dict(
                url=Output(self.video, 'url', allow_duplicate=True,),
                new_playlist=Output(self.store, 'data', allow_duplicate=True),
                app_store=Output(app_store, 'data', allow_duplicate=True),
            ),
            inputs=dict(
                current_time=Input(self.video, 'currentTime'),
            ),
            state=dict(
                duration=State(self.video, 'duration'),
                url=State(self.video, 'url'),
                playlist=State(self.store, 'data')
            ),
            prevent_initial_call=True
        )
        def play_next_video(current_time: float, duration: float, url: None | str, playlist: List[Clip]) -> Dict[str, Dict | bool]:
            '''
                When the current_time changes, check if the full video time has elapsed.

                If so, and the store has items remaining, set the next video url and advance the playlist

                If the store is empty, clear the video url and the playlist

                If the full video time has not yet elapsed, do nothing.
            '''
            new_url = no_update
            new_playlist = no_update
            app_store = no_update

            if current_time == duration and url is not None:
                # video has reached the end
                try:
                    next_video, *remaining_playlist = playlist
                    new_url = next_video['url']
                    new_playlist = remaining_playlist
                except ValueError:
                    # end of the playlist
                    new_url = None
                    new_playlist = []
                    app_store = AppStore(active=splash, last=None, finished=True)

            return dict(
                url=new_url,
                new_playlist=new_playlist,
                app_store=app_store,
            )
