#!/usr/bin/env python
"""Render conference metadata to markdown

Functionality to dump proceedings records to well-formatted metadata.

Example usage
-------------
$ ./scripts/pubs_to_markdown.py \
    publications.yaml \
    pubs.md

"""
import argparse
import os
import sys
import yaml

TEMPLATE = '''
| {} |
| --- |
'''

ENTRIES = {
    'conferences': '|{authors} **[{title}]({url})** {booktitle} {year}|',
    'journals': '|{authors} **[{title}]({url})** {booktitle} {issue}, pp. {pages} {year}|',
    'patents': '|{authors} **[{title}]({url})** {number} {year}|',
    'theses': '|{authors} **[{title}]({url})** {institution} {location} {year}|',
    'miscellaneous': '|{authors} **[{title}]({url})** {booktitle} {year}|'
}


def render_one(pubtype, record):
    return ENTRIES[pubtype].format(**record)


def render(publications):
    lines = []
    for pubtype, records in publications.items():

        lines += [TEMPLATE.format(pubtype)]
        lines += [render_one(pubtype, record) for _, record in records.items()]

    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)

    # Inputs
    parser.add_argument("publications",
                        metavar="publications", type=str,
                        help="Path to publications.")
    parser.add_argument("output_file",
                        metavar="output_file", type=str,
                        help="Path to output markdown file.")

    args = parser.parse_args()
    publications = yaml.load(open(args.publications))

    with open(args.output_file, 'w') as fp:
        fp.write(render(publications))

    sys.exit(0 if os.path.exists(args.output_file) else 1)
