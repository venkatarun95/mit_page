# Adding a blog post

1. Create the article body as an HTML file in `templates/blog/posts/`. Ordinary
   paragraphs (`<p>...</p>`) are enough; headings, lists, links, block quotes,
   and other HTML can be added when useful. Do not include `<html>`, `<head>`,
   or `<body>` tags.
2. Add one entry to `templates/blog/posts.json` with these fields:
   - `title`: the displayed title
   - `slug`: the URL portion after `/blog/`
   - `date`: the publication date in `YYYY-MM-DD` format
   - `category`: exactly one of `Fun ideas`, `Humor`, `Research`, or `Philosophy`
   - `summary`: the description shown on archive pages
   - `source`: the HTML filename created in step 1
3. From the `templates/` directory, run `./venv/bin/python build.py`.

The build creates the post at `/blog/<slug>.html`, updates the reverse-chronological
blog index, and adds the post to its category archive.
