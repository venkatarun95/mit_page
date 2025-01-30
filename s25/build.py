from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape


def prep_navigation(active: str):
    navigation = [
        {"name": "Home", "url": "index.html"},
        {"name": "Schedule", "url": "schedule.html"},
        {"name": "Ed Discussion", "url": "https://edstem.org/us/courses/74525/discussion"},
        {"name": "Canvas", "url": "https://utexas.instructure.com/courses/1414782"}
    ]
    for i in range(len(navigation)):
        if navigation[i]["name"] == active:
            navigation[i]["active"] = True
        else:
            navigation[i]["active"] = False
    return navigation

def prep_schedule():
    dates = [
        date(2025,  1, 14),
        date(2025,  1, 16),
        date(2025,  1, 21),
        date(2025,  1, 23),
        date(2025,  1, 28),
        date(2025,  1, 30),
        date(2025, 2, 4),
        date(2025, 2, 6),
        date(2025, 2, 11),
        date(2025, 2, 13),
        date(2025, 2, 18),
        date(2025, 2, 20),
        date(2025, 2, 25),
        date(2025, 2, 27),
        date(2025, 3, 4),
        date(2025, 3, 6),
        date(2025, 3, 11),
        date(2025, 3, 13), # Spring break
        date(2025, 3, 25),
        date(2025, 3, 27),
        date(2025, 4, 1),
        date(2025, 4, 3),
        date(2025, 4, 8),
        date(2025, 4, 10),
        date(2025, 4, 15),
        date(2025, 4, 17),
        date(2025, 4, 22),
        date(2025, 4, 24),
    ]

    schedule = [
        {"name": "Introduction", "reading": [("PIM: Matching in a switch", "https://dl.acm.org/doi/pdf/10.1145/161541.161736"), ("dcPIM: Matching in a datacenter", "https://www.cs.cornell.edu/~ragarwal/pubs/dcpim.pdf")], "optional": [("How to read papers", "https://cs.utexas.edu/~venkatar/sys_perf_analysis/how-to-read-paper.pdf")]},
        {"name": "Class cancelled due to 🛫", "reading": []},
        {"name": "Class cancelled due to ❄️", "reading": []},
        {"name": "Load balancing", "reading": [("Valiant routing in a switch", "https://www.cs.utexas.edu/~venkatar/sys_perf_analysis/valiant-optics.pdf"), ("Valiant routing in Google's datacenter", "https://www.cs.utexas.edu/~venkatar/sys_perf_analysis/plb.pdf")], "optional": [("Original paper by Valiant", "Universal schemes for parallel communication")]},
        {"name": "Power of two choices", "reading": [("Empirical blog", "https://www.haproxy.com/blog/power-of-two-load-balancing"), ("Survey of theory", "https://www.eecs.harvard.edu/~michaelm/postscripts/handbook2001.pdf")], "optional": [("Sparrow scheduler", "https://people.eecs.berkeley.edu/~matei/papers/2013/sosp_sparrow.pdf")]},
        {"name": "Notions of fairness I", "reading": [("Chapter 2.2 and 2.4 of R. Srikant and Lei Y. (alpha fairness and NUM)", "https://sites.google.com/view/comm-network")], "optional": []},
        {"name": "Notions of fairness II", "reading": [], "optional": []},
        {"name": "Notions of fairness III", "reading": [], "optional": []},
        # DHT
        # VL2
        # {"name": "Overload control", "reading": [("Overload control (Breakwater)", "https://www.usenix.org/conference/nsdi14/technical-sessions/presentation/zhang")], "optional": []},
        {"name": "Process scheduling I", "reading": [("Work stealing theoretical analysis", "https://dl.acm.org/doi/10.1145/277505.277526"), ("Cilk programming model", "https://dl.acm.org/doi/10.1145/262004.262005"), ("Empirical analysis that concludes work stealing is best", "https://dl.acm.org/doi/10.1145/1073970.1073974")], "optional": []},
        {"name": "Process scheduling II", "reading": [("Decades of wasted cores in Linux", "https://www.usenix.org/system/files/conference/osdi16/osdi16-peng.pdf")], "optional": [("Scheduler in Linux v4.6.8.1", "https://www.kernel.org/doc/Documentation/scheduler/sched-design-CFS.txt"), ("More bugs discovered through verification", "https://arxiv.org/abs/1802.02181")]},
        {"name": "Caching replacement policies I", "reading": [], "optional": []},
        {"name": "Cache replacement policies II", "reading": [], "optional": []},
        {"name": "Incorporating ML in systems I", "reading": [], "optional": []},
        {"name": "Incorporating ML in systems II", "reading": [], "optional": []},
        {"name": "Incorporating ML in systems III", "reading": [], "optional": []},
        {"name": "Computational complexity in practice I", "reading": [], "optional": []},
        {"name": "Computational complexity in practice II", "reading": [], "optional": []},
        {"name": "Computational complexity in practice III", "reading": [], "optional": []},
        {"name": "Congestion control I", "reading": [], "optional": []},
        {"name": "Congestion control II", "reading": [], "optional": []},
        {"name": "Congestion control III", "reading": [], "optional": []},
        {"name": "Performance verification I", "reading": [], "optional": []},
        {"name": "Performance verification II", "reading": [], "optional": []},
        {"name": "Bounding performance I", "reading": [], "optional": []},
        {"name": "Abstractions that aid performance I", "reading": [], "optional": []},
        {"name": "Abstractions that aid performance II", "reading": [], "optional": []},
        {"name": "Project presentations I", "reading": [], "optional": []},
        {"name": "Project presentations II", "reading": [], "optional": []}
    ]

    if len(schedule) > len(dates):
        print("Warning: there are more planned classes than are available in the schedule!")
    while len(dates) > len(schedule):
        schedule += [{"name": "TBD", "notes": []}]
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
