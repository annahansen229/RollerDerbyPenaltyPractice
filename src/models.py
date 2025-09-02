from dataclasses import dataclass
from enum import StrEnum
from typing import Dict, List


class Option(StrEnum):
    INTRO = 'intro'
    OUTRO = 'outro'

    @classmethod
    def label(cls, option: 'Option') -> str:
        return option.title()

    @classmethod
    def all(cls) -> List['Option']:
        return [o for o in cls]

    @classmethod
    def get_options(cls, clips: List['Clip'] = None, format: 'Format' = None) -> List[Dict[str, str]]:
        '''
            Returns a list of Option options for an html input
        '''
        if clips is None:
            return [{'label': f'Include {cls.label(option)}', 'value': option} for option in cls]
        else:
            available_options = []
            if any(cls.OUTRO in name for name in [clip.name for clip in clips]):
                available_options.append(cls.OUTRO)

            if any(cls.INTRO in name for name in [clip.name for clip in clips if format is None or clip.format == format]):
                available_options.append(cls.INTRO)

            return [{'label': f'Include {cls.label(option)}', 'value': option} for option in available_options]


class Topic(StrEnum):
    PENALTIES = 'penalties'
    PACK_STUFF = 'pack_stuff'
    JAMMER_STUFF = 'jammer_stuff'
    OTHER = 'other'

    @classmethod
    def label(cls, topic: 'Topic') -> str:
        return topic.replace('_', ' ').title()

    @classmethod
    def get_all(cls) -> List['Topic']:
        return [topic for topic in cls]

    @classmethod
    def get_options(cls, clips: List['Clip'] = None) -> List[Dict[str, str]]:
        '''
            Returns a list of Topic options for an html input component

            Args:
                clips (List[Clip]): (Optional) default None. When passed, options returned are filtered to only those \
                    that exist in the given list of clips
        '''
        return [{'label': cls.label(topic), 'value': topic} for topic in (cls if clips is None else {clip.topic for clip in clips if clip.topic is not None})]


class Format(StrEnum):
    EXPRESSIVE = 'expressive'
    RECEPTIVE = 'receptive'

    @classmethod
    def get_all(cls) -> List['Format']:
        return [f for f in cls]

    @classmethod
    def label(cls, format: 'Format') -> str:
        return format.title()

    @classmethod
    def get_options(cls, clips: List['Clip']) -> List[Dict[str, str]]:
        '''
            Returns a list of Format options for an html input component

            Args:
                clips (List[Clip]): (Optional) default None. When passed, options returned are filtered to only those \
                    that exist in the given list of clips
        '''
        result = [{'label': cls.label(f), 'value': f}
                  for f in (cls if clips is None else {clip.format for clip in clips if clip.format is not None})]

        return result

    @classmethod
    def get_default_option(cls) -> 'Format':
        return cls.EXPRESSIVE


@dataclass
class Clip:
    format: Format | None
    topic: Topic | None
    name: str
    url: str
