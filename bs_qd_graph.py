import json, re 
import matplotlib.pyplot as plt
import sys

fio_result_filename = sys.argv[1]
print("loading results from %s."%(fio_result_filename))

# Load fio JSON results 
with open(fio_result_filename) as f: 
    data = json.load(f) 

rows = [] 
for j in data["jobs"]: 
    name = j["jobname"] 
    m = re.match(r"bs(\d+)([km])_qd(\d+)", name) 
    if not m: 
        continue 
    size, unit, qd = int(m.group(1)), m.group(2).lower(), int(m.group(3)) 
    # Convert to KB for numeric sorting 
    bs_kb = size if unit == "k" else size * 1024 
    throughput = j["read"]["bw"] / 1024 # KB/s -> MB/s 
    rows.append((bs_kb, qd, throughput)) 

# Group by iodepth 
qd_groups = {} 
for bs_kb, qd, mbps in rows: 
    qd_groups.setdefault(qd, []).append((bs_kb, mbps)) 

# Sort each group by block size 
for qd in qd_groups: 
    qd_groups[qd].sort() 

# Plot 
plt.figure(figsize=(10, 6)) 
for qd, points in sorted(qd_groups.items()): 
    x = [p[0] for p in points] # block sizes in KB 
    y = [p[1] for p in points] # throughput MB/s 
    labels = [f"{kb}K" if kb < 1024 else f"{kb//1024}M" for kb in x] 
    plt.plot(x, y, marker='o', label=f"QD={qd}") 

plt.xscale("log") 
plt.xticks(x, labels, rotation=45) 
plt.xlabel("Block Size") 
plt.ylabel("Throughput (MB/s)") 
plt.title("fio: Throughput vs Block Size (per iodepth)") 
plt.grid(True, which="both", ls="--") 
plt.legend(title="Queue Depth") 
plt.tight_layout() 
plt.show() 