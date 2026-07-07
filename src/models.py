from enum import StrEnum
from typing import Dict, List, TypedDict


class Topic(StrEnum):
    PENALTIES = 'penalties'
    PACK = 'pack'
    JAMMER = 'jammer'
    OTHER = 'other'

    @classmethod
    def all(cls) -> List['Topic']:
        return [topic for topic in cls]

    @classmethod
    def get_options(cls) -> List[Dict[str, str]]:
        '''
            Returns a list of Topic options for an html input component
        '''
        return [{'label': topic.title(), 'value': topic} for topic in cls]


class Format(StrEnum):
    RECEPTIVE = 'receptive'
    BOTH = 'both'
    EXPRESSIVE = 'expressive'

    @classmethod
    def all(cls) -> List['Format']:
        return [format for format in cls]

    @classmethod
    def get_options(cls) -> List[Dict[str, str]]:
        '''
            Returns a list of Format options for an html input component
        '''
        return [{'label': format.title(), 'value': format} for format in cls]

    @classmethod
    def get_default_option(cls) -> 'Format':
        return cls.BOTH


class Clip(TypedDict):
    format: Format | None
    topic: Topic | None
    name: str
    url: str


class Media(TypedDict):
    topic: Topic
    format: Format
    rule: Dict[str, str] | None
    code: str | None
    cue: str
    alternate_cues: list[str] | None
    url: str


class AppStore(TypedDict):
    active: str
    last: str | None
    finished: bool
