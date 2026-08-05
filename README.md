# Li Meng — academic website redesign

A complete GitHub Pages/Jekyll redesign for `www.meng.science`.

## What changed

- Research-first home page instead of a generic template.
- Responsive editorial design with light/dark mode and accessible navigation.
- Data-driven publication list with client-side filters.
- Dedicated research, publications, writing, and about pages.
- Three edited research essays based on public papers.
- Existing domain, public profile links, and email retained; the portrait was upgraded to a higher-resolution professional version.
- No proprietary framework or paid service required.

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
