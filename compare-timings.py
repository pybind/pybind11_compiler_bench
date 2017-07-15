#!/usr/bin/python3
from __future__ import print_function
import sys
from math import sqrt

if len(sys.argv) < 2:
    raise RuntimeError("Invalid usage.  Specify one or more files with `NAME CPU MEM` triplets on each line")

stats = {}

inputs = sys.argv[1:]
for f in inputs:
    with open(f) as file:
        stats[f] = {}
        for line in file:
            data = line.split()
            assert len(data) == 3
            name, cpu, mem = data[0], float(data[1]), float(data[2])
            if not name in stats[f]:
                stats[f][name] = {"n": 0, "cpu_agg": 0, "mem_agg": 0, "cpu^2_agg": 0, "mem^2_agg": 0}
            stats[f][name]["n"] += 1
            stats[f][name]["cpu_agg"] += cpu
            stats[f][name]["mem_agg"] += mem
            stats[f][name]["cpu^2_agg"] += cpu**2
            stats[f][name]["mem^2_agg"] += mem**2

names = set()
for f in inputs:
    names |= set(stats[f].keys())
    for name, s in stats[f].items():
        for stat in ["cpu", "mem"]:
            n = s["n"]
            s[stat + "_mean"] = s[stat + "_agg"] / n
            s[stat + "_sd"] = float('nan') if n == 1 else sqrt(1. / (n-1) * (s[stat + "^2_agg"] - n * s[stat + "_mean"] ** 2))

names = sorted(names)
namelen = max(len(i) for i in names)

valsfmt0     = "   {:>6.3f} ({:>5.3f})   {:>6.0f} ({:>6.1f})"
valsfmt_str0 = "   {:^6"+"} ({:^5"+"})   {:^6"+"} ({:^6"+"})"
vals_ul0     = "   " + "-"*(6+5+3) + "   " + "-"*(6+6+3)

valsfmt      = "   {:>6.3f} ({:>5.3f}) ({:>+7.2%})   {:>6.0f} ({:>6.1f}) ({:>+7.2%})"
valsfmt_str  = "   {:^6"+"} ({:^5"+"}) ({:^7" +"})   {:^6"+"} ({:^6"+"}) ({:^7" +"})"
vals_ul      = "   " + "-" * (6 + 5 + 7 + 6)   + "   " + "-" * (6 + 6 + 7 + 6)

extra_inputs = len(inputs) - 1

valslen0 = len(valsfmt0.format(0, 0, 0, 0))
valslen = len(valsfmt.format(0, 0, 0, 0, 0, 0))
fmt = "{:>" + str(namelen) + "}:" + valsfmt0 + valsfmt * extra_inputs
headerfmt = (" " * (namelen + 1) +
    ("   {:^" + str(valslen0 - 3) + "}") +
    ("   {:^" + str(valslen  - 3) + "}") * extra_inputs)

def file_n(f):
    ns = sorted(set(stats[f][name]["n"] for name in names))
    return "[n=" + ','.join(map(str, ns)) + "]"

print(headerfmt.format(*(f + " " + file_n(f) for f in inputs)))
print(headerfmt.format("=" * (valslen0 - 3), *(["=" * (valslen - 3)] * extra_inputs)))
print(" " * (namelen + 1) +
    valsfmt_str0.format("CPU", "s.d.", "MaxRSS", "s.d.") +
    valsfmt_str.format("CPU", "s.d.", "+/-", "MaxRSS", "s.d.", "+/-") * extra_inputs)
print(" " * (namelen + 1) + vals_ul0 + vals_ul * extra_inputs)

for name in names:
    for f in inputs:
        for s in ["cpu", "mem"]:
            stats[f][name][s + "_diff"] = stats[f][name][s + "_mean"] / stats[inputs[0]][name][s + "_mean"] - 1
    print(fmt.format(name,
        *([stats[inputs[0]][name][s] for s in ["cpu_mean", "cpu_sd", "mem_mean", "mem_sd"]] +
          [stats[f][name][s] for f in inputs[1:] for s in ["cpu_mean", "cpu_sd", "cpu_diff", "mem_mean", "mem_sd", "mem_diff"]])
    ))
