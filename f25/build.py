from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape


def prep_navigation(active: str):
    navigation = [
        {"name": "Home", "url": "index.html"},
        {"name": "Schedule", "url": "schedule.html"},
        {"name": "Assignments", "url": "assignments.html"},
        {"name": "Ed Discussion", "url": "https://edstem.org/us/courses/84822/discussion"},
        {"name": "Canvas", "url": "https://utexas.instructure.com/courses/1421734"}
    ]
    for i in range(len(navigation)):
        if navigation[i]["name"] == active:
            navigation[i]["active"] = True
        else:
            navigation[i]["active"] = False
    return navigation

def prep_schedule():
    dates = [
        # August
        date(2025,  8, 26),  # Tue
        date(2025,  8, 28),  # Thu

        # September
        date(2025,  9,  2),  # Tue
        date(2025,  9,  4),  # Thu
        date(2025,  9,  9),  # Tue
        date(2025,  9, 11),  # Thu
        date(2025,  9, 16),  # Tue
        date(2025,  9, 18),  # Thu
        date(2025,  9, 23),  # Tue
        date(2025,  9, 25),  # Thu
        date(2025,  9, 30),  # Tue

        # October
        date(2025, 10,  2),  # Thu
        date(2025, 10,  7),  # Tue
        date(2025, 10,  9),  # Thu
        date(2025, 10, 14),  # Tue
        date(2025, 10, 16),  # Thu
        date(2025, 10, 21),  # Tue
        date(2025, 10, 23),  # Thu
        date(2025, 10, 28),  # Tue
        date(2025, 10, 30),  # Thu

        # November (before Thanksgiving break)
        date(2025, 11,  4),  # Tue
        date(2025, 11,  6),  # Thu
        # Skip Nov 11? 2025-11-11 is Tuesday but Veterans Day isn't listed as a UT holiday—only Thanksgiving break is. So include it:
        date(2025, 11, 11),  # Tue
        date(2025, 11, 13),  # Thu
        date(2025, 11, 18),  # Tue
        date(2025, 11, 20),  # Thu
        # Skip week of Nov 24–29 (break)
        date(2025, 12,  2),  # Tue
        date(2025, 12,  4),  # Thu
    ]
    
    schedule = [
        {"name": "Introduction", "notes": "assets/slides/lec1-intro.pdf"},
        {"name": "Overview of the internet", "notes": "assets/slides/lec2-architecture.pdf"},
        {"name": "Naming and addressing", "notes": "assets/slides/lec3-names.pdf"},
        {"name": "Spanning tree routing", "notes": "assets/slides/lec4-routing-1.pdf"},
        {"name": "Distance vector and link state routing", "notes": "assets/slides/lec5-routing-2.pdf"},
        {"name": "Inter domain routing", "notes": "assets/slides/lec6-bgp.pdf"},
        {"name": "Inter domain routing continued", "notes": "assets/slides/lec7-bgp-advanced.pptx"},
        {"name": "Voltages to bits", "notes": "assets/slides/lec8-phy-1.pdf"},
        {"name": "Error detection and reliability", "notes": "assets/slides/lec9-error-detect.pdf"},
        {"name": "Forward error correction and neural networks", "notes": "assets/slides/lec11-error-correction-and-quiz.pptx"},
        {"name": "<b>Quiz 1</b>", "notes": None},
        {"name": "Media access control (MAC)", "notes": "assets/slides/lec12-mac-protocols.pptx"},
        {"name": "Transport layer: flow control and reliaiblity", "notes": "assets/slides/lec13-transport-intro.pdf"},
        {"name": "Transport layer: alternate designs", "notes": "assets/slides/lec14-transport-adv-reliability.pdf"},
        {"name": "Congestion control 1", "notes": "assets/slides/lec15-congestion-control-1.pptx"},
        {"name": "Queuing Disciplines and Switches", "notes": "assets/slides/lec16-qd-and-switches.pdf"},
        # {"name": "Recap: BGP and FEC", "notes": None},
        # {"name": "Queuing disciplines + HTTP and the web", "notes": "assets/slides/lec18-qd-and-app.pdf"},
        {"name": "Encryption 1", "notes": "assets/slides/lec19-security-crypto.pdf"},
        {"name": "Encryption 2", "notes": "assets/slides/lec20-security-crypto-2.pdf"},
        {"name": "Web security", "notes": "assets/slides/lec22-practical-security.pdf"},
        {"name": "<b>Quiz 2</b>", "notes": None},
        {"name": "HTTP and the web", "notes": None},
        {"name": "Overlay networks", "notes": None},
        {"name": "Datacenter networks", "notes": "assets/slides/lec23-datacenter-networks.pdf"},
        #{"name": "Programmable network devices (guest lecture by Daehyoek Kim)", "notes": "assets/slides/lec24-programmable-networks.pdf"},
        {"name": "Content Delivery Networks (CDNs)", "notes": "assets/slides/lec25-cdn.pdf"},
        #{"name": "Putting it all together: Journey of a web page", "notes": None},
        {"name": "The scarcity of addresses: NAT and IPv6", "notes": "assets/slides/lec26-nat-ipv6-overlay.pptx"},
        {"name": "Course review: the philosophy of internet design", "notes": None},
        {"name": "<b>Quiz 3</b>", "notes": None},
        #{"name": "Reverse proxies", "notes": None},
    ]

    if len(schedule) > len(dates):
        print(f"Warning: there are more planned classes {len(schedule)} than are available in the schedule {len(dates)}!")
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
