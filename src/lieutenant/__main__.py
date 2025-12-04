import re
import bisect
import random
import operator
import functools
import itertools
from pathlib import Path
from collections import Counter

import typer

from lieutenant import major
from lieutenant.pronounce import load_cmudict


BROWN_CORPUS = Path(__file__).parent / 'resources' \
    / 'brown' / 'brown_detokenized.txt'
with BROWN_CORPUS.open('r') as f:
    brown_words = Counter(re.split(r'[^a-z]+', f.read().lower()))

app = typer.Typer()
dictionary = load_cmudict()
table = major.encode.generate_encoding_table(dictionary)
dfa = major.encode.generate_encoding_automaton(table)


def prod(it):
    return functools.reduce(operator.mul, it, 1)


@app.command()
def decode(words: list[str]):
    '''Decode a sentence to a number.'''
    parts = [major.decode.decode_from_dictionary(
        word, dictionary) for word in words]
    for part in parts:
        if len(part) == 1:
            print(list(part)[0], end='')
        else:
            print('({})'.format('|'.join(part)), end='')
    print()


@app.command()
def count(number: str):
    '''Count the number of encodings of a number.'''
    n = sum(
        prod(len(table[di]) for di in P if di != '')
        for P in major.encode.generate_partitions(number, dfa)
    )
    print(f'{n:,}')


@app.command()
def encode(number: str, results: int = 5):
    partitions = sorted(
        major.encode.generate_partitions(number, dfa),
        key=len
    )
    partition = partitions[0]
    used_words = [set() for _ in partition]
    choice_sets = [list(table[pi]) for pi in partition]
    for _ in range(min(results, min(len(S) for S in choice_sets))):
        words = []
        for i, choices in enumerate(choice_sets):
            weights = [
                brown_words.get(w, 0)
                    if w not in used_words[i]
                    else 0
                for w in choices
            ]
            for used in used_words[i]:
                weights[choices.index(used)] = 0
            cum_weights = list(itertools.accumulate(weights))
            t = random.uniform(0, cum_weights[-1])
            index = bisect.bisect(cum_weights, t)
            word = choices[index] if index < len(choices) else random.choice(choices)
            words.append(word)
            used_words[i].add(word)
        print(' '.join(words))

if __name__ == '__main__':
    app()
