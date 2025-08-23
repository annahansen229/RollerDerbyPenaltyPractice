from dash import Dash, Input, Output, State, callback, dcc, html

app = Dash()

practice_formats = ['Expressive', 'Receptive']
signal_categories = ['Penalties', 'Pack Definition', 'Other']

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
]


@callback(
    Output('display', 'children'),
    inputs=dict(
        btn=Input('start_button', 'n_clicks')
    ),
    state=dict(
        practice_format=State('practice_format', 'value'),
        categories=State('category_checklist', 'value')
    )
)
def start_button_click(btn, practice_format, categories):
    return f'Format: {practice_format}, Categories: {', '.join(categories)}'


if __name__ == '__main__':
    app.run(debug=True)
