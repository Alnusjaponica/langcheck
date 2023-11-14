from __future__ import annotations

import random


def change_case(
    instances: list[str] | str,
    *,
    to_case: str = 'uppercase',
    aug_char_p: float = 1.0,
    num_perturbations: int = 1,
) -> list[str]:
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

    instances = [instances] if isinstance(instances, str) else instances
    perturbed_instances = map(
        lambda x: _perturb_instance(x, to_case, aug_char_p, num_perturbations),
        instances)
    return sum(perturbed_instances, [])


def _perturb_char(char, to_case, aug_char_p):
    if random.random() > aug_char_p:
        return char  # No augmentation
    if to_case == 'uppercase':
        return char.upper()
    return char.lower()


def _perturb_instance(instance, to_case, aug_char_p, num_perturbations):
    # Generate `num_perturbations` perturbed instances
    perturbed_instance = [
        "".join(map(lambda x: _perturb_char(x, to_case, aug_char_p), instance))
        for _ in range(num_perturbations)
    ]
    return perturbed_instance
