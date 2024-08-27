from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape


def prep_navigation(active: str):
    navigation = [
        {"name": "Home", "url": "index.html"},
        {"name": "Schedule", "url": "schedule.html"},
        {"name": "Assignments", "url": "assignments.html"},
        {"name": "Ed Discussion", "url": "https://edstem.org/us/courses/62463"},
        {"name": "Canvas", "url": "https://utexas.instructure.com/courses/1401747"}
    ]
    for i in range(len(navigation)):
        if navigation[i]["name"] == active:
            navigation[i]["active"] = True
        else:
            navigation[i]["active"] = False
    return navigation

def prep_schedule():
    dates = [
        date(2024,  8, 27),
        date(2024,  8, 29),
        date(2024,  9, 3),
        date(2024,  9, 5),
        date(2024,  9, 10),
        date(2024,  9, 12),
        date(2024,  9, 17),
        date(2024,  9, 19),
        date(2024,  9, 24),
        date(2024,  9, 26),
        date(2024, 10, 1),
        date(2024, 10, 3),
        date(2024, 10, 8),
        date(2024, 10, 10),
        date(2024, 10, 15),
        date(2024, 10, 17),
        date(2024, 10, 22),
        date(2024, 10, 24),
        date(2024, 10, 29),
        date(2024, 10, 31),
        date(2024, 11, 5),
        date(2024, 11, 7),
        date(2024, 11, 12),
        date(2024, 11, 14),
        date(2024, 11, 19),
        date(2024, 11, 21),
        date(2024, 12, 3),
        date(2024, 12, 5),
    ]
    
    schedule = [
        {"name": "Introduction", "notes": "assets/slides/lec1-intro.pdf"},
        {"name": "Overview of the internet", "notes": None},
        {"name": "Naming and addressing", "notes": None},
        {"name": "Physical layer design considerations", "notes": None},
        {"name": "Physical layer data encoding and multiplexing", "notes": None},
        {"name": "Media access control (MAC)", "notes": None},
        {"name": "Reliable transmission, error detection and correction", "notes": None},
        {"name": "Spanning tree routing", "notes": None},
        {"name": "Distance vector and link state routing", "notes": None},
        {"name": "<b>Quiz 1</b>", "notes": None},
        {"name": "Inter domain routing", "notes": None},
        {"name": "Inter domain routing continued", "notes": None},
        {"name": "Transport layer reliability", "notes": None},
        {"name": "Congestion control", "notes": None},
        {"name": "Congestion control 2", "notes": None},
        {"name": "Queuing mechanisms and centralized bandwidth allocation", "notes": None},
        {"name": "The Domain Name System (DNS)", "notes": None},
        {"name": "HTTP and the web", "notes": None},
        {"name": "<b>Quiz 2</b>", "notes": None},
        {"name": "Content Delivery Networks (CDNs)", "notes": None},
        {"name": "Putting it all together: Journey of a web page", "notes": None},
        {"name": "Traffic engineering", "notes": None},
        {"name": "The scarcity of addresses: NAT and IPv6", "notes": None},
        {"name": "Virtual Private Networks (VPNs)", "notes": None},
        {"name": "Reverse proxies", "notes": None},
        {"name": "Encryption 1", "notes": None},
        {"name": "Encryption 2 and managing certificates", "notes": None},
        {"name": "Web security", "notes": None},
    ]

    if len(schedule) > len(dates):
        print("Warning: there are more planned classes than are available in the schedule!")
    while len(dates) > len(schedule):
        schedule += [{"name": "TBD", "notes": None}]
    assert len(schedule) >= len(dates)

    for i in range(len(dates)):
        schedule[i]["date"] = dates[i].strftime("%a, %b %d")
        schedule[i]["number"] = i+1
        #print(i, schedule[i], dates[i])
    
    return schedule

if __name__ == "__main__":
    env = Environment(
        loader=FileSystemLoader("templates/"),
        # autoescape=select_autoescape()
    )
    
    with open("index.html", "w") as index_file:
        index_template = env.get_template("index.html")
        rendered = index_template.render(navigation=prep_navigation("Home"))
        index_file.write(rendered)

    with open("schedule.html", "w") as schedule_file:
        schedule_template = env.get_template("schedule.html")
        rendered = schedule_template.render(schedule=prep_schedule(), navigation=prep_navigation("Schedule"))
        schedule_file.write(rendered)

    with open("assignments.html", "w") as assignments_file:
        assignments_template = env.get_template("assignments.html")
        rendered = assignments_template.render(navigation=prep_navigation("Assignments"))
        assignments_file.write(rendered)
