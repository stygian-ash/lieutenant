'''Encode a number to a word or sentence using the major system.'''
import string
import itertools
from typing import Iterator

from automata.fa.dfa import DFA
from automata.base.exceptions import RejectionException

from lieutenant.major.decode import decode_from_dictionary
from lieutenant.pronounce import Dictionary


type EncodingTable = dict[str, set[str]]


def generate_encoding_table(dictionary: Dictionary) -> EncodingTable:
    '''Generate a lookup table that maps numbers to words in a dictionary.'''
    table = {}
    for word, _ in dictionary.items():
        for encoding in decode_from_dictionary(word, dictionary):
            if not encoding in table:
                table[encoding] = set()
            table[encoding].add(word)
    return table


def generate_encoding_automaton(table: EncodingTable) -> DFA:
    '''Generate a DFA that accepts numbers that have a valid encoding in the lookup table.'''
    return DFA.from_finite_language(set(string.digits), set(table.keys()))


def accepted_prefixes(input: str, automaton: DFA) -> Iterator[tuple[str, str]]:
    '''Find all prefixes of a string that are accepted by a DFA.'''
    try:
        for index, state in enumerate(automaton.read_input_stepwise(input)):
            if state is None:
                break
            if state in automaton.final_states:
                yield (input[:index], input[index:])
    except RejectionException:
        pass


def generate_partitions(input: str, automaton: DFA) -> Iterator[tuple[str, ...]]:
    '''Generate all possible partitions of an input into subsequences that are accepted by a DFA.'''
    if input == '':
        yield ()
    for first, rest in list(accepted_prefixes(input, automaton))[::-1]:
        if first == '':
            continue
        else:
            for partition in generate_partitions(rest, automaton):
                yield (first,) + partition


def encode_partition(partition: tuple[str, ...], table: EncodingTable) -> Iterator[tuple[str, ...]]:
    '''Generate all possible encodings from the lookup table of a partition of a valid partition of a digit string.'''
    yield from itertools.product(*map(table.__getitem__, partition))
