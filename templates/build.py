from datetime import date
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
import json
from typing import Dict, Union

def prep_navigation(active: str):
    navigation = [
        {"name": "Home", "url": "index.html"},
        {"name": "Students", "url": "projects.html"},
        {"name": "Teaching", "url": "teaching.html"},
    ]
    for i in range(len(navigation)):
        if active is not None and navigation[i]["name"] == active:
            navigation[i]["active"] = True
        else:
            navigation[i]["active"] = False
    return navigation

def prep_inline_cites(papers: Dict[str, Dict[str, Union[str, int]]]) -> Dict[str,str]:
    ''' Prepare the list of papers with <abbr> tags for inline citations '''
    res = {}
    for ref in papers:
        paper = papers[ref]

        conf_map = {"ACM SIGCOMM": "SIGCOMM",
                    "USENIX NSDI": "NSDI",
                    "ACM SIGCOMM HotNets": "HotNets",
                    "ACM MobiSys": "MobiSys",
                    "NDSS Symposium": "NDSS",
                    "Facebook Engineering Blog": "FB Engg. Blog"}
        if paper['conf'] in conf_map:
            conf_name = conf_map[paper['conf']] + str(paper['year'] - 2000)
        elif paper['conf'].startswith('Arxiv'):
            conf_name = 'Arxiv'
        else:
            print(f"Warning: unrecognized conference '{paper['conf']}'")

        res[ref] = f"<abbr title=\"{paper['title']}. {paper['authors']}. In {paper['conf']} {paper['year']}\">{conf_name}</abbr>"
    return res

if __name__ == "__main__":
    env = Environment(
        loader=FileSystemLoader("./"),
        undefined=StrictUndefined
        #autoescape=select_autoescape()
    )

    with open("papers.json", "r") as papers_file:
        papers = json.load(papers_file)
        inline_cites = prep_inline_cites(papers)

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
        rendered = template.render(navigation=prep_navigation("Home"), icite=inline_cites, project_descriptions=project_descriptions)
        outfile.write(rendered)

    with open("../perf-verif.html", "w") as outfile:
        template = env.get_template("perf-verif.html")
        rendered = template.render(navigation=prep_navigation(None))
        outfile.write(rendered)

    with open("../congestion-control.html", "w") as outfile:
        template = env.get_template("congestion-control.html")
        rendered = template.render(navigation=prep_navigation(None))
        outfile.write(rendered)


    with open("../rfocus.html", "w") as outfile:
        template = env.get_template("rfocus.html")
        rendered = template.render(navigation=prep_navigation(None))
        outfile.write(rendered)
