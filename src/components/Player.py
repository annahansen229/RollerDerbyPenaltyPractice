from dataclasses import asdict
from typing import List

import dash_player as dp
from dash import Input, Output, State, get_app, html, no_update

from src.models import Clip


class Player(html.Div):
    def __init__(self, id, store):

        super().__init__(id=id, hidden=True)

        self.video = 'video'
        self.store = store

        self.children = [
            dp.DashPlayer(
                id=self.video,
                url=None,
                playing=False,
                controls=True,
                intervalCurrentTime=500,
            ),
        ]

        self.register_callbacks()

    def register_callbacks(self):
        app = get_app()

        app.callback(
            output=dict(
                url=Output(self.video, 'url', allow_duplicate=True,),
                store=Output(self.store, 'data', allow_duplicate=True,),
            ),
            inputs=dict(
                current_time=Input(self.video, 'currentTime'),
            ),
            state=dict(
                duration=State(self.video, 'duration'),
                store=State(self.store, 'data'),
            ),
            prevent_initial_call=True
        )(self.play_next_video)

        app.callback(
            output=dict(
                hidden=Output(self.id, 'hidden', allow_duplicate=True,),
                playing=Output(self.video, 'playing', allow_duplicate=True,),
            ),
            inputs=dict(
                url=Input(self.video, 'url')
            ),
            prevent_initial_call=True
        )(self.show_player)

    def show_player(self, url):
        '''
            When there is no url, stop playing and hide player
            When there is a url, start playing and show player
        '''
        playing = bool(url)
        return dict(
            hidden=not playing,
            playing=playing,
        )

    def play_next_video(self, current_time: float, duration: float, store: List[Clip]):
        '''
            When the current_time changes, check if the full video time has elapsed.

            If so, and the store has items remaining, set the next video url and advance the playlist

            If the store is empty, clear the video url and the playlist

            If the full video time has not yet elapsed, do nothing.
        '''
        url = no_update
        new_playlist = no_update

        if current_time == duration:
            # video has reached the end
            try:
                next_video, *remaining_playlist = [Clip(**dict) for dict in store]
                url = next_video.url
                new_playlist = [asdict(clip) for clip in remaining_playlist]
            except ValueError:
                # end of the playlist
                url = None
                new_playlist = []

        return dict(
            url=url,
            store=new_playlist,
        )
