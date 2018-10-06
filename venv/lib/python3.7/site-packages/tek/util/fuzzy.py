from difflib import SequenceMatcher
from operator import itemgetter


def best_match(seq, target):
    matcher = SequenceMatcher()
    matcher.set_seq2(target)

    def ratio():
        for index, specimen in enumerate(seq):
            matcher.set_seq1(specimen)
            yield index, matcher.ratio()
    candidates = ratio()
    return max(candidates, key=itemgetter(1)) if candidates else None
