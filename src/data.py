import random
from pathlib import Path

from src.models import Format, Media, Topic

placeholder_image_src = "static/400.svg"

data = {
    Topic.PENALTIES: [
        {
            'cue': 'Back Block',
            'code': 'B',
        },
        {
            'cue': 'High Block',
            'code': 'A',
        },
        {
            'cue': 'Low Block',
            'code': 'L',
        },
        {
            'cue': 'Head Block',
            'code': 'H',
        },
        {
            'cue': 'Forearm',
            'code': 'F',
        },
        {
            'cue': 'Leg Block',
            'code': 'E',
        },
        {
            'cue': 'Illegal Contact',
            'code': 'C',
            'alternate cues': ['Illegal Assist', 'Early Hit']
        },
        {
            'cue': 'Direction',
            'code': 'D',
            'alternate cues': ['Stop Block']
        },
        {
            'cue': 'Multiplayer',
            'code': 'M',
        },
        {
            'cue': 'Illegal Position',
            'code': 'P',
            'alternate cues': [
                'Destruction',
                'Skating Out of Bounds',
                'Failure to Reform',
                'Failure to Return',
                'Failure to Yield',
            ]
        },
        {
            'cue': 'Cut',
            'code': 'X',
            'alternate cues': ['Illegal Re-Entry',]
        },
        {
            'cue': 'Interference',
            'code': 'N',
            'alternate cues': ['Delay of Game',]
        },
        {
            'cue': 'Illegal Procedure',
            'code': 'I',
            'alternate cues': ['Star Pass Violation', 'Star Pass Interference']
        },
        {
            'cue': 'Misconduct',
            'code': 'G',
            'alternate cues': ['Insubordination']
        },
    ],
    Topic.PACK: [
        {'cue': 'No Pack'},
        {'cue': 'Out of Play'},
        {'cue': 'Pack is Here'},
    ],
    Topic.OTHER: [
        {'cue': 'Official Review'},
        {'cue': 'Official Timeout'},
        {'cue': 'Report to the Box'},
        {'cue': 'Return to the Track'},
        {'cue': 'Return to your Bench'},
        {'cue': 'Team Timeout'},
        {'cue': 'Two Penalties'},
    ],
    Topic.JAMMER: [
        {'cue': 'Jam Ending'},
        {'cue': 'Lead Jammer'},
        {'cue': 'No Earned Pass'},
        {'cue': 'Not Lead Jammer'},
        {'cue': 'Star Pass Complete'},
    ]
}


def get_file_url(cue: str) -> str:
    try:
        return next(
            (
                str(f.relative_to('src'))
                for f in Path("src/static/").iterdir()
                if f.is_file() and f.stem.lower() == cue.lower()
            )
        )
    except StopIteration:
        return placeholder_image_src


def get_media(topic: str, format: str) -> list[Media]:
    return [
        Media(
            topic=topic,
            format=format,
            cue=entry.get('cue', None),
            code=entry.get('code', None),
            url=get_file_url(entry.get('cue', None))
        )
        for entry in data[topic]
    ]


def get_sub_playlist(format: Format, topics: list[Topic]) -> list[Media]:
    '''
        Gets all content for the given format and topics, and shuffles their order.
    '''
    playlist = [
        media
        for topic in topics
        for media in get_media(topic, format)
    ]

    random.shuffle(playlist)

    return playlist


def get_new_playlist(format: Format, topics: list[Topic]) -> list[Media]:
    '''
        Gets all content for the given formats and topics
        Content for each format is grouped together.
    '''
    if format == Format.BOTH:
        selected_formats = [Format.RECEPTIVE, Format.EXPRESSIVE]
    else:
        selected_formats = [format]

    playlist = [
        media
        for format in selected_formats
        for media in get_sub_playlist(format, topics)
    ]

    return playlist
