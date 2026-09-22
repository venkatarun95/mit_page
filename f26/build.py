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
        "Introduction", "Overview of the internet", "Using LLMs", "Naming and addressing", "Spanning tree routing",
        "Distance vector and link state routing", "Inter-domain routing", "Inter-domain routing continued",
        "Traffic Engineering", "Error detection and reliability", "Quiz 1",
        "Media access control (MAC)", "Transport layer: flow control and reliability",
        "Transport layer: alternate designs", "Congestion control", "Queuing disciplines and switches",
        "Encryption 1", "Encryption 2", "Web security", "Quiz 2", "Putting it all together",
        "HTTP and the web", "Datacenter networks", "Content delivery networks (CDNs)",
        "The scarcity of addresses: NAT and IPv6", "Designing a modern application", "Quiz 3", "Completely optional class",
    ]
    notes = [
        "lec1-intro.pdf", "lec2-architecture.pdf", "lec3-agentic-coding.pdf", "lec3-names.pdf", "lec4-routing-1.pdf",
        "lec5-routing-2.pdf", "lec6-bgp.pdf", "lec7-bgp-advanced.pptx", 
        "lec9-te.pdf", "lec9-error-detect.pdf", None,
        "lec12-mac-protocols.pptx", "lec13-transport-intro.pdf", "lec14-transport-adv-reliability.pdf",
        "lec15-congestion-control-1.pdf", "lec16-qd-and-switches.pdf", "lec19-security-crypto.pdf",
        "lec20-security-crypto-2.pdf", "lec22-practical-security.pdf", None, "lec22-web.pdf",
        "lec22-web.pdf", "lec23-datacenter-networks.pdf", "lec25-cdn.pdf", "lec26-nat-ipv6-overlay.pptx",
        None, None, None,
    ]
    return [
        {"number": i + 1, "date": day.strftime("%a, %b %d"), "name": name, "notes": notes[i]}
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
