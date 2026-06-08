import random
from pathlib import Path

from src.models import Media, PracticeFormat, Option, Topic, MediaFormat


def get_media() -> list[Media]:
    '''
        Gets all media in the static directory.

        Media is expected to be organized like `static/{MediaFormat}/{Topic}/{PracticeFormat}/{*.mp4}`

        If the subfolder names are not valid `MediaFormats`, `PracticeFormat`s or `Topic`s, the video is not included in the return value.
        (PracticeFormat is only applicable to video files)
    '''
    all_files = [f.relative_to('src') for f in Path("src/static/").rglob('*') if f.is_file()]

    media = []

    for f in all_files:
        parts = f.parts

        try:
            media_format = MediaFormat(parts[parts.index('static') + 1].removeprefix('s'))
            topic = None
            practice_format = None

            if media_format == MediaFormat.VIDEO:
                if "intro" in f.name:
                    practice_format = PracticeFormat(f.stem.removeprefix('intro').strip('-'))
                elif "outro" in f.name:
                    pass
                else:
                    practice_format = PracticeFormat(f.parent.name)
                    topic = Topic(f.parent.parent.name)

            elif media_format == MediaFormat.IMAGE:
                topic = Topic(f.parent.parent.name)

            media.append(
                Media(
                    media_format=media_format,
                    practice_format=practice_format,
                    topic=topic,
                    name=f.name,
                    url=str(f)
                )
            )

        except ValueError:
            pass

    return media


all_media = get_media()


def media_is_relevant(media: Media, media_format: MediaFormat, practice_format: PracticeFormat, topics: list[Topic]) -> bool:
    relevant_media_format = media['media_format'] == media_format
    relevant_practice_format = media['practice_format'] == practice_format
    relevant_topic = media['topic'] in topics

    return relevant_media_format and relevant_practice_format and relevant_topic


def get_sub_playlist(media_format: MediaFormat, practice_format: PracticeFormat, topics: list[Topic], include_intro: bool) -> list[Media]:
    '''
        Gets all media entries for the given attributes, and shuffles their order.
        When `include_intro=True`, the intro clip for the format is included at the beginning (only applicable to video).
    '''
    relevant_media = [m for m in all_media if media_is_relevant(m, media_format, practice_format, topics)]

    random.shuffle(relevant_media)

    if include_intro:
        intro = next(
            (m for m in all_media if Option.INTRO in m['name'] and practice_format == m['practice_format']),
            None
        )
        if intro:
            relevant_media.insert(0, intro)

    return relevant_media


def get_playlist(media_format: MediaFormat, practice_format: PracticeFormat, topics: list[Topic], options: list[Option]) -> list[Media]:
    '''
        Gets media for the given attributes.
        Content for each format is grouped together.
        The outro clip is included at the end, when selected.
    '''
    playlist = []

    if practice_format == PracticeFormat.BOTH:
        selected_practice_formats = [PracticeFormat.RECEPTIVE, PracticeFormat.EXPRESSIVE]
    else:
        selected_practice_formats = [practice_format]

    for pf in selected_practice_formats:
        playlist.extend(get_sub_playlist(media_format=media_format, practice_format=pf,
                        topics=topics, include_intro=Option.INTRO in options))

    if Option.OUTRO in options:
        outro = next((c for c in all_media if Option.OUTRO in c['name']), None)
        if outro:
            playlist.append(outro)

    return playlist
