#!/usr/bin/env python3
"""Insert one "Notes & updates" entry into index.html and pt/index.html.

Usage: python3 add_note.py note.json [--repo PATH]

The JSON carries the date and one version of the note per language:

    {
      "date": "2026-09",
      "en": {"title": "...", "body": "...", "link": {"href": "...", "text": "Repository"}},
      "pt": {"title": "...", "body": "...", "link": {"href": "...", "text": "Repositório"}}
    }

"link" is optional. Text is plain — &, < and > are escaped here.

The entry lands in date order (newest first) and the script checks that both
pages tell the same story before and after the edit.
"""

import argparse
import html
import io
import json
import os
import re
import sys
import textwrap

MONTHS = {
    'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'pt': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
           'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
}

PAGES = {'en': 'index.html', 'pt': 'pt/index.html'}

LIST_OPEN = '<ul class="notes">'
NOTE_RE = re.compile(r'^ *<li class="note">\n(?:.*?\n)*? *</li>\n', re.M)
DATETIME_RE = re.compile(r'<time datetime="([^"]+)"')
COMMENT_RE = re.compile(r'<!--(?:.|\n)*?-->')


def fail(message):
    sys.stderr.write('add_note: %s\n' % message)
    sys.exit(1)


def read(path):
    with io.open(path, encoding='utf-8') as fh:
        return fh.read()


def mask_comments(region):
    """Blank out HTML comments, keeping offsets intact.

    The list ends with a commented-out <li class="note"> template the author
    keeps as a reminder of the format. Matching it as a real note would date
    the timeline wrongly and, worse, file new entries inside the comment.
    """
    def blank(match):
        return re.sub(r'[^\n]', ' ', match.group(0))
    return COMMENT_RE.sub(blank, region)


def notes_block(source, path):
    """Return (start, end) offsets of everything between <ul class="notes"> and </ul>."""
    open_at = source.find(LIST_OPEN)
    if open_at < 0:
        fail('no %s found in %s' % (LIST_OPEN, path))
    start = source.index('\n', open_at) + 1
    end = source.find('</ul>', start)
    if end < 0:
        fail('unterminated notes list in %s' % path)
    return start, end


def existing_dates(source, path):
    start, end = notes_block(source, path)
    region = mask_comments(source[start:end])
    return [DATETIME_RE.search(m.group(0)).group(1)
            for m in NOTE_RE.finditer(region)]


def month_label(date, lang):
    try:
        year, month = date.split('-')
        return '%s %s' % (MONTHS[lang][int(month) - 1], year)
    except (ValueError, IndexError):
        fail('date must look like YYYY-MM, got %r' % date)


def render(entry, date, lang):
    title = html.escape(entry['title'].strip(), quote=False)
    body = html.escape(' '.join(entry['body'].split()), quote=False)

    lines = textwrap.wrap(body, width=95) or ['']
    paragraph = ['              %s' % line for line in lines]

    link = entry.get('link')
    if link:
        paragraph.append(
            '              <a href="%s" target="_blank" rel="noopener">%s →</a>'
            % (html.escape(link['href'], quote=True),
               html.escape(link.get('text', 'Repository').strip(), quote=False))
        )

    return (
        '        <li class="note">\n'
        '          <time datetime="%s">%s</time>\n'
        '          <div>\n'
        '            <h3>%s</h3>\n'
        '            <p>\n'
        '%s\n'
        '            </p>\n'
        '          </div>\n'
        '        </li>\n'
    ) % (date, month_label(date, lang), title, '\n'.join(paragraph))


def insert(source, path, entry_html, date):
    """Insert before the first note older than `date`, i.e. keep newest first."""
    start, end = notes_block(source, path)
    region = mask_comments(source[start:end])
    position, index = start, 0
    for match in NOTE_RE.finditer(region):
        note_date = DATETIME_RE.search(match.group(0)).group(1)
        if note_date <= date:
            break
        position, index = start + match.end(), index + 1
    return source[:position] + entry_html + source[position:], index


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('note', help='path to the note JSON')
    parser.add_argument('--repo', default=None,
                        help='repository root (default: two levels above this script)')
    args = parser.parse_args()

    root = args.repo or os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

    with io.open(args.note, encoding='utf-8') as fh:
        note = json.load(fh)

    date = note.get('date', '')
    for lang in ('en', 'pt'):
        if lang not in note:
            fail('the note needs both "en" and "pt" — "%s" is missing' % lang)
        if not note[lang].get('title') or not note[lang].get('body'):
            fail('the %s entry needs a title and a body' % lang)

    paths = {lang: os.path.join(root, rel) for lang, rel in PAGES.items()}
    sources = {}
    for lang, path in paths.items():
        if not os.path.exists(path):
            fail('%s not found — is --repo pointing at the site?' % path)
        sources[lang] = read(path)

    before = {lang: existing_dates(sources[lang], paths[lang]) for lang in paths}
    if before['en'] != before['pt']:
        fail('index.html and pt/index.html already disagree on the notes timeline:\n'
             '  en: %s\n  pt: %s\nFix that before adding a new one.'
             % (before['en'], before['pt']))

    results = {}
    for lang, path in paths.items():
        updated, index = insert(sources[lang], path,
                                render(note[lang], date, lang), date)
        results[lang] = (path, updated, index)

    if results['en'][2] != results['pt'][2]:
        fail('the entry would land at different positions in each page — aborting')

    for lang, (path, updated, _) in results.items():
        with io.open(path, 'w', encoding='utf-8') as fh:
            fh.write(updated)

    index = results['en'][2]
    where = 'at the top' if index == 0 else 'in position %d' % (index + 1)
    print('Added the %s note %s of the timeline in:' % (date, where))
    for lang, (path, _, _) in sorted(results.items()):
        print('  %s  (%s)' % (os.path.relpath(path, root), month_label(date, lang)))


if __name__ == '__main__':
    main()
