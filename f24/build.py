from jinja2 import Environment, FileSystemLoader, select_autoescape


def prep_navigation(active: str):
    navigation = [
        {"name": "Home", "url": "index.html"},
        {"name": "Schedule", "url": "schedule.html"},
        {"name": "Assignments", "url": "asignments.html"},
        {"name": "Ed Discussion", "url": "https://edstem.org/us/courses/62463"},
        {"name": "Canvas", "url": "https://utexas.instructure.com/courses/1401747"}
    ]
    for i in range(len(navigation)):
        if navigation[i]["name"] == active:
            navigation[i]["active"] = True
        else:
            navigation[i]["active"] = False
    return navigation

env = Environment(
    loader=FileSystemLoader("."),
#    autoescape=select_autoescape()
)

template = env.get_template("template.html")

with open("index.html", "w") as index_file:
    with open("index.content.html", "r") as content:
        rendered = template.render(content=content.read(), navigation=prep_navigation("Home"))
        index_file.write(rendered)
