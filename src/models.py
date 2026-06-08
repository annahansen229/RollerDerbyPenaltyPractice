from enum import StrEnum
from typing import TypedDict


class Option(StrEnum):
    INTRO = 'intro'
    OUTRO = 'outro'

    def label(self) -> str:
        return f'Include {self.title()}'

    @classmethod
    def all(cls) -> list['Option']:
        return [option for option in cls]

    @classmethod
    def get_options(cls) -> list[dict[str, str]]:
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
    def all(cls) -> list['Topic']:
        return [topic for topic in cls]

    @classmethod
    def get_options(cls) -> list[dict[str, str]]:
        '''
            Returns a list of Topic options for an html input component
        '''
        return [{'label': topic.title(), 'value': topic} for topic in cls]


class PlaybackMode(StrEnum):
    AUTOMATIC = 'automatic'
    MANUAL = 'manual'

    @classmethod
    def get_options(cls) -> list[dict[str, str]]:
        '''
            Returns a list of PlaybackFormat options for an html input component
        '''
        return [{'label': format.title(), 'value': format} for format in cls]

    @classmethod
    def get_default_option(cls) -> 'PracticeFormat':
        return cls.AUTOMATIC


class MediaFormat(StrEnum):
    VIDEO = 'video'
    IMAGE = 'image'

    @classmethod
    def get_options(cls) -> list[dict[str, str]]:
        '''
            Returns a list of MediaFormat options for an html input component
        '''
        return [{'label': format.title(), 'value': format} for format in cls]

    @classmethod
    def get_default_option(cls) -> 'PracticeFormat':
        return cls.VIDEO


class PracticeFormat(StrEnum):
    RECEPTIVE = 'receptive'
    BOTH = 'both'
    EXPRESSIVE = 'expressive'

    @classmethod
    def all(cls) -> list['PracticeFormat']:
        return [format for format in cls]

    @classmethod
    def get_options(cls) -> list[dict[str, str]]:
        '''
            Returns a list of PracticeFormat options for an html input component
        '''
        return [{'label': format.title(), 'value': format} for format in cls]

    @classmethod
    def get_default_option(cls) -> 'PracticeFormat':
        return cls.BOTH


class Media(TypedDict):
    practice_format: PracticeFormat | None
    media_format: MediaFormat
    topic: Topic | None
    name: str
    url: str


class AppStore(TypedDict):
    active: str
    last: str | None
    finished: bool
