from datetime import date
from jinja2 import Environment, FileSystemLoader


def prep_navigation(active: str):
    navigation = [
        {"name": "Home", "url": "index.html"},
        {"name": "Schedule", "url": "schedule.html"},
        {"name": "Assignments", "url": "assignments.html"},
        {"name": "Ed Discussion", "url": "https://edstem.org/us/courses/102831/discussion"},
        {"name": "Canvas", "url": "https://utexas.instructure.com/courses/1450929"},
    ]
    for item in navigation:
        item["active"] = item["name"] == active
    return navigation


def prep_schedule():
    dates = [
        date(2026, 8, 25), date(2026, 8, 27),
        date(2026, 9, 1), date(2026, 9, 3), date(2026, 9, 8), date(2026, 9, 10),
        date(2026, 9, 15), date(2026, 9, 17), date(2026, 9, 22), date(2026, 9, 24), date(2026, 9, 29),
        date(2026, 10, 1), date(2026, 10, 6), date(2026, 10, 8), date(2026, 10, 13), date(2026, 10, 15),
        date(2026, 10, 20), date(2026, 10, 22), date(2026, 10, 27), date(2026, 10, 29),
        date(2026, 11, 3), date(2026, 11, 5), date(2026, 11, 10), date(2026, 11, 12), date(2026, 11, 17), date(2026, 11, 19),
        date(2026, 12, 1), date(2026, 12, 3),
    ]
    schedule = [
        "Introduction", "Overview of the internet", "Naming and addressing", "Spanning tree routing",
        "Distance vector and link state routing", "Inter-domain routing", "Inter-domain routing continued",
        "Voltages to bits", "Error detection and reliability", "Forward error correction", "Quiz 1",
        "Media access control (MAC)", "Transport layer: flow control and reliability",
        "Transport layer: alternate designs", "Congestion control", "Queuing disciplines and switches",
        "Encryption 1", "Encryption 2", "Web security", "Quiz 2", "Putting it all together",
        "HTTP and the web", "Datacenter networks", "Content delivery networks (CDNs)",
        "The scarcity of addresses: NAT and IPv6", "Designing a modern application", "Quiz 3", "TBD",
    ]
    return [
        {"number": i + 1, "date": day.strftime("%a, %b %d"), "name": name}
        for i, (day, name) in enumerate(zip(dates, schedule))
    ]


if __name__ == "__main__":
    env = Environment(loader=FileSystemLoader("templates/"))
    for filename, active, context in [
        ("index.html", "Home", {}),
        ("schedule.html", "Schedule", {"schedule": prep_schedule()}),
        ("assignments.html", "Assignments", {}),
    ]:
        template = env.get_template(filename)
        with open(filename, "w") as output:
            output.write(template.render(navigation=prep_navigation(active), **context))
