from lieutenant.major import encode
from lieutenant.pronounce import load_cmudict


dictionary = load_cmudict()
encoding_table = encode.generate_encoding_table(dictionary)
encoding_automaton = encode.generate_encoding_automaton(encoding_table)


class TestEncodingTable:
    def test_314(self):
        assert '314' in encoding_table
        assert 'motor' in encoding_table['314']
        assert 'mutter' in encoding_table['314']
        assert 'meteor' in encoding_table['314']
        assert 'midyear' in encoding_table['314']
        assert 'amateur' in encoding_table['314']
        assert 'humidor' in encoding_table['314']

    def test_empty(self):
        assert '' in encoding_table

    def test_converage_2(self):
        for key in range(10**2):
            key = str(key).rjust(2, '0')
            assert key in encoding_table
            assert len(encoding_table[key]) > 0

    def test_converage_1(self):
        for key in range(10**1):
            key = str(key).rjust(1, '0')
            assert key in encoding_table
            assert len(encoding_table[key]) > 0


class TestEncodingAutomaton:
    def test_314(self):
        assert encoding_automaton.accepts_input('314')

    def test_empty(self):
        assert encoding_automaton.accepts_input('')

    def test_antidisestablishmentarianism(self):
        assert encoding_automaton.accepts_input('2110019563214203')


class TestAcceptedPrefixes:
    def _test_number(self, number):
        prefixes, suffixes = zip(
            *encode.accepted_prefixes(number, encoding_automaton)
        )

        for i in range(len(number) + 1):
            assert (number[:i] in prefixes) == (number[:i] in encoding_table)

        for prefix, suffix in zip(prefixes, suffixes):
            assert prefix + suffix == number

    def test_314(self):
        self._test_number('314')

    def test_20632(self):
        self._test_number('20632')

    def test_2110019563214203(self):
        self._test_number('2110019563214203')


class TestGeneratePartitions:
    def test_314(self):
        partitions = set(encode.generate_partitions('314', encoding_automaton))
        assert partitions == {('314',), ('31', '4'),
                              ('3', '14'), ('3', '1', '4')}

    def test_empty(self):
        assert set(encode.generate_partitions('', encoding_automaton)) == {()}


class TestEncodePartition:
    def test_314(self):
        assert set(encode.encode_partition(('314',), encoding_table)) \
            == {(x,) for x in encoding_table['314']}
        assert ('mute', 'arrow') in set(
            encode.encode_partition(('31', '4'), encoding_table))
