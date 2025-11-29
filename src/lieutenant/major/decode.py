'''Decode a word to a number using the major system.'''

from lieutenant.pronounce import Pronunciation, Dictionary

DIGIT_MAPPINGS = {
    '0': {'S', 'Z'},
    '1': {'T', 'TH', 'D', 'DH', 'DX'},
    '2': {'N', 'EN', 'NG', 'NX'},
    '3': {'M', 'EM'},
    '4': {'R', 'AXR', 'ER'},
    '5': {'L', 'EL'},
    '6': {'JH', 'CH', 'ZH', 'SH'},
    '7': {'K', 'G'},
    '8': {'F', 'V'},
    '9': {'P', 'B'}
}

PHONEME_MAPPINGS = {
    phoneme: digit
    for digit, phonemes in DIGIT_MAPPINGS.items()
    for phoneme in phonemes
}


def decode_pronunciation(pronunciation: Pronunciation) -> str:
    '''Decode a particular pronunciation of a word to its value under the major system.'''
    return ''.join(
        PHONEME_MAPPINGS.get(phoneme, '')
        for phoneme in pronunciation.phonemes
    )


def decode_from_dictionary(word: str, dictionary: Dictionary) -> set[str]:
    '''Decode a word using all its pronunciations listed in a dictionary.'''
    if pronunciations := dictionary.get(word):
        return set(map(decode_pronunciation, pronunciations))
    raise ValueError(f'Word "{word}" is not listed in dictionary')
