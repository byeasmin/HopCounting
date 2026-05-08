#!/usr/bin/env python3
"""
parse_console.py
================
Collects hopCount values from your OMNeT++ console output
and displays them for insertion into MANUAL_RESULTS in analyze_results.py.

Usage:
    1. After each OMNeT++ run, copy the console output
    2. Paste it into the console_outputs dictionary below according to the seed
    3. Run: python parse_console.py
"""

import re

# ── Paste the console output of each run here ──────────────────
# For each run, the "Packets received" and "Average hop count" lines are required


console_outputs = {
    42:   """
Packets received : 48
Average hop count: 8.45833
Min hop count    : 4
Max hop count    : 18
Std deviation    : 3.77539
""",
    # Paste the remaining runs here after completing them:
    100:  """
Packets received : 47
Average hop count: 8.97872
Min hop count    : 4
Max hop count    : 19
Std deviation    : 4.33634
""",
    255:  """
Packets received : 44
Average hop count: 7.70455
Min hop count    : 4
Max hop count    : 19
Std deviation    : 3.77618
""",
    777:  """
Packets received : 46
Average hop count: 7.86957
Min hop count    : 4
Max hop count    : 18
Std deviation    : 3.30393
""",
    1234: """
Packets received : 47
Average hop count: 8.42553
Min hop count    : 4
Max hop count    : 19
Std deviation    : 4.0311
""",
    9999: """
Packets received : 46
Average hop count: 8.80435
Min hop count    : 4
Max hop count    : 19
Std deviation    : 3.68552
""",
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
