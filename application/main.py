#!/usr/bin/env python

__copyright__ = 'Copyright 2023, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'

import logging
import os

from pathlib import Path
from typing import Union

import keepachangelog

EMOJIS = {
    'added': '⭐',
    'fixed': '🐛',
    'changed': '♻',
    'removed': '🌀',
    'deprecated': '⚙',
    'security': '⚠',
    'backend': '⛽',
    'tests': '🎳',
    'test': '🎳',
    'translations': '🗺',
    'funders': '🙂',
    'funder': '🙂',
    'funded': '🙂',
}


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def to_bool(val: Union[str, int, float, bool], default_value: bool = True) -> bool:
    """ Convert a value to boolean """
    if isinstance(val, str):
        # For string, compare lower value to True string
        return val.lower() in ('yes', 'true', 't', '1')
    elif not val:
        # For value like False, 0, 0.0, None, empty list or dict returns False
        return False
    else:
        return default_value


def add_emoji(version_changelog: dict, end: bool = False) -> dict:
    """ Add emojis if possible. """
    logger = logging.getLogger("ReleaseChangelog")
    logger.debug("Let's add some colors if possible !")
    content = version_changelog['raw'].split('\n')
    # noinspection PyBroadException
    try:
        final = []
        for line in content:
            if line.startswith('###'):
                sub_section = line.replace('###', '').lower().strip()
                emoji = EMOJIS.get(sub_section)
                if emoji and end:
                    line = f'\n{line} {emoji}\n'
                elif emoji:
                    line = f'\n### {emoji} {sub_section.title()}\n'

            final.append(line)

        if final:
            version_changelog['raw'] = '\n'.join(final)

    except Exception as e:
        # Let's be safe, emoji is cool, but no need to fail in CI for that.
        logger.warning(f"Error while adding emoji, but we continue : {str(e)}")
        pass

    return version_changelog


def main():
    # Setting up logger
    logger = logging.getLogger("ReleaseChangelog")
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    failure_code = 0 if to_bool(os.getenv("INPUT_ALLOW_FAILURE")) else 1

    # Check changelog file
    changelog_env = os.getenv("INPUT_CHANGELOG_FILE")
    if not changelog_env:
        changelog_env = "CHANGELOG.md"
    changelog_file = Path(changelog_env)
    if not changelog_file.is_file():
        logger.critical(f"CHANGELOG file {changelog_file.absolute()} not found or is not a file.")
        exit(failure_code)

    # Check input release tag
    tag = os.getenv("INPUT_TAG_NAME")
    if not tag:
        tag = os.getenv("GITHUB_REF_NAME")
        if not tag:
            logger.critical(f"Tag is missing : from the action input and from a tag")
            exit(failure_code)

    changes = keepachangelog.to_raw_dict(str(changelog_file))
    info = None
    index = 0
    for i, version_changelog in enumerate(changes.keys()):
        if tag == version_changelog:
            logger.debug(f"We found the release {tag} in the changelog file")
            info = changes[version_changelog]
            index = i
            break

    if not info:
        logger.critical(f"Tag {tag} not found in the changelog file {changelog_file.absolute()}")
        exit(failure_code)

    add_emojis = to_bool(os.getenv("INPUT_ADD_EMOJIS"))
    if add_emojis:
        end_of_line = to_bool(os.getenv("INPUT_EMOJI_END_OF_LINE"))
        info = add_emoji(info, end=end_of_line)
    else:
        logger.debug("No adding emoji")

    output = info['raw']

    # Check raw GitHub link
    add_raw_changelog = to_bool(os.getenv("INPUT_ADD_RAW_CHANGELOG_LINK"))
    if add_raw_changelog:
        previous = None
        for i, version_changelog in enumerate(changes.keys()):
            if i == index + 1:
                previous = changes[version_changelog]

        if previous:
            output += (
                "\n"
                f"**Full changelog between {previous['metadata']['version']} and {tag}**: "
                f"https://github.com/{os.getenv('GITHUB_REPOSITORY')}/compare/{previous['metadata']['version']}...{tag}\n\n"
            )

    output = output.replace('%', '%25')
    output = output.replace('\n', '%0A')
    output = output.replace('\r', '%0D')
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'name=markdown::{output}', file=fh)

    return tag


if __name__ == "__main__":
    main()
