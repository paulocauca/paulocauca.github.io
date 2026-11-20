---
name: add-site-note
description: Publish a new "Notes & updates" entry on paulocauca.github.io in both languages at once — English in index.html and Portuguese in pt/index.html — inserted in the right place on the timeline (newest first) using the site's existing note markup. Use this whenever the user brings something to post on the site: a note, an update, an activity, a piece of news, a repo or article they published, a talk, a certification, a milestone — in Portuguese or English, phrased as "adiciona uma nota", "publica isso no site", "nova novidade", "add a note", or just handed over as raw text to publish. Use it even when they only give you the text in one language; producing the other translation is part of the job.
---

# Publishing a note on the site

The Notes & updates section is the only part of this site that grows regularly, and it exists twice — once in `index.html` (English) and once in `pt/index.html` (Portuguese). The two pages must stay in lockstep: same entries, same order, same dates. A note published in one language only is a bug, because the language switch keeps the reader on the same anchor and they'd land on a section that silently lost an entry.

Your job: take whatever the user hands you — usually a couple of sentences, often in Portuguese, sometimes just a link — and turn it into one entry on each page, written naturally in each language.

## The markup

Each entry is one `<li class="note">` inside `<ul class="notes">`. This is the shape, indented with 8 spaces at the `<li>`:

```html
        <li class="note">
          <time datetime="2026-09">Sep 2026</time>
          <div>
            <h3>Headline in sentence case</h3>
            <p>
              Two or three sentences of body text, hard-wrapped at roughly 95 columns
              the way the rest of the file is.
              <a href="https://example.com" target="_blank" rel="noopener">Repository →</a>
            </p>
          </div>
        </li>
```

Details that matter:

- `datetime` is machine-readable and identical on both pages: `YYYY-MM`. The visible label is localized — `Sep 2026` in English, `Set 2026` in Portuguese.
- Portuguese month labels: Jan, Fev, Mar, Abr, Mai, Jun, Jul, Ago, Set, Out, Nov, Dez. English: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec.
- The trailing link is optional. When there is one, it goes inside the same `<p>`, ends with a space and `→`, and carries `target="_blank" rel="noopener"`. Usual labels: `Repository →` / `Repositório →`, or something more specific like `Read the post →` / `Ler o post →`.
- The commented-out `EDIT ME` template lives at the bottom of the list on both pages. Leave it there — it's the author's own reminder of the format.

## Order on the timeline

The list reads newest first. A new note normally goes at the very top of `<ul class="notes">`, but not blindly: if the user is backfilling something older than an entry already published, it belongs below that entry, so the section still reads as a descending timeline. The helper script does this placement for you.

Both pages must end up with the entries in the same order — that's what makes the language switch feel like the same site rather than two.

## How to do it

1. **Settle the date.** If the user didn't say, use the current month (`YYYY-MM`). Don't invent a day; this site dates notes by month.

2. **Write both languages.** Write each version so it reads as though it were written in that language, not translated into it — the site's voice is first person, plain, slightly understated, and it says what something is for rather than selling it. Look at the neighbouring notes before you write; matching them is more reliable than any rule here. If the user gave you the text in Portuguese, the Portuguese entry should stay close to their wording and the English one should be a natural rewrite, and vice versa.

3. **Insert with the script**, which handles the placement, the month labels, the wrapping and the indentation on both pages at once:

   ```bash
   python3 .claude/skills/add-site-note/scripts/add_note.py note.json
   ```

   Write `note.json` first (anywhere temporary — the scratchpad is fine):

   ```json
   {
     "date": "2026-09",
     "en": {
       "title": "Post-quantum study repo now covers ML-DSA",
       "body": "Added working signature examples alongside the KEM notes. Still rough — it tracks what I'm learning rather than what I've finished.",
       "link": { "href": "https://github.com/paulocauca/pqc", "text": "Repository" }
     },
     "pt": {
       "title": "Repositório de estudo de PQC agora cobre ML-DSA",
       "body": "Adicionei exemplos de assinatura funcionando ao lado das notas de KEM. Ainda cru — acompanha o que estou aprendendo, e não o que já terminei.",
       "link": { "href": "https://github.com/paulocauca/pqc", "text": "Repositório" }
     }
   }
   ```

   Omit `link` when there's nothing to link to. The script escapes `&`, `<` and `>` for you, so write plain text — but em dashes, accents and `→` are fine as-is, the pages are UTF-8. It prints where the entry landed in each file and refuses to run if the two pages are already out of sync, which is worth knowing about before you add to the mess.

4. **Check it in the browser.** Start the preview (`preview_start` with the `site` config), open `/#notes` and `/pt/#notes`, and confirm the new entry reads correctly at the top of both, with the right month label. This catches the things a script can't judge — a headline that wraps badly, a translation that sits oddly next to its neighbours.

5. **Commit and open a PR** against the latest `origin/main`, per the standing preference in this repo. A commit message like `Add a note about the PQC signature examples` and a PR body carrying both language versions of the note is enough — the reviewer is the person who wrote it, so what they want to see is the copy, not a description of the mechanics.

## When the script isn't the right tool

If the entry needs something the template doesn't cover — a second paragraph, an inline `<strong>`, two links — edit both files by hand instead of bending the JSON. The script exists to save you from indentation and ordering mistakes on the common case, not to be the only way in. Whatever you do by hand, keep the two pages identical in structure and order; that invariant is the thing worth protecting.
