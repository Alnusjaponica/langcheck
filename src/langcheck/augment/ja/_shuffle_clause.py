from __future__ import annotations

import random

import ginza
import spacy


def shuffle_clause(instances: list[str] | str,
                   *,
                   num_perturbations: int = 1,
                   aug_sent_p=0.5,
                   aug_clause_p=0.1) -> list[str]:
    '''Applies a text perturbation to each string in instances (usually a list
    of prompts) where some characters are changed to uppercase or lowercase.

    Args:
        instances: A single string or a list of strings to be augmented.
        to_case: Either 'uppercase' or 'lowercase'.
        aug_char_p: Percentage of all characters that will be augmented.
        num_perturbations: The number of perturbed instances to generate for
            each string in instances.

    Returns:
        A list of perturbed instances.
    '''

    nlp = spacy.load("ja_ginza")

    instances = [instances] if isinstance(instances, str) else instances
    perturbed_instances = []
    for instance in instances:
        parsed_instance = nlp(instance)
        for _ in range(num_perturbations):
            perturbed_instance = _perturb_sentence(parsed_instance, aug_sent_p,
                                                   aug_clause_p)
            perturbed_instances.append(perturbed_instance)
    return perturbed_instances


def _perturb_sentence(
        sentence: spacy.tokens.Doc,  # type: ignore[reportGeneralTypeIssues]
        aug_sent_p: float,
        aug_clause_p: float) -> str:
    if random.random() > aug_sent_p:
        return sentence.text

    parsed_sentence = list(ginza.bunsetu_spans(sentence))
    if len(parsed_sentence) < 2:
        return sentence.text

    parsed_sentence_len = len(parsed_sentence)
    for i in range(parsed_sentence_len):
        if random.random() > aug_clause_p:
            continue
        j = _get_index_pair(i, parsed_sentence_len)
        parsed_sentence[i], parsed_sentence[j] = parsed_sentence[
            j], parsed_sentence[i]
    return ''.join([clause.text for clause in parsed_sentence])


def _get_index_pair(index1: int, clause_num: int) -> int:
    index2 = random.randint(0, clause_num - 1)
    while index1 == index2:
        index2 = random.randint(0, clause_num - 1)
    return index2
