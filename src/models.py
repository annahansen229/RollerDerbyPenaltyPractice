from dataclasses import dataclass
from enum import StrEnum
from typing import Dict, List


class Option(StrEnum):
    INTRO = 'intro'
    OUTRO = 'outro'

    def label(self) -> str:
        return f'Include {self.title()}'

    @classmethod
    def all(cls) -> List['Option']:
        return [option for option in cls]

    @classmethod
    def get_options(cls) -> List[Dict[str, str]]:
        '''
            Returns a list of Option options for an html input
        '''
        return [{'label': option.label(), 'value': option} for option in cls]


class Topic(StrEnum):
    PENALTIES = 'penalties'
    PACK = 'pack'
    JAMMER = 'jammer'
    OTHER = 'other'

    @classmethod
    def sort(cls, members):
        '''
            Sort an iterable of Topic members in definition order
        '''
        order = {topic: i for i, topic in enumerate(cls)}
        return sorted(members, key=order.get)

    @classmethod
    def label(cls, topic: 'Topic') -> str:
        return topic.title()

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
        return [{'label': cls.label(topic), 'value': topic} for topic in (cls if clips is None else cls.sort({clip.topic for clip in clips if clip.topic is not None}))]


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
