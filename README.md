# Bookshelf

Technical books and articles I have read. Each PDF is committed once read.

> Generated from `catalog.json` by `scripts/build_readme.py`. Do not edit by hand.

## Adding a book

1. Name the PDF `<first-author-surname>-<title-in-kebab-case>-<year>.pdf`
   (lowercase ASCII, digits and dashes only), e.g. `martin-the-clean-coder-2011.pdf`.
2. Add an entry to `catalog.json` (`file`, `title`, `authors`, `year`, `url`, optional `articles`
   as a list of `{"title": ..., "url": ...}`).
3. `git add` both and commit: the pre-commit hook regenerates and stages this README.
   CI fails if the README, the catalog and the committed PDFs ever disagree.

One-time setup per clone: `git config core.hooksPath .githooks`

## Books (2)

| Title | Author(s) | Year | Links |
| --- | --- | --- | --- |
| The Clean Coder: A Code of Conduct for Professional Programmers | Robert C. Martin | 2011 | [PDF](martin-the-clean-coder-2011.pdf) · [Book page](https://www.informit.com/store/clean-coder-a-code-of-conduct-for-professional-programmers-9780137081073) |
| UNIX: A History and a Memoir | Brian W. Kernighan | 2019 | [PDF](kernighan-unix-a-history-and-a-memoir-2019.pdf) · [Book page](https://www.cs.princeton.edu/~bwk/memoir.html) |
