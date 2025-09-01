import random
from pathlib import Path
from typing import List

from src.models import Category, Clip, Format, Option


def get_clips() -> List[Clip]:
    '''
        Gets all clips in the static directory and organizes them by category and format

        Clips are expected to be organized like `static/{Format}/{Category}/{*.mp4}`

        If the subfolder names are not valid `Format`s or `Category`s, the video is not included in the return value.
    '''
    all_files = [f.relative_to('src') for f in Path("src/static/").rglob('*') if f.is_file()]

    clips = []

    for f in all_files:
        try:
            if "intro" in f.name:
                format = Format(f.parent.name)
                category = None
            elif "outro" in f.name:
                format = None
                category = None
            else:
                category = Category(f.parent.name)
                format = Format(f.parent.parent.name)

            clips.append(Clip(format, category, f.name, str(f)))
        except ValueError:
            pass

    return clips


clips = get_clips()


def shuffle_clips(format: Format, categories: List[Category]) -> List[Clip]:
    relevant_clips = [c for c in clips if c.format == format and c.category in categories]

    random.shuffle(relevant_clips)

    return relevant_clips


def get_playlist(format: Format, categories: List[Category], options: List[Option]) -> List[Clip]:
    playlist = []

    if Option.INTRO in options:
        intro = next((c for c in clips if Option.INTRO in c.name and format == c.format), None)
        if intro:
            playlist.append(intro)

    playlist.extend(shuffle_clips(format, categories))

    if Option.OUTRO in options:
        outro = next((c for c in clips if Option.OUTRO in c.name), None)
        if outro:
            playlist.append(outro)

    return playlist
