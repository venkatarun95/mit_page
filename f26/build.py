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
    lectures = {
        "Introduction": "lec1-intro.pdf",
        "Overview of the internet": "lec2-architecture.pdf",
        "Using LLMs": "lec3-agentic-coding.pdf",
        "Naming and addressing": "lec3-names.pdf",
        "Spanning tree routing": "lec4-routing-1.pdf",
        "Distance vector and link state routing": "lec5-routing-2.pdf",
        "Inter-domain routing": "lec6-bgp.pdf",
        "Inter-domain routing continued": "lec7-bgp-advanced.pptx",
        "Traffic Engineering": "lec9-te.pdf",
        "Error detection and correction": "lec9-error-detect-correct.pdf",
        "Quiz 1": None,
        "Transport layer: flow control and reliability": "lec13-transport-intro.pdf",
        "Congestion control": "lec15-congestion-control-1.pdf",
        "Transport layer: alternate designs": "lec14-transport-adv-reliability.pdf",
        "Physical layer transmission": "lec8-phy-1.pdf",
        "Media access control (MAC)": "lec12-mac-protocols.pptx",
        "Queuing disciplines and switches": "lec16-qd-and-switches.pdf",
        "Encryption 1": "lec19-security-crypto.pdf",
        "Encryption 2": "lec20-security-crypto-2.pdf",
        "Web security": "lec22-practical-security.pdf",
        "Quiz 2": None,
        "Putting it all together": "lec22-web.pdf",
        "HTTP and the web": "lec22-web.pdf",
        "Datacenter networks": "lec23-datacenter-networks.pdf",
        "Content delivery networks (CDNs)": "lec25-cdn.pdf",
        "The scarcity of addresses: NAT and IPv6": "lec26-nat-ipv6-overlay.pptx",
        "Designing a modern application": None,
        "Quiz 3": None,
        "Completely optional class": None,
    }
    return [
        {"number": i + 1, "date": day.strftime("%a, %b %d"), "name": name, "notes": notes}
        for i, (day, (name, notes)) in enumerate(zip(dates, lectures.items()))
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
