from lieutenant.pronounce import load_cmudict, parse_cmudict_entry
from lieutenant.major import decode


def decode_cmu(entry: str) -> str:
    '''Decode a pronunciation as given in cmudict.'''
    return decode.decode_pronunciation(
        parse_cmudict_entry(entry)
    )


class TestDecodePronunciation:
    def test_meteor(self):
        assert decode_cmu('meteor M IY1 T IY0 ER0') == '314'

    def test_amateur_1(self):
        assert decode_cmu('amateur AE1 M AH0 T ER2') == '314'

    def test_amateur_2(self):
        assert decode_cmu('amateur(2) AE1 M AH0 CH ER2') == '364'

    def test_aboard(self):
        assert decode_cmu('aboard AH0 B AO1 R D') == '941'

    def test_a(self):
        assert decode_cmu('a AH0') == ''

    def test_antidisestablishmentarianism(self):
        assert decode_cmu('antidisestablishmentarianism AE2 N T AY0 D IH2 S AH0 S T AE2 B L IH0 SH M AH0 N T EH1 R IY0 AH0 N IH2 Z AH0 M') \
            == '2110019563214203'


class TestDecodeFromDict:
    def test_meteor(self):
        assert decode.decode_from_dictionary(
            'meteor', load_cmudict()) == {'314'}

    def test_amateur(self):
        assert decode.decode_from_dictionary(
            'amateur', load_cmudict()) == {'314', '364'}
