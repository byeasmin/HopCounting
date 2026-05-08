#!/usr/bin/env python3
"""
parse_console.py
================
তোমার OMNeT++ console output থেকে hopCount values সংগ্রহ করে
analyze_results.py এর MANUAL_RESULTS এ বসানোর জন্য দেখায়।

Usage:
    1. OMNeT++ এ প্রতিটা run শেষে Console এর output copy করো
    2. নিচের console_outputs dict এ seed অনুযায়ী paste করো
    3. python parse_console.py চালাও
"""

import re

# ── তোমার প্রতিটা run এর console output এখানে paste করো ──────────────────
# প্রতিটা run এর "Packets received" এবং "Average hop count" লাইন দরকার

console_outputs = {
    42:   """
Packets received : 48
Average hop count: 8.45833
Min hop count    : 4
Max hop count    : 18
Std deviation    : 3.77539
""",
    # বাকি run গুলো run করার পর এখানে paste করো:
    100:  "",
    255:  "",
    777:  "",
    1234: "",
    9999: "",
}

# ─────────────────────────────────────────────────────────────────────────────
# Parse and summarize
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 55)
print("  Parsed Results from Console Output")
print("=" * 55)

parsed = {}
for seed, txt in console_outputs.items():
    if not txt.strip():
        print(f"  Seed {seed:>4}: (no data yet)")
        continue
    rcvd = re.search(r'Packets received\s*:\s*(\d+)', txt)
    avg  = re.search(r'Average hop count\s*:\s*([\d.]+)', txt)
    mn   = re.search(r'Min hop count\s*:\s*(\d+)', txt)
    mx   = re.search(r'Max hop count\s*:\s*(\d+)', txt)
    drop_match = re.search(r'dropped.*?:\s*(\d+)', txt, re.IGNORECASE)

    if rcvd and avg:
        n    = int(rcvd.group(1))
        a    = float(avg.group(1))
        total_sum = round(n * a)
        parsed[seed] = {'n': n, 'avg': a, 'sum': total_sum,
                        'min': int(mn.group(1)) if mn else '?',
                        'max': int(mx.group(1)) if mx else '?'}
        print(f"  Seed {seed:>4}: received={n}  avg={a:.2f}  "
              f"sum≈{total_sum}  min={parsed[seed]['min']}  max={parsed[seed]['max']}")

# Overall average formula
if parsed:
    total_n   = sum(v['n']   for v in parsed.values())
    total_sum = sum(v['sum'] for v in parsed.values())
    overall   = total_sum / total_n if total_n else 0
    print("-" * 55)
    print(f"\n  Formula:")
    print(f"  Overall Average = Total Sum / Total Received")
    print(f"                  = {total_sum} / {total_n}")
    print(f"                  = {overall:.2f}")
    print(f"\n  Overall Average Hop Count = {overall:.2f}")
print("=" * 55)
