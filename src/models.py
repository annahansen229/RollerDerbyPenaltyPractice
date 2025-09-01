from dataclasses import dataclass
from enum import StrEnum
from typing import Dict, List


class Option(StrEnum):
    INTRO = 'intro'
    OUTRO = 'outro'

    @classmethod
    def title(cls, option: 'Option') -> str:
        return option.title()

    @classmethod
    def all(cls) -> List['Option']:
        return [o for o in cls]

    @classmethod
    def options(cls) -> List[Dict[str, str]]:
        '''
            Returns a list of Option options for an html input
        '''
        return [{'label': f'Include {cls.title(o)}', 'value': o} for o in cls]


class Category(StrEnum):
    PENALTIES = 'penalties'
    PACK_STUFF = 'pack_stuff'
    JAMMER_STUFF = 'jammer_stuff'
    OTHER = 'other'

    @classmethod
    def label(cls, category: 'Category') -> str:
        return category.replace('_', ' ').title()

    @classmethod
    def get_all(cls) -> List['Category']:
        return [f for f in cls]

    @classmethod
    def get_options(cls, clips: List['Clip'] = None) -> List[Dict[str, str]]:
        '''
            Returns a list of Category options for an html input component

            Args:
                clips (List[Clip]): (Optional) default None. When passed, options returned are filtered to only those \
                    that exist in the given list of clips
        '''
        return [{'label': cls.label(c), 'value': c} for c in (cls if clips is None else {clip.category for clip in clips if clip.category is not None})]


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
    category: Category | None
    name: str
    url: str
