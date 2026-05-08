#!/usr/bin/env python3
"""
analyze_results.py
==================
Reads OMNeT++ .sca result files OR uses direct simulation values
to produce the 3-panel analysis chart matching the lab requirements.

Usage:
    python analyze_results.py
"""

import os
import re
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# OPTION A: Read from OMNeT++ .sca files
# ─────────────────────────────────────────────────────────────────────────────

def parse_sca_files(results_dir="results"):
    """
    Parse all .sca files and collect ALL finalHopCount scalar values.
    In OMNeT++ each recordScalar() call writes one line like:
        scalar HopCountNet.receiver finalHopCount 9
    """
    run_data = {}   # run_label -> {'hops': [...], 'dropped': int}

    if not os.path.isdir(results_dir):
        return run_data

    for fname in sorted(os.listdir(results_dir)):
        if not fname.endswith(".sca"):
            continue

        filepath   = os.path.join(results_dir, fname)
        run_label  = os.path.splitext(fname)[0]   # e.g. "HopCount-Run1"
        hops       = []
        dropped    = 0

        with open(filepath) as f:
            for line in f:
                line = line.strip()
                # Match:  scalar <module> finalHopCount <value>
                m = re.match(r'^scalar\s+\S+\s+finalHopCount\s+([\d.]+)', line)
                if m:
                    hops.append(int(float(m.group(1))))
                    continue
                # Match:  scalar <module> droppedPackets <value>
                m = re.match(r'^scalar\s+\S+\s+droppedPackets\s+([\d.]+)', line)
                if m:
                    dropped += int(float(m.group(1)))

        if hops:
            run_data[run_label] = {'hops': hops, 'dropped': dropped}

    return run_data


# ─────────────────────────────────────────────────────────────────────────────
# OPTION B: Hardcoded values from OMNeT++ console output
#   → Fill these in from your simulation EV logs
#   → Format:  seed -> (hopCounts_list, dropped_count)
# ─────────────────────────────────────────────────────────────────────────────

MANUAL_RESULTS = {
    42:   {'hops': [], 'dropped': 0},   # fill after Run1
    100:  {'hops': [], 'dropped': 0},   # fill after Run2
    255:  {'hops': [], 'dropped': 0},   # fill after Run3
    777:  {'hops': [], 'dropped': 0},   # fill after Run4
    1234: {'hops': [], 'dropped': 0},   # fill after Run5
    9999: {'hops': [], 'dropped': 0},   # fill after Run6
}

# ─────────────────────────────────────────────────────────────────────────────
# OPTION C: Python simulation (matches NED topology exactly)
#   Used when neither .sca files nor manual results are available
# ─────────────────────────────────────────────────────────────────────────────

import random

GRAPH = {
    'sender': ['r0'],
    'r0':  ['r1', 'r2', 'r3'],
    'r1':  ['r4', 'r5', 'r2'],
    'r2':  ['r4', 'r6', 'r5'],
    'r3':  ['r5', 'r7', 'r6'],
    'r4':  ['r6', 'r8', 'r7'],
    'r5':  ['r7', 'r8', 'r9'],
    'r6':  ['r8', 'r9'],
    'r7':  ['r9', 'r8'],
    'r8':  ['r9'],
    'r9':  ['receiver', 'r6', 'r7'],
    'receiver': []
}

def simulate_seed(seed, num_packets=50):
    rng = random.Random(seed)
    hops, dropped = [], 0
    for _ in range(num_packets):
        node, h, ttl, arrived = 'sender', 0, 20, False
        while ttl > 0:
            nb = GRAPH.get(node, [])
            if not nb: break
            node = rng.choice(nb)
            h += 1; ttl -= 1
            if node == 'receiver':
                hops.append(h); arrived = True; break
        if not arrived:
            dropped += 1
    return {'hops': hops, 'dropped': dropped}

SEEDS = [42, 100, 255, 777, 1234, 9999]

# ─────────────────────────────────────────────────────────────────────────────
# Decide which data source to use
# ─────────────────────────────────────────────────────────────────────────────

sca_data = parse_sca_files("results")

if sca_data:
    print("[INFO] Using data from .sca result files.\n")
    results = {}
    for label, d in sca_data.items():
        results[label] = d
    labels = sorted(results.keys())

elif any(MANUAL_RESULTS[s]['hops'] for s in SEEDS):
    print("[INFO] Using manually entered results.\n")
    results = {f"Seed {s}": MANUAL_RESULTS[s] for s in SEEDS}
    labels  = list(results.keys())

else:
    print("[INFO] No .sca files found. Running Python simulation.\n")
    results = {f"Seed {s}": simulate_seed(s) for s in SEEDS}
    labels  = list(results.keys())

# ─────────────────────────────────────────────────────────────────────────────
# Statistics
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 62)
print(f"  {'HOP COUNT RESULTS — ALL RUNS':^58}")
print("=" * 62)
print(f"  {'Run':>16} | {'Rcvd':>5} | {'Drop':>5} | {'Sum':>5} | {'Avg':>6} | {'Min':>4} | {'Max':>4}")
print(f"  {'-'*56}")

all_hops = []
for lbl in labels:
    d = results[lbl]
    h = d['hops']
    dr = d['dropped']
    all_hops.extend(h)
    s   = sum(h) if h else 0
    avg = s/len(h) if h else 0
    mn  = min(h) if h else 0
    mx  = max(h) if h else 0
    print(f"  {lbl:>16} | {len(h):>5} | {dr:>5} | {s:>5} | {avg:>6.2f} | {mn:>4} | {mx:>4}")

print(f"  {'-'*56}")
total_recv  = len(all_hops)
total_drop  = sum(results[l]['dropped'] for l in labels)
overall_avg = sum(all_hops)/total_recv if all_hops else 0
print(f"  {'OVERALL':>16} | {total_recv:>5} | {total_drop:>5} | {sum(all_hops):>5} | {overall_avg:>6.2f} |")
print("=" * 62)

# Average formula
print(f"\n  Formula:  Average = Sum of all hopCounts / Total packets received")
print(f"                    = {sum(all_hops)} / {total_recv} = {overall_avg:.4f}")
print(f"\n  Overall Average Hop Count = {overall_avg:.2f}")
print(f"  Total Dropped Packets     = {total_drop}\n")

# ─────────────────────────────────────────────────────────────────────────────
# 3-Panel Chart
# ─────────────────────────────────────────────────────────────────────────────

COLORS = ['#4C72B0','#DD8452','#55A868','#C44E52','#8172B3','#937860']

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("Hop Counting in Random Mesh Network — Analysis",
             fontsize=15, fontweight='bold')

avgs  = [sum(results[l]['hops'])/len(results[l]['hops'])
         if results[l]['hops'] else 0 for l in labels]
recvd = [len(results[l]['hops'])   for l in labels]
drops = [results[l]['dropped']     for l in labels]

# Panel 1: Average hop count per run
ax1 = axes[0]
bars = ax1.bar(labels, avgs,
               color=COLORS[:len(labels)], edgecolor='black', linewidth=0.8)
ax1.axhline(overall_avg, color='red', linestyle='--', linewidth=1.8,
            label=f'Overall avg = {overall_avg:.2f}')
ax1.set_title("Average Hop Count per Run", fontweight='bold')
ax1.set_xlabel("Run (Seed)")
ax1.set_ylabel("Average Hop Count")
ax1.set_ylim(0, max(avgs)*1.3 if avgs else 5)
ax1.legend(fontsize=9)
ax1.tick_params(axis='x', rotation=30)
for bar, val in zip(bars, avgs):
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.15,
             f"{val:.1f}", ha='center', va='bottom', fontsize=9, fontweight='bold')

# Panel 2: Hop count distribution histogram
ax2 = axes[1]
if all_hops:
    ax2.hist(all_hops, bins=range(1, max(all_hops)+2),
             color='steelblue', edgecolor='black', linewidth=0.8, align='left')
    ax2.axvline(overall_avg, color='red', linestyle='--', linewidth=1.8,
                label=f'Mean = {overall_avg:.2f}')
    ax2.legend(fontsize=9)
ax2.set_title("Distribution of Hop Counts (All Runs)", fontweight='bold')
ax2.set_xlabel("Hop Count")
ax2.set_ylabel("Frequency")

# Panel 3: Received vs Dropped
ax3 = axes[2]
x = np.arange(len(labels))
w = 0.35
b1 = ax3.bar(x-w/2, recvd, w, label='Received',
             color='#55A868', edgecolor='black', linewidth=0.8)
b2 = ax3.bar(x+w/2, drops, w, label='Dropped',
             color='#C44E52', edgecolor='black', linewidth=0.8)
ax3.set_title("Received vs Dropped Packets", fontweight='bold')
ax3.set_xlabel("Run (Seed)")
ax3.set_ylabel("Packet Count")
ax3.set_xticks(x)
ax3.set_xticklabels(labels, rotation=30)
ax3.legend()
for bar in list(b1)+list(b2):
    h = bar.get_height()
    if h > 0:
        ax3.text(bar.get_x()+bar.get_width()/2, h+0.3,
                 str(int(h)), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig("hop_count_analysis.png", dpi=150, bbox_inches='tight')
print("[INFO] Chart saved → hop_count_analysis.png")
