from dataclasses import asdict
from typing import Dict, List

import dash_mantine_components as dmc
import dash_player as dp
from dash import Input, Output, State, callback, dcc, html, no_update

from src.models import Clip


class Player(html.Div):
    '''
        Renders the Player component

        Args:
            id (str): The identifier of the player component
            playlist (str): The identifier of the playlist store component
    '''

    def __init__(self, id: str, playlist: str):

        self.video = 'video'
        self.finished = 'finished'
        self.collapse = f'{id}_collapse'
        self.playlist = playlist

        super().__init__(
            id=id,
            children=[
                dcc.Store(id=self.finished, storage_type='session', data=False),
                dmc.Collapse(
                    dp.DashPlayer(
                        id=self.video,
                        url=None,
                        playing=False,
                        controls=True,
                        intervalCurrentTime=500,
                        style={'maxWidth': '100%'}
                    ),
                    opened=False,
                    id=self.collapse,
                ),
            ]
        )

        self.register_callbacks()

    def register_callbacks(self):
        callback(
            output=dict(
                url=Output(self.video, 'url', allow_duplicate=True,),
                playlist=Output(self.playlist, 'data', allow_duplicate=True,),
                finished=Output(self.finished, 'data', allow_duplicate=True,)
            ),
            inputs=dict(
                current_time=Input(self.video, 'currentTime'),
            ),
            state=dict(
                duration=State(self.video, 'duration'),
                playlist=State(self.playlist, 'data'),
                url=State(self.video, 'url'),
            ),
            prevent_initial_call=True
        )(self.play_next_video)

        callback(
            output=dict(
                playing=Output(self.video, 'playing', allow_duplicate=True,),
                opened=Output(self.collapse, 'opened')
            ),
            inputs=dict(
                url=Input(self.video, 'url')
            ),
            prevent_initial_call=True
        )(self.toggle)

    def toggle(self, url: str) -> Dict[str, bool]:
        '''
            When there is no url, stop playing
            When there is a url, start playing
        '''
        playing = bool(url)
        return dict(
            playing=playing,
            opened=playing,
        )

    def play_next_video(self, current_time: float, duration: float, playlist: List[Clip], url: None | str) -> Dict[str, str | List[Clip] | bool]:
        '''
            When the current_time changes, check if the full video time has elapsed.

            If so, and the store has items remaining, set the next video url and advance the playlist

            If the store is empty, clear the video url and the playlist

            If the full video time has not yet elapsed, do nothing.
        '''
        new_url = no_update
        new_playlist = no_update
        finished = no_update

        if current_time == duration and url is not None:
            # video has reached the end
            try:
                next_video, *remaining_playlist = [Clip(**dict) for dict in playlist]
                new_url = next_video.url
                new_playlist = [asdict(clip) for clip in remaining_playlist]
            except ValueError:
                # end of the playlist
                new_url = None
                new_playlist = []
                finished = True

        return dict(
            url=new_url,
            playlist=new_playlist,
            finished=finished,
        )
