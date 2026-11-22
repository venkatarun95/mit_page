# Fall 2026 course site

Edit the files in `templates/`, then run `python3 build.py` from this `f26/` directory. The script renders `index.html`, `schedule.html`, and `assignments.html` here; do not edit those generated pages directly.

- Change home-page or assignment text and links in `templates/index.html` or `templates/assignments.html`.
- Change lecture dates, topics, slide filenames, or navigation in `build.py`. The schedule markup is in `templates/schedule.html`.
- Put quiz PDFs in `assets/` and assignment PDFs in `assets/assignments/`. Link them with paths relative to the generated page, such as `assets/quiz1-2026.pdf`.
- After building, check that each new link points to an existing file. The script does not copy assets or validate links.

The site-wide `templates/build.py` is separate; it builds the main site, not this course folder.
