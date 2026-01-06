import random
from pathlib import Path
from typing import List

from src.models import Clip, Format, Option, Topic


def get_clips() -> List[Clip]:
    '''
        Gets all clips in the static directory and organizes them by topic and format

        Clips are expected to be organized like `static/{Format}/{Topic}/{*.mp4}`

        If the subfolder names are not valid `Format`s or `Topic`s, the video is not included in the return value.
    '''
    all_files = [f.relative_to('src') for f in Path("src/static/").rglob('*') if f.is_file()]

    clips = []

    for f in all_files:
        try:
            if "intro" in f.name:
                format = Format(f.parent.name)
                topic = None
            elif "outro" in f.name:
                format = None
                topic = None
            else:
                topic = Topic(f.parent.name)
                format = Format(f.parent.parent.name)

            clips.append(Clip(format=format, topic=topic, name=f.name, url=str(f)))
        except ValueError:
            pass

    return clips


clips = get_clips()


def get_sub_playlist(format: Format, topics: List[Topic], include_intro: bool) -> List[Clip]:
    '''
        Gets all clips for the given format and topics, and shuffles their order.
        When `include_intro=True`, the intro clip for that format is included at the beginning
    '''
    relevant_clips = [c for c in clips if c['format'] == format and c['topic'] in topics]

    random.shuffle(relevant_clips)

    if include_intro:
        intro = next((c for c in clips if Option.INTRO in c['name'] and format == c['format']), None)
        if intro:
            relevant_clips.insert(0, intro)

    return relevant_clips


def get_playlist(format: Format, topics: List[Topic], options: List[Option]) -> List[Clip]:
    '''
        Gets clips for the given formats and topics.
        Content for each format is grouped together.
        The outro clip is included at the end, when selected.
    '''
    playlist = []

    if format == Format.BOTH:
        selected_formats = [Format.RECEPTIVE, Format.EXPRESSIVE]
    else:
        selected_formats = [format]

    for f in selected_formats:
        playlist.extend(get_sub_playlist(f, topics, Option.INTRO in options))

    if Option.OUTRO in options:
        outro = next((c for c in clips if Option.OUTRO in c['name']), None)
        if outro:
            playlist.append(outro)

    return playlist
