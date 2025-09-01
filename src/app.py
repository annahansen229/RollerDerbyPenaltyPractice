
from dataclasses import asdict
from typing import Dict, Union

from dash import Dash, Input, Output, State, callback, dcc, html

from src.clips import clips, get_playlist
from src.components import Player
from src.models import Category, Format, Option

app = Dash()

# Requires Dash 2.17.0 or later

player = Player(id='player', store='store')

app.layout = [
    dcc.Store(id='store', storage_type='session', data=[]),
    html.Div(
        children='Roller Derby Hand Signals and Verbal Cues Practice',
    ),
    html.Div(
        dcc.RadioItems(
            id='format',
            options=Format.get_options(clips),
            value=Format.get_default_option(),
        ),
        hidden=True
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
    ),
    player,
]


@callback(
    output=dict(
        store=Output('store', 'data', allow_duplicate=True,),
        start_button_text=Output('start_button', 'children', allow_duplicate=True,),
        url=Output(player.video, 'url', allow_duplicate=True, ),
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
    '''
        When the start button is clicked, get the playlist based on the selected options and
        set the store contents and url of the first video
    '''
    first_video, *remaining_playlist = get_playlist(format, categories, options)

    return dict(
        store=[asdict(clip) for clip in remaining_playlist],
        start_button_text='Restart',
        url=first_video.url
    )


if __name__ == '__main__':
    app.run(debug=True)
