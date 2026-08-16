# paulocauca.github.io

Personal website — [paulocauca.github.io](https://paulocauca.github.io/)

Static HTML/CSS/JS. No build step, no framework, no dependencies. Edit and push.

## Structure

```
index.html            all content lives here
assets/css/style.css  design system (colors, type, layout)
assets/js/main.js     theme toggle, scrollspy, footer year
assets/img/avatar.jpg profile photo
.nojekyll             serve files as-is, skip Jekyll
```

## Editing

Sections are marked in `index.html` with `<!-- EDIT ME -->` comments where content
is meant to be updated regularly:

- **Career** — one `<li class="tl">` per *company*, newest first; inside it, one
  `<div class="job">` per *role* at that company, newest first. Use `<ul class="bullets">`
  for responsibilities and `<p class="job__text">` for a single-paragraph summary.
- **Education** — one `<li class="edu__item">` per course, newest end-date first.
- **Notes & updates** — add new entries at the *top* of the `<ul class="notes">` list.
- **Books** — replace with your current shelf.

Section numbers (`<span class="sec__num">`) are written by hand — renumber them if you
insert or remove a section, and keep the left-rail nav links in sync.

To change the accent color or fonts, edit the `:root` variables at the top of
`assets/css/style.css`. Dark theme values live in `html[data-theme="dark"]`.

## Local preview

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Deploy

GitHub Pages serves `main` from the repository root. Push to publish.
