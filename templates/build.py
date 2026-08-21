import copy
from datetime import date, datetime
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
import os
import subprocess
import shutil
from templatex import Environment as LatexEnvironment
import json
from typing import Dict, Tuple, Union

BLOG_CATEGORIES = [
    {"name": "Research", "slug": "research", "description": "Technical ideas, research notes, and works in progress."},
    {"name": "Philosophy", "slug": "philosophy", "description": "Essays about society, language, and how we make sense of the world."},
    {"name": "Fun ideas", "slug": "fun-ideas", "description": "Small experiments and unexpected ways to look at everyday things."},
    {"name": "Humor", "slug": "humor", "description": "Pieces written mainly for amusement."},
]


def prep_navigation(active: str, root_prefix: str = ""):
    navigation = [
        {"name": "Home", "url": root_prefix + "index.html"},
        {"name": "Students", "url": root_prefix + "students.html"},
        {"name": "Teaching", "url": root_prefix + "index.html#teaching"},
        {"name": "Publications", "url": root_prefix + "publications.html"},
        {"name": "Blog", "url": root_prefix + "blog/index.html"}
    ]
    for i in range(len(navigation)):
        if active is not None and navigation[i]["name"] == active:
            navigation[i]["active"] = True
        else:
            navigation[i]["active"] = False
    return navigation


def prep_blog_posts(posts):
    """Validate and prepare blog metadata for templates."""
    category_names = {category["name"] for category in BLOG_CATEGORIES}
    prepared = copy.deepcopy(posts)
    seen_slugs = set()

    for post in prepared:
        required = {"title", "slug", "date", "category", "summary", "source"}
        missing = required - post.keys()
        if missing:
            raise ValueError(f"Blog post is missing fields: {sorted(missing)}")
        if post["slug"] in seen_slugs:
            raise ValueError(f"Duplicate blog slug: {post['slug']}")
        if post["category"] not in category_names:
            raise ValueError(f"Unknown blog category: {post['category']}")
        seen_slugs.add(post["slug"])
        post["date_obj"] = datetime.strptime(post["date"], "%Y-%m-%d")
        post["date_display"] = post["date_obj"].strftime("%B %-d, %Y")
        post["category_slug"] = next(
            category["slug"] for category in BLOG_CATEGORIES
            if category["name"] == post["category"]
        )

    prepared.sort(key=lambda post: post["date_obj"], reverse=True)
    return prepared

def prep_cites(papers: Dict[str, Dict[str, Union[str, int]]]) -> Tuple[Dict[str,str], Dict[str,str]]:
    ''' Prepare the list of papers with <abbr> tags for inline citations '''
    inline = {}
    full = copy.deepcopy(papers)
    for ref in papers:
        paper = papers[ref]

        conf_map = {"ACM SIGCOMM": "SIGCOMM",
                    "USENIX NSDI": "NSDI",
                    "ACM SIGCOMM HotNets": "HotNets",
                    "ACM MobiSys": "MobiSys",
                    "NDSS Symposium": "NDSS",
                    "DIMES": "DIMES",
                    "NINeS": "NINeS",
                    "Facebook Engineering Blog": "FB Engg. Blog",
                    "arXiv": "arXiv",
                    "unpublished": "Coming soon"}
        if paper['conf'] in conf_map:
            conf_name = conf_map[paper['conf']] + str(paper['year'] - 2000)
            conf_full_name = conf_map[paper['conf']] + ' ' + str(paper['year'])
        else:
            print(f"Warning: unrecognized conference '{paper['conf']}'")

        url = ""
        if "url" in paper:
            url = paper["url"]
        inline[ref] = (
            '<abbr class="citation" data-url="{}" data-papertitle="{}" '
            'data-authors="{}" data-conf="{}" data-year="{}">{}</abbr>'
        ).format(
            url,
            paper['title'],
            paper['authors'],
            paper['conf'],
            paper['year'],
            paper['short_name'],
        )
        full[ref]['conf'] = conf_full_name
        full[ref]['ref'] = ref

        if "exclude" not in full[ref]:
            full[ref]["exclude"] = False

    # Sort full by year
    full = [full[p] for p in full]
    full.sort(key=lambda p: p['year'], reverse=True)

    return inline, full

def prep_students(students: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    ''' Prepare the list of all students '''
    res = copy.deepcopy(students)
    year_now = datetime.now()
    year_map = ["First year student",
                "Second year student",
                "Third year student",
                "Fourth year student",
                "Fifth year student",
                "Sixth year student",
                "Seventh year student",
                "Eigth year student",
                "Ninth year student",
                "Tenured grad student"]

    for ref in res:
        if 'end' in res[ref]:
            end = datetime.strptime(res[ref]['end'], "%Y-%m")
            res[ref]['year'] = "Graduated in " + str(end.year)
            continue

        start = datetime.strptime(res[ref]['start'], "%Y-%m")
        year = max(0, (year_now - start).days // 365)
        if year >= 9:
            print("Warning: You have a tenured grad student. This is not supposed to happen. Graduate them ASAP")
            year = 9
        res[ref]['year'] = year_map[year]

    return dict(sorted(res.items(), key=lambda student: student[1]['start'], reverse=True))

def compile_tex_to_pdf(tex_file_path, output_dir):
    """
    Compile a .tex file into a PDF using pdflatex and copy the PDF to the given directory.

    :param tex_file_path: Path to the .tex file.
    :param output_dir: Directory where the resulting PDF will be copied.
    """
    # Get the directory and filename of the .tex file
    tex_dir = os.path.dirname(tex_file_path)
    tex_filename = os.path.basename(tex_file_path)
    pdf_filename = os.path.splitext(tex_filename)[0] + ".pdf"

    # Compile the .tex file using pdflatex
    try:
        subprocess.run(
            ["pdflatex", tex_filename],
            cwd=tex_dir,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error compiling {tex_filename}: {e}")
        return

    # Check if the output directory exists, create if it doesn't
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Copy the resulting PDF to the output directory
    pdf_file_path = os.path.join(tex_dir, pdf_filename)
    if os.path.exists(pdf_file_path):
        shutil.copy(pdf_file_path, output_dir)
        print(f"PDF successfully copied to {output_dir}")
    else:
        print(f"PDF file not found after compilation: {pdf_file_path}")

if __name__ == "__main__":
    env = Environment(
        loader=FileSystemLoader("./"),
        undefined=StrictUndefined
        #autoescape=select_autoescape()
    )

    latex_env = LatexEnvironment(loader=FileSystemLoader('./'))

    with open("students.json", "r") as papers_file:
        students = json.load(papers_file)
        students = prep_students(students)

    with open("papers.json", "r") as papers_file:
        papers = json.load(papers_file)
        inline_cites, papers = prep_cites(papers)
        blog_inline_cites = {
            ref: cite.replace('data-url="assets/', 'data-url="../assets/')
            for ref, cite in inline_cites.items()
        }

    with open("awards.json", "r") as awards_file:
        awards = json.load(awards_file)

    with open("blog/posts.json", "r") as posts_file:
        blog_posts = prep_blog_posts(json.load(posts_file))

    with open("project_descriptions.json") as project_descriptions_file:
        project_descriptions = json.load(project_descriptions_file)
        # Render the descriptions
        res = []
        for proj in project_descriptions:
            desc_template = env.from_string(project_descriptions[proj]['description'])
            project_descriptions[proj]['description'] = desc_template.render(icite=inline_cites)
        project_descriptions = [project_descriptions[x] for x in project_descriptions]

    with open("../index.html", "w") as outfile:
        template = env.get_template("index.html")
        rendered = template.render(navigation=prep_navigation("Home"), icite=inline_cites, project_descriptions=project_descriptions, students=students, awards=awards)
        outfile.write(rendered)

    with open("../students.html", "w") as outfile:
        template = env.get_template("students.html")
        rendered = template.render(navigation=prep_navigation("Students"), students=students)
        outfile.write(rendered)

    with open("../publications.html", "w") as outfile:
        template = env.get_template("publications.html")
        rendered = template.render(navigation=prep_navigation("Publications"), papers=papers)
        outfile.write(rendered)

    with open("../rfocus.html", "w") as outfile:
        template = env.get_template("rfocus.html")
        rendered = template.render(navigation=prep_navigation(None))
        outfile.write(rendered)

    blog_dir = "../blog"
    os.makedirs(blog_dir, exist_ok=True)

    with open(os.path.join(blog_dir, "index.html"), "w") as outfile:
        template = env.get_template("blog/index.html")
        rendered = template.render(
            navigation=prep_navigation("Blog", "../"),
            root_prefix="../",
            posts=blog_posts,
            categories=BLOG_CATEGORIES,
        )
        outfile.write("\n".join(line.rstrip() for line in rendered.splitlines()) + "\n")

    post_template = env.get_template("blog/post.html")
    for post in blog_posts:
        with open(os.path.join(blog_dir, post["slug"] + ".html"), "w") as outfile:
            rendered = post_template.render(
                navigation=prep_navigation("Blog", "../"),
                root_prefix="../",
                post=post,
                icite=blog_inline_cites,
            )
            outfile.write("\n".join(line.rstrip() for line in rendered.splitlines()) + "\n")

    category_template = env.get_template("blog/category.html")
    for category in BLOG_CATEGORIES:
        category_dir = os.path.join(blog_dir, "category", category["slug"])
        os.makedirs(category_dir, exist_ok=True)
        category_posts = [
            post for post in blog_posts if post["category"] == category["name"]
        ]
        with open(os.path.join(category_dir, "index.html"), "w") as outfile:
            rendered = category_template.render(
                navigation=prep_navigation("Blog", "../../../"),
                root_prefix="../../../",
                category=category,
                posts=category_posts,
                categories=BLOG_CATEGORIES,
            )
            outfile.write("\n".join(line.rstrip() for line in rendered.splitlines()) + "\n")

    with open("/tmp/cv.tex", "w") as outfile:
        template = latex_env.get_template("cv.tex")
        rendered = template.render(awards=awards, papers=papers)
        outfile.write(rendered)

        # Check if the rendered file is the same as cv-compiled.tex. If so, no
        # need to run pdflatex again as it will create a pdf that is
        # unnecessarily different from what is comitted
        with open("cv-compiled.tex", "r") as cached_file:
            cached = cached_file.read()
            cached_file.close()
            if cached != rendered:
                print("Compiling Latex again")
                compile_tex_to_pdf("/tmp/cv.tex", "../")
                # Copy new cached file
                shutil.copyfile("/tmp/cv.tex", "cv-compiled.tex")
