from typing import Dict, List, Union

import dash_mantine_components as dmc
from dash import Input, Output, State, callback, no_update
from dash_iconify import DashIconify

from .MediaFormatPicker import MediaFormatPicker
from .IntroOutroPicker import IntroOutroPicker
from .PracticeFormatPicker import PracticeFormatPicker
from .TopicPicker import TopicPicker
from .PlaybackModePicker import PlaybackModePicker
from src.media import get_playlist
from src.components import VideoPlayer
from src.models import AppStore, PracticeFormat, Option, Topic, MediaFormat


class NavBar(dmc.AppShellNavbar):
    '''
        Renders the Options control component

        Args:
            player (VideoPlayer): The video player component
            contact_form (str): The identifier of the contact form component
            app_store (str): The identifier of the app store
    '''

    def __init__(self, video_player: VideoPlayer, contact_form: str, app_store: str):
        self.contact_button_id = 'contact_button'
        self.start_button_id = 'start_button'

        super().__init__(
            id='navbar',
            children=[
                dmc.ScrollArea(
                    children=[
                        dmc.Accordion(
                            children=[
                                PracticeFormatPicker(),
                                TopicPicker(self.start_button_id),
                                MediaFormatPicker(),
                                IntroOutroPicker(),
                                PlaybackModePicker(),
                            ],
                            multiple=True,
                            variant='contained',
                            mb=10,
                        ),

                        dmc.Button(
                            'Start',
                            id=self.start_button_id,
                            rightSection=DashIconify(icon='flowbite:chevron-double-right-outline'),
                            variant='filled',
                            my=10,
                            fullWidth=True,
                        ),
                    ],
                    mb=10
                ),

                dmc.Button(
                    'Contact Us',
                    id=self.contact_button_id,
                    mt='auto',
                    fullWidth=True,
                ),
            ],
            p='md'
        )

        @callback(
            output=dict(
                player_store=Output(video_player.store, 'data', allow_duplicate=True,),
                start_button_text=Output(self.start_button_id, 'children', allow_duplicate=True,),
                url=Output(video_player.video, 'url', allow_duplicate=True, ),
                mobile_burger=Output('mobile-burger', 'opened', allow_duplicate=True),
                desktop_burger=Output('desktop-burger', 'opened', allow_duplicate=True),
                app_store=Output(app_store, 'data', allow_duplicate=True)
            ),
            inputs=dict(
                btn=Input(self.start_button_id, 'n_clicks')
            ),
            state=dict(
                media_format=State('media-format', 'value'),
                practice_format=State('practice-format', 'value'),
                topics=State('topics', 'value'),
                options=State('options', 'value'),
            ),
            prevent_initial_call=True
        )
        def start_button_click(media_format: MediaFormat, practice_format: PracticeFormat, topics: List[Topic], options: List[Option], **kwargs) -> Dict[str, Union[bool, str, Dict]]:
            '''
                When the start button is clicked, get the playlist based on the selected options, and
                set the store contents and url of the first entry
            '''
            first_entry, *remaining_playlist = get_playlist(media_format, practice_format, topics, options)

            return dict(
                player_store=remaining_playlist,
                start_button_text='Restart',
                url=first_entry['url'],
                mobile_burger=False,
                desktop_burger=False,
                app_store=AppStore(active=video_player.id, last=None, finished=False),
            )

        @callback(
            output=dict(
                contact_button_text=Output(self.contact_button_id, 'children'),
                app_store=Output(app_store, 'data', allow_duplicate=True),
                playing=Output(video_player.video, 'playing', allow_duplicate=True)
            ),
            inputs=dict(
                btn=Input(self.contact_button_id, 'n_clicks')
            ),
            state=dict(
                currently_hidden=State(contact_form, 'hidden'),
                old_app_store=State(app_store, 'data'),
            ),
            prevent_initial_call=True
        )
        def contact_button_click(currently_hidden, old_app_store: Dict[str, str], **kwargs) -> Dict[str, Union[bool, str]]:
            '''
                Hides/Shows the contact form, modifies the contact button text based on new state, and
                pauses playback if mid-session
            '''
            if currently_hidden:
                last = old_app_store.get('active')
                return dict(
                    contact_button_text='Close Contact Form',
                    app_store=AppStore(
                        active=contact_form,
                        last=last,
                        finished=old_app_store.get('finished')
                    ),
                    playing=False if last == video_player.id else no_update
                )

            else:
                active = old_app_store.get('last')
                return dict(
                    contact_button_text='Contact Us',
                    app_store=AppStore(
                        active=active,
                        last=contact_form,
                        finished=old_app_store.get('finished')
                    ),
                    playing=True if active == video_player.id else no_update
                )
