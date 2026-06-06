import random
import re


def spin_text(text):

    pattern = r'\{([^{}]+)\}'

    while re.search(pattern, text):

        text = re.sub(
            pattern,
            lambda m: random.choice(
                m.group(1).split('|')
            ),
            text
        )

    return text