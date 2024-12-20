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
        #date(2024, 11, 12),
        date(2024, 11, 14),
        date(2024, 11, 19),
        date(2024, 11, 21),
        date(2024, 12, 3),
        date(2024, 12, 5),
    ]
    
    schedule = [
        {"name": "Introduction", "notes": "assets/slides/lec1-intro.pdf"},
        {"name": "Overview of the internet", "notes": "assets/slides/lec2-architecture.pdf"},
        {"name": "Naming and addressing", "notes": "assets/slides/lec3-names.pdf"},
        {"name": "Spanning tree routing", "notes": "assets/slides/lec4-routing-1.pdf"},
        {"name": "Distance vector and link state routing", "notes": "assets/slides/lec5-routing-2.pdf"},
        {"name": "Inter domain routing", "notes": "assets/slides/lec6-bgp.pdf"},
        {"name": "Inter domain routing continued", "notes": "assets/slides/lec7-bgp-advanced.pptx"},
        {"name": "Physical layer design considerations", "notes": "assets/slides/lec8-phy-1.pdf"},
        {"name": "Physical layer error detection and reliability", "notes": "assets/slides/lec9-error-detect.pdf"},
        {"name": "<b>Quiz 1</b>", "notes": None},
        {"name": "Quiz 1 recap and error correction", "notes": "assets/slides/lec11-error-correction-and-quiz.pptx"},
        {"name": "Media access control (MAC)", "notes": "assets/slides/lec12-mac-protocols.pptx"},
        {"name": "Transport layer: flow control and reliaiblity", "notes": "assets/slides/lec13-transport-intro.pdf"},
        {"name": "Transport layer: alternate designs", "notes": "assets/slides/lec14-transport-adv-reliability.pdf"},
        {"name": "Congestion control 1", "notes": "assets/slides/lec15-congestion-control-1.pptx"},
        {"name": "Congestion control 2", "notes": None},
        {"name": "Recap: BGP and FEC", "notes": None},
        {"name": "Queuing disciplines + HTTP and the web", "notes": "assets/slides/lec18-qd-and-app.pdf"},
        {"name": "Encryption 1", "notes": "assets/slides/lec19-security-crypto.pdf"},
        {"name": "<b>Quiz 2</b>", "notes": None},
        {"name": "Encryption 2", "notes": "assets/slides/lec20-security-crypto-2.pdf"},
        {"name": "Web security", "notes": "assets/slides/lec22-practical-security.pdf"},
        {"name": "Datacenter Networks", "notes": "assets/slides/lec23-datacenter-networks.pdf"},
        {"name": "Programmable network devices (guest lecture by Daehyoek Kim)", "notes": "assets/slides/lec24-programmable-networks.pdf"},
        {"name": "Content Delivery Networks (CDNs)", "notes": "assets/slides/lec25-cdn.pdf"},
        #{"name": "HTTP and the web", "notes": None},
        #{"name": "Putting it all together: Journey of a web page", "notes": None},
        {"name": "The scarcity of addresses: NAT and IPv6", "notes": "assets/slides/lec26-nat-ipv6-overlay.pptx"},
        {"name": "Course review: the philosophy of internet design", "notes": None},
        #{"name": "Reverse proxies", "notes": None},
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
