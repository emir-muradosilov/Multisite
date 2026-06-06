import re
import random


pattern = re.compile(r'\{([^{}]+)\}')


def process_spintax(text):

    while re.search(pattern, text):

        text = re.sub(
            pattern,
            replace_match,
            text
        )

    return text


def replace_match(match):

    options = match.group(1).split('|')

    return random.choice(options)