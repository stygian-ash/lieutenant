#!/usr/bin/env python3
'''Produce a version of the Brown Corpus with natural whitespace and without POS tags.'''
import re
import logging

import nltk
from nltk.corpus import brown
from mosestokenizer import MosesDetokenizer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

OUTFILE = 'brown_detokenized.txt'


def main():
    logging.info('Fetching Brown Corpus')
    nltk.download('brown')
    sentences = brown.sents()

    # See https://stackoverflow.com/a/47301618
    logging.info('Detokenizing')
    detokenizer = MosesDetokenizer()
    detokenized = [
        detokenizer(
            ' '.join(sent).replace('``', '"')
               .replace("''", '"')
               .replace('`', "'")
               .split()
        )
        for sent in sentences
    ]
    detokenized = '\n'.join(detokenized)

    logging.info('Stripping list markers')
    detokenized = re.sub(r'\(\d+\)\s*', '', detokenized)
    detokenized = re.sub(r'^--\s*', '', detokenized)

    logging.info('Stripping hyphens')
    detokenized = re.sub(r'(?<!-)-(?!-)', ' ', detokenized)

    logging.info('Normalizing punctuation')
    detokenized = detokenized.replace('..', '.') \
                             .replace(';;', ';') \
                             .replace(',,', ',') \
                             .replace('??', '?') \
                             .replace('!!', '!')
    detokenized = re.sub(r'(["\'])\s+([,.?!])', r'\1\2', detokenized)

    logging.info('Normalizing whitespace')
    detokenized = re.sub(r'(\s)\s+', r'\1', detokenized)
    detokenized = re.sub(r'\s?([,.?!])', r'\1', detokenized)

    logging.info('Writing output to %s', OUTFILE)
    with open(OUTFILE, 'w') as f:
        f.write(detokenized)

    logging.info('Done!')


if __name__ == '__main__':
    main()
