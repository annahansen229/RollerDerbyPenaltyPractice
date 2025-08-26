
from typing import Dict, List, Union

import dash_player as dp
from dash import Dash, Input, Output, State, callback, dcc, html, no_update

from src.clips import clips, get_playlist
from src.models import Category, Clip, Format, Option

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [
    dcc.Store(id='store', storage_type='session', data=[]),
    html.Div(
        children='Roller Derby Hand Signals and Verbal Cues Practice',
    ),
    dcc.RadioItems(
        id='format',
        options=Format.get_options(clips),
        value=Format.get_default_option(),
    ),
    dcc.Checklist(
        id='categories',
        options=Category.get_options(clips),
        value=Category.get_all(),
    ),
    dcc.Checklist(
        id='options',
        options=Option.all(),
        value=[],
    ),
    html.Button(
        id='start_button',
        children='Start'
        # TODO "restart" after start ("start over?")
    ),
    dp.DashPlayer(id='player', url=None, playing=False),
    html.Button(
        id='play_button',
        children='Play',
        # TODO don't show until after start
        # TODO "pause" when playing, "play" when paused
    ),
]


@callback(
    output=dict(
        playing=Output('player', 'playing', allow_duplicate=True,),
        url=Output('player', 'url', allow_duplicate=True,),
        store=Output('store', 'data', allow_duplicate=True,),
        start_button_text=Output('start_button', 'children', allow_duplicate=True,)
    ),
    inputs=dict(
        btn=Input('start_button', 'n_clicks')
    ),
    state=dict(
        format=State('format', 'value'),
        categories=State('categories', 'value'),
        options=State('options', 'value'),
    ),
    prevent_initial_call=True
)
def start_button_click(format, categories, options, **kwargs) -> Dict[str, Union[bool, str, Dict]]:
    playlist = get_playlist(format, categories, options)
    first_video = playlist.pop(0)
    return dict(
        playing=True,
        url=first_video.url,
        store=playlist,
        start_button_text='Restart'
    )


@callback(
    output=dict(
        url=Output('player', 'url', allow_duplicate=True,),
        store=Output('store', 'data', allow_duplicate=True,),
        playing=Output('player', 'playing', allow_duplicate=True,),
    ),
    inputs=dict(
        current_time=Input('player', 'currentTime'),
    ),
    state=dict(
        duration=State('player', 'duration'),
        store=State('store', 'data'),
    ),
    prevent_initial_call=True
)
def play_next_video(current_time: float, duration: float, store: List[Clip]):
    if current_time == duration:
        # video has reached the end
        try:
            next_video, *new_playlist = store
            url = next_video.url
            store = new_playlist
            playing = True
        except ValueError:
            # end of the playlist
            url = None
            store = []
            playing = False
    else:
        # video still in progress
        url = no_update
        store = no_update
        playing = no_update

    return dict(
        url=url,
        store=store,
        playing=playing,
    )


if __name__ == '__main__':
    app.run(debug=True)
