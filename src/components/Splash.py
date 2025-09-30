from typing import Dict, List

import dash_mantine_components as dmc
from dash import Input, Output, callback, html
from dash_iconify import DashIconify

from src.components import Player


class Splash(html.Div):
    '''
        Renders the Welcome component. 

        Args:
            player (Player): The Player component
    '''

    def __init__(self, player: Player):
        self.welcome = 'splash_welcome'
        self.finished = 'splash_finished'

        self.welcome_content = dmc.Collapse(
            [
                dmc.Card(
                    [
                        dmc.CardSection(
                            dmc.Text(
                                'Welcome to the Roller Derby Penalty Hand Signals and Verbal Cues Practice App!',
                            ),
                            inheritPadding=True,
                            mt='sm'
                        ),
                        dmc.CardSection(
                            [
                                dmc.Text(
                                    "Practice Format Options",
                                    fw=500,
                                ),
                                dmc.Text(children=[
                                    dmc.Text('Choose ', span=True,),
                                    dmc.Text('Expressive Format', span=True, c='grape', inherit=True,),
                                    ' to hear and see the verbal cue, and then perform the correct hand signal.'
                                ]),
                                dmc.Text(children=[
                                    dmc.Text('Choose ', span=True,),
                                    dmc.Text('Receptive Format', span=True, c='grape', inherit=True,),
                                    ' to see the hand signal, and then say the correct verbal cue.'
                                ]),
                            ],
                            inheritPadding=True,
                            mt='sm'
                        ),
                        dmc.CardSection(
                            [
                                dmc.Text(
                                    "Topic Areas",
                                    fw=500,
                                ),
                                dmc.Text(children=[
                                    dmc.Text('Choose ', span=True,),
                                    dmc.Text('Penalties', span=True, c='grape', inherit=True,),
                                    ' to practice cues and signals related to issuing penalties.'
                                ]),
                                dmc.Text(children=[
                                    dmc.Text('Choose ', span=True,),
                                    dmc.Text('Pack', span=True, c='grape', inherit=True,),
                                    ' to practice cues and signals related to pack definition and engagement zone.'
                                ]),
                                dmc.Text(children=[
                                    dmc.Text('Choose ', span=True,),
                                    dmc.Text('Jammer', span=True, c='grape', inherit=True,),
                                    ' to practice cues and signals related to jammers.'
                                ]),
                                dmc.Text(children=[
                                    dmc.Text('Choose ', span=True,),
                                    dmc.Text('Other', span=True, c='grape', inherit=True,),
                                    ' to practice other cues and signals that you may see on the track.'
                                ]),

                            ],
                            inheritPadding=True,
                            mt='sm'
                        ),
                        dmc.CardSection(
                            [
                                dmc.Text(
                                    "Other Options",
                                    fw=500,
                                ),
                                dmc.Text(children=[
                                    'Include the ',
                                    dmc.Text('Intro', span=True, c='grape', inherit=True,),
                                    ' to hear a brief verbal explanation of how this practice works.'
                                ]),
                                dmc.Text(children=[
                                    'Include the ',
                                    dmc.Text('Outro', span=True, c='grape', inherit=True,),
                                    ' to hear some parting words after you have completed practice.'
                                ]),
                            ],
                            inheritPadding=True,
                            mt='sm',
                        ),
                        dmc.CardSection(
                            [
                                dmc.Text(children=[
                                    'When you click ',
                                    dmc.Text('Start', span=True, c='grape', inherit=True,),
                                    ' all the clips for your selected topics will be shuffled and played for you in a random order.'
                                ]),
                                dmc.Text(children=[
                                    'Click ',
                                    dmc.Text('Restart', span=True, c='grape', inherit=True,),
                                    ' to start over with a new random order.'
                                ]),
                            ],
                            inheritPadding=True,
                            mt='sm',
                            mb='sm'
                        ),
                    ],
                    withBorder=True
                )
            ],
            id=self.welcome,
            opened=True,
        )

        self.finished_content = dmc.Collapse(
            [
                dmc.Card(
                    [
                        dmc.CardSection(
                            dmc.Text(
                                'Congratulations! You finished your practice Session!',
                            ),
                            inheritPadding=True,
                            mt='sm'
                        ),
                        dmc.CardSection(
                            dmc.Text(
                                'Use the controls in the side bar to try again.',
                            ),
                            inheritPadding=True,
                            mt='sm'
                        ),
                        dmc.CardSection(
                            dmc.Text(
                                'Practice your hand signals and verbal cues every day and you will learn them in no time!',
                            ),
                            inheritPadding=True,
                            mt='sm',
                        ),
                        dmc.CardSection(
                            dmc.Button(
                                'Start Over',
                                leftSection=DashIconify(icon='iconamoon:restart-bold'),
                                id='restart',
                                fullWidth=False
                            ),
                            inheritPadding=True,
                            mt='sm',
                            mb='sm'
                        )

                    ],
                    withBorder=True
                )
            ],
            id=self.finished,
            opened=False,
        )

        super().__init__(
            children=[
                self.welcome_content,
                self.finished_content,
            ],
        )

        @callback(
            output=dict(
                welcome_open=Output(self.welcome, 'opened', allow_duplicate=True),
                finished_open=Output(self.finished, 'opened', allow_duplicate=True)
            ),
            inputs=dict(
                playing=Input(player.video, 'playing'),
                finished=Input(player.finished, 'data'),
            ),
            prevent_initial_call=True,
        )
        def toggle_content(playing: bool, finished: bool) -> Dict[str, bool | List]:
            return dict(
                welcome_open=False if playing else not finished,
                finished_open=False if playing else finished,
            )

        @callback(
            Input('restart', 'n_clicks'),
            output=dict(
                welcome_open=Output(self.welcome, 'opened', allow_duplicate=True),
                finished_open=Output(self.finished, 'opened', allow_duplicate=True),
                mobile_burger=Output('mobile-burger', 'opened', allow_duplicate=True),
                desktop_burger=Output('desktop-burger', 'opened', allow_duplicate=True),
            ),
            prevent_initial_call=True,
        )
        def restart(_):
            return dict(
                welcome_open=True,
                finished_open=False,
                mobile_burger=True,
                desktop_burger=True,
            )
