import pytest

from lieutenant import pronounce


class TestCMUDict:
    '''Test parsing of entries from the CMU Pronouncing Dictionary.'''

    def test_no_variant(self):
        assert pronounce.parse_cmudict_entry('amateur AE1 M AH0 T ER2') \
            == pronounce.Pronunciation(
                word='amateur',
                phonemes=('AE', 'M', 'AH', 'T', 'ER')
        )

    def test_variant(self):
        assert pronounce.parse_cmudict_entry('amateur(2) AE1 M AH0 CH ER2') \
            == pronounce.Pronunciation(
                word='amateur',
                phonemes=('AE', 'M', 'AH', 'CH', 'ER')
        )

    def test_whitespace(self):
        assert pronounce.parse_cmudict_entry('\t amateur\t  AE1\tM   AH0 T ER2 \n') \
            == pronounce.Pronunciation(
                word='amateur',
                phonemes=('AE', 'M', 'AH', 'T', 'ER')
        )

    def test_comment(self):
        assert pronounce.parse_cmudict_entry('aalsmeer AA1 L S M IH0 R # place, dutch') \
            == pronounce.Pronunciation(
                word='aalsmeer',
                phonemes=('AA', 'L', 'S', 'M', 'IH', 'R')
        )

    def test_empty(self):
        with pytest.raises(ValueError):
            pronounce.parse_cmudict_entry('')

    def test_abuse(self):
        assert len(pronounce.load_cmudict()['abuse']) == 2

    def test_aspirants(self):
        assert len(pronounce.load_cmudict()['aspirants']) == 4

    def test_nonexistent_word(self):
        assert 'nonexistent word' not in pronounce.load_cmudict()


def test_strip_stress():
    assert pronounce.strip_stress(('AE1', 'M', 'AH0', 'T', 'ER2')) \
        == ('AE', 'M', 'AH', 'T', 'ER')
