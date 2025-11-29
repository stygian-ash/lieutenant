'''Tools for parsing, matching and manipulating word pronunciations and pronouncing dictionaries.'''

import re
from pathlib import Path
from functools import lru_cache
from dataclasses import dataclass

CMUDICT_PATH = Path(__file__).parent / 'resources' / 'cmudict' / 'cmudict.dict'

type Phonemes = tuple[str, ...]
type Dictionary = dict[str, set[Pronunciation]]


@dataclass(frozen=True)
class Pronunciation:
    '''A pronunciation of a word as a sequence of ARPABET 2-letter codes.'''
    word: str
    phonemes: Phonemes


def strip_stress(phonemes: Phonemes) -> Phonemes:
    '''Strip stress markers from phonemes.'''
    return tuple(
        re.sub(r'\d+', '', phoneme)
        for phoneme in phonemes
    )


def parse_cmudict_entry(line: str) -> Pronunciation:
    '''Parse an entry in the CMU Pronouncing Dictionary.'''
    if match := re.match(r'\s*([^)\s]+)(\(\d+\))?\s+([^#]+)(\s*#.+)?', line):
        return Pronunciation(
            word=match[1],
            phonemes=strip_stress(tuple(re.split(r'\s+', match[3].strip()))),
        )
    raise ValueError


@lru_cache
def load_cmudict() -> Dictionary:
    '''Load and return the CMU Pronouncing Dictionary.'''
    dictionary = {}
    with CMUDICT_PATH.open('r') as f:
        for line in f.readlines():
            entry = parse_cmudict_entry(line)
            if not entry.word in dictionary:
                dictionary[entry.word] = set()
            dictionary[entry.word].add(entry)
    return dictionary
