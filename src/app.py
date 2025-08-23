import dash_player as dp
from dash import Dash, Input, Output, State, callback, dcc, html, no_update

practice_formats = ['Expressive', 'Receptive']
signal_categories = ['Penalties', 'Pack Definition', 'Other']

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [
    html.Div(
        children='Roller Derby Hand Signals and Verbal Cues Practice',
    ),
    html.Div(
        id='display',
        children=None
    ),
    dcc.RadioItems(
        id='practice_format',
        options=practice_formats
    ),
    dcc.Checklist(
        id='category_checklist',
        options=signal_categories,
        value=signal_categories,
    ),
    html.Button(
        id='start_button',
        children='Start'
    ),
    html.Button(
        id='stop_button',
        children='Stop'
    ),
    dp.DashPlayer(id='player', url='/static/BigBuckBunny.mp4', playing=False),
    html.Div(
        id='current_time',
        children=None,
    ),
    html.Div(
        id='duration',
        children=None,
    )
]


@callback(
    output=dict(
        display=Output('display', 'children'),
        playing=Output('player', 'playing', allow_duplicate=True,)
    ),
    inputs=dict(
        btn=Input('start_button', 'n_clicks')
    ),
    state=dict(
        practice_format=State('practice_format', 'value'),
        categories=State('category_checklist', 'value')
    ),
    prevent_initial_call=True
)
def start_button_click(practice_format, categories, **kwargs):
    return {
        'display': f'Format: {practice_format}, Categories: {', '.join(categories)}',
        'playing': True
    }


@callback(
    Output('player', 'playing', allow_duplicate=True,),
    inputs=dict(
        btn=Input('stop_button', 'n_clicks')
    ),
    prevent_initial_call=True
)
def stop_button_click(**kwargs):
    False


@callback(
    Output('current_time', 'children'),
    Input('player', 'currentTime'),
)
def display_current_time(current_time):
    return f'Current Time: {current_time}'


@callback(
    Output('duration', 'children'),
    Input('player', 'duration'),
)
def display_duration(duration):
    return f'Duration: {duration}'


@callback(
    Output('player', 'url'),
    Input('player', 'currentTime'),
    State('player', 'duration'),
    prevent_initial_call=True
)
def play_next_video(current_time, duration):
    if current_time == duration or current_time > 10:
        return 'static/ElephantsDream.mp4'
    else:
        return no_update


if __name__ == '__main__':
    app.run(debug=True)
