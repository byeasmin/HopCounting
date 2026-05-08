# Hop Counting in Random Mesh Network

## Project Files

Place the following files inside the project folder:

```text
MyMessage.msg
Sender.h
Sender.cc
Router.h
Router.cc
Receiver.h
Receiver.cc
HopCountNet.ned
omnetpp.ini
```

---

# Step 1: Import the Project in OMNeT++

1. Open the OMNeT++ IDE
2. Go to:

```text
File → New → OMNeT++ Project
```

3. Create a project named:

```text
HopCountSim
```

4. Copy all project files into the project folder

---

# Step 2: Build the Project

Build the project using:

```text
Project → Build All
```

or press:

```text
Ctrl + B
```

If no errors appear, the build is successful.

---

# Step 3: Run the Simulation

1. Right-click on `omnetpp.ini`
2. Select:

```text
Run As → OMNeT++ Simulation
```

3. Run each configuration separately.

| Run Configuration | Seed |
|-------------------|------|
| Run1 | 42 |
| Run2 | 100 |
| Run3 | 255 |
| Run4 | 777 |
| Run5 | 1234 |
| Run6 | 9999 |

---

# Step 4: Record hopCount Values

After each run, check the Receiver log output:

```text
[Receiver] Packet arrived! hopCount=7, remaining TTL=13
```

Record the `hopCount` value from each run.

Example:

| Run | Seed | hopCount |
|-----|------|-----------|
| 1 | 42 | 7 |
| 2 | 100 | 11 |
| 3 | 255 | 9 |
| 4 | 777 | 13 |
| 5 | 1234 | 8 |
| 6 | 9999 | 10 |

---

# Step 5: Calculate Average Hop Count

Formula:

```text
Average Hop Count =
(Run1 + Run2 + Run3 + Run4 + Run5 + Run6) / 6
```

Example Calculation:

```text
= (7 + 11 + 9 + 13 + 8 + 10) / 6
= 58 / 6
= 9.67 hops
```

---

# Step 6: Calculate Dropped Packets

If a packet exceeds the TTL limit, it is dropped by the router.

Router logs will show:

```text
[r3] Total packets dropped: 2
```

Add the dropped packet counts from all routers to get the total dropped packets.

---

# Lab Report Format

```text
Total Runs        = 6
hopCount values   = 7, 11, 9, 13, 8, 10
Sum               = 7 + 11 + 9 + 13 + 8 + 10 = 58
Average           = 58 ÷ 6 = 9.67 hops
```

Replace the example values with your actual simulation results.

---

# Automating the Analysis Using Python

Instead of calculating everything manually, a Python script can automatically analyze the simulation results.

---

# Step 1: Install Python

Check Python installation:

```bash
python --version
```

If Python is not installed, download it from:

- https://www.python.org

---

# Step 2: Run the Analysis Script

Go to the project folder:

```bash
cd HopCountSim
```

Run the script:

```bash
python3 analyze_results.py
```

---

# Step 3: Example Output

```text
============================================================
       Hop Counting in Random Mesh Network — Results
============================================================
    Seed | Received | Dropped | Avg Hops | Min | Max | StdDev
------------------------------------------------------------
      42 |       48 |       2 |      9.60 |   5 |  20 |   4.56
     100 |       46 |       4 |      9.98 |   5 |  19 |   3.56
     255 |       41 |       9 |      9.73 |   5 |  20 |   4.27
     777 |       44 |       6 |     10.34 |   5 |  19 |   4.29
    1234 |       45 |       5 |      9.84 |   5 |  20 |   4.15
    9999 |       49 |       1 |      9.80 |   5 |  20 |   4.06
------------------------------------------------------------
 OVERALL |      273 |      27 |      9.88 |   5 |  20 |   4.13
============================================================

Overall Average Hop Count : 9.88
Total Dropped Packets     : 27
```

---

# Average Calculation Used in Python

The script calculates the average using:

```python
avg = statistics.mean(hops)
```

Equivalent formula:

```text
Overall Average =
(sum of all hopCounts) / total packets received
```

Example:

```text
(7 + 9 + 11 + ...) / 273 = 9.88
```

---

# Generated Chart

The script automatically generates:

```text
hop_count_analysis.png
```
