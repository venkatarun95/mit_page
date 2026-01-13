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
        # date(2025, 3, 13), # Spring break
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
        # {"name": "Introduction", "reading": [("PIM: Matching in a switch", "https://dl.acm.org/doi/pdf/10.1145/161541.161736"), ("dcPIM: Matching in a datacenter", "https://www.cs.cornell.edu/~ragarwal/pubs/dcpim.pdf")], "optional": [("How to read papers", "https://cs.utexas.edu/~venkatar/sys_perf_analysis/how-to-read-paper.pdf")]},
        {"name": "Introduction", "reading": [("Notes: When should we use which operation?", "papers/notes_when_to_use_which_operation.pdf")], "optional": [("How to read papers", "https://cs.utexas.edu/~venkatar/sys_perf_analysis/how-to-read-paper.pdf")]},
        # {"name": "Class cancelled due to 🛫", "reading": []},
        # {"name": "Class cancelled due to ❄️", "reading": []},
        {"name": "Load balancing", "reading": [("Valiant routing in a switch", "https://www.cs.utexas.edu/~venkatar/sys_perf_analysis/valiant-optics.pdf"), ("Valiant routing in Google's datacenter", "https://www.cs.utexas.edu/~venkatar/sys_perf_analysis/plb.pdf")], "optional": [("Original paper by Valiant", "Universal schemes for parallel communication")]},
        {"name": "Power of two choices", "reading": [("Empirical blog", "https://www.haproxy.com/blog/power-of-two-load-balancing"), ("Survey of theory", "https://www.eecs.harvard.edu/~michaelm/postscripts/handbook2001.pdf")], "optional": [("Sparrow scheduler", "https://people.eecs.berkeley.edu/~matei/papers/2013/sosp_sparrow.pdf")]},
        {"name": "Notions of fairness I", "reading": [("Chapter 2.2 (&alpha;-fairness) and 2.4 (NUM) of R. Srikant and Lei Y. (alpha fairness and NUM)", "https://sites.google.com/view/comm-network")], "optional": []},
        {"name": "Notions of fairness II", "reading": [("Dominant Resource Fairness", "https://www.usenix.org/legacy/event/nsdi11/tech/full_papers/Ghodsi.pdf")]},
        {"name": "Notions of fairness III", "reading": [("FairCloud (fairness is hard)", "https://dl.acm.org/doi/pdf/10.1145/2342356.2342396")], "optional": []},
        # DHT
        # VL2
        {"name": "Overload control", "reading": [("Overload control (Breakwater)", "https://www.usenix.org/conference/nsdi14/technical-sessions/presentation/zhang")], "optional": []},
        {"name": "Process scheduling I", "reading": [("Work stealing theoretical analysis", "https://dl.acm.org/doi/pdf/10.1145/324133.324234")], "optional": [("Cilk programming model", "../sys_perf_analysis/ws_cilk.pdf"), ("Empirical analysis that concludes work stealing is best", "../sys_perf_analysis/ws_empirical.pdf")]},
        {"name": "Process scheduling II", "reading": [("Decades of wasted cores in Linux", "papers/wasted-cores.pdf"),  ("More bugs discovered through verification (section 5 only)", "https://arxiv.org/pdf/2301.04205")], "optional": [("Scheduler in Linux v4.6.8.1", "https://www.kernel.org/doc/Documentation/scheduler/sched-design-CFS.txt")]},
        # {"name": "When should we use which mathematical operation?", "reading": [("Notes", "papers/notes_when_to_use_which_operation.pdf")], "optional": [("L1 vs L2 norms and compressed sensing", "http://timroughgarden.org/f14/l/l9.pdf")]},
        {"name": "Caching replacement policies I", "reading": [("Tim Roughgarden's beyond worst-case lecture 3", "http://timroughgarden.org/f14/l/l3.pdf"), ("Tim Roughgarden's beyond worst-case lecture 4", "http://timroughgarden.org/f14/l/l4.pdf")], "optional": []},
        {"name": "Cache replacement policies II", "reading": [("Caching with delayed hits", "../sys_perf_analysis/belatedly.pdf")], "optional": []},
        {"name": "Incorporating ML in systems I", "reading": [("ML improves the average. Theory bounds the worst", "../sys_perf_analysis/competitive_caching_ml_advice.pdf")], "optional": []},
        {"name": "Incorporating ML in systems II", "reading": [("Traffic engineering by using ML to solve LPs faster", "https://dl.acm.org/doi/pdf/10.1145/3603269.3604857")], "optional": [("Solving computationally hard problems with AlphaZero", "https://arxiv.org/pdf/1712.01815")]},
        {"name": "Computational complexity in practice I", "reading": [("Notes", "papers/complexity_in_practice.pdf")], "optional": []},
        {"name": "Computational complexity in practice II", "reading": [("Notes", "papers/complexity_in_practice.pdf")], "optional": []},
        {"name": "Signal processing tasting menu I", "reading": [("Rule: use sinusoids", "https://venkatarun.wordpress.com/2022/04/18/why-the-sinusoid/"), ("Learn the rule to break it", "https://dl.acm.org/doi/pdf/10.1145/3230543.3230565")], "optional": []},
        {"name": "Signal processing tasting menu II", "reading": [("Funamental Limits (read before 7.1.1 and skim the rest)", "https://ethz.ch/content/dam/ethz/special-interest/itet/photonics-dam/documents/lectures/EandM/AngularSpectrumRepresentation.pdf"), ("Use the limits", "https://www.usenix.org/system/files/nsdi20-paper-arun.pdf")], "optional": []},
        {"name": "Congestion control I", "reading": [("AIMD analysis", "https://www.cs.columbia.edu/~danr/courses/6761/Summer03/week4/aimd.pdf"), ("Delay based multi-bottleneck CC (pay attention to IIIB)", "https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=4032738")], "optional": []},
        {"name": "Guest lecture by Tegan Wilson", "reading": [("Oblivious reconfigurable networks (sections 3, 4.3, 4.4, and 4.5 are optional)", "https://dl.acm.org/doi/10.1145/3519935.3520020"), ("Real-world version of the above idea in practice", "https://dl.acm.org/doi/10.1145/3651890.3672248")], "optional": []},
        {"name": "Congestion control II/Performance Verifiaction I", "reading": [("Everything is broken", "https://dl.acm.org/doi/pdf/10.1145/3452296.3472912"), ("Everything is unfair", "https://dl.acm.org/doi/pdf/10.1145/3544216.3544223")], "optional": []},
        # {"name": "Congestion control III", "reading": [], "optional": []},
        {"name": "Performance verification II", "reading": [("How broken are optimizers?", "https://www.usenix.org/system/files/nsdi24-namyar-finding.pdf")], "optional": []},
        {"name": "Performance verification III", "reading": [("Hoe complex is my distributed system?", "https://dl.acm.org/doi/pdf/10.1145/3591235")], "optional": []},
        # {"name": "Bounding performance I", "reading": [], "optional": []},
        {"name": "Hardware abstractions for performance I", "reading": [("Hardware for sparse linear algebra", "https://dl.acm.org/doi/pdf/10.1145/3582016.3582051")], "optional": []},
        {"name": "Abstractions that aid performance II", "reading": [("PIFO", "https://dl.acm.org/doi/pdf/10.1145/2934872.2934899"), ("Approximate PIFO", "https://www.usenix.org/system/files/nsdi20-paper-alcoz.pdf")], "optional": []},
        {"name": "Project presentations I", "reading": [], "optional": []},
        {"name": "Project presentations II", "reading": [], "optional": []}
    ]

    other_papers = [
        ("Adaptive Work Stealing with Parallelism Feedback", "https://dl.acm.org/doi/10.1145/1394441.1394443"),
        ("Multiplicative Weights Update Method: A Meta Algorithm and Applications", "https://theoryofcomputing.org/articles/v008a006/v008a006.pdf"),
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
