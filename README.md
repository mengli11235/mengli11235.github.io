# Li Meng — academic website redesign

A complete GitHub Pages/Jekyll redesign for `www.meng.science`.

## Design

- Type: Source Serif 4 for headings and essays, Schibsted Grotesk for text and interface. Both are self-hosted latin subsets in `assets/fonts/` (SIL Open Font License), so no third-party font requests.
- Color: near-white paper, one teal accent (`#0e6b5e`, the same as the CV), amber reserved for data marks. Dark mode inverts the same tokens.
- One signature figure: the "signal to structure" illustration in `_includes/fig-signal.html`, generated once and drawn on page load. The three research glyphs in `_includes/glyph-*.html` share its line style.
- Structure is carried by hairlines, timelines, and type scale. No cards, badges, or scroll animations.
- Social previews use `assets/img/og.png`; favicons are `favicon.svg`, `favicon.png`, and `apple-touch-icon.png`.

## Local preview

```bash
bundle install
bundle exec jekyll serve
```

Then open `http://127.0.0.1:4000`.

## Deploy

Replace the contents of the current `mengli11235.github.io` repository with this folder and push to the default branch. GitHub Pages will build it automatically. Keep the included `CNAME` file so the custom domain continues to work.

## Content maintenance

- Edit publications in `_data/publications.yml`.
- Edit recent updates in `_data/news.yml`.
- Add essays to `_posts/` using the existing front matter as a template.

## Verification note

The public-facing content was compiled from the previous site and public profiles/papers. The unpublished WACV/SPR material found in the working archive was deliberately not exposed in this website version.
