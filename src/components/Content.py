from typing import Any

import dash_mantine_components as dmc
from dash import Input, Output, State, callback, dcc, html, no_update
from dash.exceptions import PreventUpdate

from src.components import NavBar
from src.data import get_new_playlist, placeholder_image_src
from src.models import AppStore, Format, Media, Topic


class Content(html.Div):
    '''
        Renders the practice session content
    '''

    def __init__(self, id: str, interval_id: str, app_store_id: str, splash_id: str, nav_bar: NavBar):
        '''
            Args:
                    id (str): The identifier of the Content component
                    interval_id (str): The identifier of the content interval component
                    app_store_id (str): The identifier of the app_store component
                    splash_id (str): The identifier of the Splash component
                    nav_bar (str): The NavBar component
        '''

        self.id = id

        self.splash_id = splash_id
        self.app_store_id = app_store_id
        self.nav_bar = nav_bar

        self.playlist = 'content_playlist'
        self.image = 'content_image'

        self.label = 'content_label'
        self.cue = 'content_cue'
        self.code = 'content_code'

        self.interval = interval_id
        self.timer = 'content_timer'

        super().__init__(
            id=self.id,
            hidden=True,
            children=[
                dcc.Store(
                    id=self.playlist,
                    storage_type='session',
                    data=[]
                ),
                dcc.Store(
                    id=self.timer,
                    storage_type='session',
                    data={'next_action': 'prompt', 'next_interval': 0}
                ),
                dcc.Interval(
                    id=self.interval,
                    interval=1000,  # 1 second
                    disabled=True,
                ),
                dmc.Center(
                    dmc.Card(
                        children=[
                            dmc.CardSection(
                                dmc.Image(
                                    id=self.image,
                                    src=placeholder_image_src,
                                )
                            ),
                            dmc.CardSection(
                                dmc.Progress(
                                    id='progress',
                                    value=0,
                                    size='lg',
                                    radius='xs',
                                    striped=True,
                                    animated=True,
                                    mt='md',
                                    mb='xs',
                                ),
                            ),
                            dmc.CardSection(
                                dmc.Group(
                                    [
                                        dmc.Text(
                                            None,
                                            size='xl',
                                            id=self.cue,
                                        ),
                                        dmc.Text(
                                            None,
                                            size='xl',
                                            id=self.code,
                                        )
                                    ],
                                    justify='space-between',
                                    mt='md',
                                    mb='xs',
                                    id=self.label
                                ),
                            ),
                        ],
                        maw=400,
                    )
                )
            ]
        )

        self.register_callbacks()

    def register_callbacks(self):
        callback(
            output=dict(
                image=Output(self.image, 'src'),

                cue=Output(self.cue, 'children'),
                code=Output(self.code, 'children'),

                progress=Output('progress', 'value'),

                playlist=Output(self.playlist, 'data'),
                timer_state=Output(self.timer, 'data'),
                app_store=Output(self.app_store_id, 'data', allow_duplicate=True),

                interval_disabled=Output(self.interval, 'disabled', allow_duplicate=True)
            ),
            inputs=dict(
                n_intervals=Input(self.interval, 'n_intervals'),
            ),
            state=dict(
                playlist=State(self.playlist, 'data'),
                timer_state=State(self.timer, 'data'),
                format=State(self.nav_bar.format_picker.control_id, 'value'),
                topics=State(self.nav_bar.topic_picker.control_id, 'value'),
                prompt_display_seconds=State(self.nav_bar.playback_controls.prompt_display.control_id, 'value'),
                answer_display_seconds=State(self.nav_bar.playback_controls.answer_display.control_id, 'value'),
            ),
            prevent_initial_call=True,
        )(self.set_content)

    def set_content(
        self,
        n_intervals: int,
        playlist: list[Media],
        timer_state: dict[str, str | int],
        format: list[Format],
        topics: list[Topic],
        prompt_display_seconds: int,
        answer_display_seconds: int,
    ) -> dict[str, Any]:
        '''
            Handles each interval tick
        '''
        next_action = timer_state['next_action']
        next_interval = timer_state['next_interval']

        if n_intervals == 0:
            return self.start_new_session(format, topics, prompt_display_seconds)

        elif n_intervals == next_interval:
            if next_action == 'prompt':
                return self.show_prompt(n_intervals, playlist, prompt_display_seconds)

            if next_action == 'answer':
                return self.show_answer(n_intervals, timer_state, answer_display_seconds)

            # if you get here something is wrong with the timer state
        else:
            return self.tick(n_intervals, timer_state, prompt_display_seconds)

    def get_next_prompt(self, n_intervals: bool, source_playlist: list[Media], prompt_display_seconds: int) -> tuple[dict[str, Any], dict[str, str | int]]:
        '''
            Gets the next entry in the playlist

            Gets the next timer state depending on the format of the next entry

            In expressive mode, the image is displayed and the cue/code is held in timer state
            In receptive mode, the cue/code is displayed and the image is held in timer state

            Returns the next prompt and the timer state
        '''

        next_media, *remaining_playlist = source_playlist

        is_receptive = next_media['format'] == Format.RECEPTIVE

        next_image = next_media['url']
        next_cue = next_media.get('cue')
        next_code = next_media.get('code')

        timer_state = dict(
            next_action='answer',
            next_interval=n_intervals + prompt_display_seconds,

            # image is held in timer state in expressive mode
            next_image=None if is_receptive else next_image,

            # cue/code is held in timer state in receptive mode
            next_cue=next_cue if is_receptive else None,
            next_code=next_code if is_receptive else None,
        )

        next_prompt = dict(
            # image is displayed in receptive mode
            image=next_image if is_receptive else placeholder_image_src,

            # text displayed in expressive mode
            cue=None if is_receptive else next_cue,
            code=None if is_receptive else next_code,
        )

        return next_prompt, timer_state, remaining_playlist

    def start_new_session(self, format: list[Format], topics: list[Topic], prompt_display_seconds: int) -> dict[str, Any]:
        try:
            display_data, timer_state, remaining_playlist = self.get_next_prompt(
                0, get_new_playlist(format, topics), prompt_display_seconds)

            return dict(
                **display_data,
                timer_state=timer_state,
                playlist=remaining_playlist,
                progress=0,
                app_store=no_update,
                interval_disabled=False
            )

        except ValueError:
            return self.end_session()

    def show_prompt(self, n_intervals: int, old_playlist: list[Media], prompt_display_seconds) -> dict[str, Any]:
        '''
            Advances the playlist, updates the image and label content, shows/hides the image and label
            based on the current format, and updates the timer state.
        '''
        try:
            display_data, timer_state, remaining_playlist = self.get_next_prompt(
                n_intervals, old_playlist, prompt_display_seconds)

            return dict(
                **display_data,
                timer_state=timer_state,
                playlist=remaining_playlist,
                progress=0,
                app_store=no_update,
                interval_disabled=no_update
            )
        except ValueError:
            return self.end_session()

    def show_answer(self, n_intervals: int, timer_state: dict[str, str | int], answer_display_seconds: int) -> dict[str, Any]:
        '''
            Shows the answer from the timer state, and resets the timer state.
        '''
        display_data = dict(
            image=timer_state.get('next_image') or no_update,
            cue=timer_state.get('next_cue') or no_update,
            code=timer_state.get('next_code') or no_update,
        )

        timer_state = {
            'next_action': 'prompt',
            'next_interval': n_intervals + answer_display_seconds
        }

        return dict(
            **display_data,
            playlist=no_update,
            timer_state=timer_state,
            progress=100,
            app_store=no_update,
            interval_disabled=no_update
        )

    def tick(self, n_intervals, timer_state, prompt_display_seconds: int) -> dict[str, Any]:
        if timer_state['next_action'] == 'answer':
            # count up while displaying prompt
            elapsed_ticks = prompt_display_seconds - (timer_state['next_interval'] - n_intervals)

            return dict(
                image=no_update,
                cue=no_update,
                code=no_update,
                playlist=no_update,
                timer_state=no_update,
                progress=int(elapsed_ticks / prompt_display_seconds * 100),
                app_store=no_update,
                interval_disabled=no_update
            )

        else:
            raise PreventUpdate

    def end_session(self,) -> dict[str, Any]:
        '''
            Clears all content, disables the interval, resets the timer state, and displays the splash screeen
        '''
        return dict(
            image=None,
            cue=None,
            code=None,
            playlist=[],
            timer_state={
                'next_action': 'prompt',
                'next_interval': 0
            },
            progress=0,
            app_store=AppStore(active=self.splash_id, last=None, finished=True),
            interval_disabled=True
        )
