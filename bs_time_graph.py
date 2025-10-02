import json, re 
import matplotlib.pyplot as plt
import sys

def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


def parse_bw_data(read_write_mode: str):
    rows = [] 
    if read_write_mode not in ["read", "write"]:
        raise ValueError("read_write_mode must be 'read' or 'write'")

    for j in data["jobs"]: 
        name = j["jobname"] 
        size_str = j["job options"]["bs"]
        m = re.match(r"(\d+)([kM])", size_str, re.IGNORECASE) 
        if not m: 
            continue 
        size, unit = int(m.group(1)), m.group(2).lower()
        # runtime = int(int(j["job_runtime"]) / int(1000))
        runtime_str = j["job options"]["runtime"]
        m = re.match(r"(\d+)([s])", runtime_str, re.IGNORECASE) 
        if not m: 
            continue 
        runtime = int(m.group(1))

        # Convert to KB for numeric sorting 
        bs_kb = size if unit == "k" else size * 1024 
        throughput = j[read_write_mode]["bw"] / 1024 # KiB/s -> MiB/s
        throughput_mean = j[read_write_mode]["bw_mean"] / 1024 # KiB/s -> MiB/s
        throughput_min = j[read_write_mode]["bw_min"] / 1024
        throughput_max = j[read_write_mode]["bw_max"] / 1024
        throughput_dev = j[read_write_mode]["bw_dev"] / 1024
        iops = j[read_write_mode]["iops_mean"]
        lower_error = throughput_mean - throughput_min
        upper_error = throughput_max - throughput_mean
        # lower_error = throughput_dev
        # upper_error = throughput_dev

        # Only include successful runs (nonzero runtime)
        if (runtime > 0):
            rows.append((bs_kb, runtime, throughput, throughput_mean, lower_error, upper_error, iops))

    return rows


read_write_mode = sys.argv[1]
fio_result_filename = sys.argv[2]

print("loading %s results from %s."%(read_write_mode, fio_result_filename))

# Load fio JSON results 
with open(fio_result_filename) as f: 
    data = json.load(f)

rows = parse_bw_data(read_write_mode)

# Group by iodepth 
runtime_groups = {} 
for bs_kb, rt, mbps, mbps_med, mbps_min, mbps_max, iops in rows: 
    runtime_groups.setdefault(rt, []).append((bs_kb, mbps, mbps_med, mbps_min, mbps_max, iops)) 

# Sort each group by block size 
for rt in runtime_groups: 
    runtime_groups[rt].sort() 

# Plot bandwidth variation
plt.figure(figsize=(10, 6))
width = len(runtime_groups)
colors = []
# for rt, points in sorted(runtime_groups.items()): 
#     x = [p[0] for p in points] # block sizes in KiB 
#     y_med = [p[2] for p in points]
#     lower_error = [p[3] for p in points]
#     upper_error = [p[4] for p in points]
#     yerr = [lower_error, upper_error]

#     labels = [f"{kb}K" if kb < 1024 else f"{kb//1024}M" for kb in x] 
#     container = plt.errorbar(x, y_med, yerr=yerr, elinewidth=width * 4, marker='X', linestyle="",  capsize=5.0 + width * 4, label=f"Runtime={rt}") 
#     clr = container[0]._color
#     colors.append(clr)    
#     width = width - 1

for rt, points in sorted(runtime_groups.items()): 
    x = [p[0] for p in points] # block sizes in KiB 
    y = [p[1] for p in points] # throughput MiB/s

    labels = [f"{kb}K" if kb < 1024 else f"{kb//1024}M" for kb in x] 
    # clr = colors.pop(0)
    # container = plt.plot(x, y, marker='o', color=clr, label=f"Runtime={rt}")
    container = plt.plot(x, y, marker='o', label=f"Runtime={rt}")

plt.xscale("log") 
plt.xticks(x, labels, rotation=45) 
plt.xlabel("Block Size") 
plt.ylabel("Throughput (MB/s)") 
plt.title("fio: Throughput vs Block Size (per runtime)") 
plt.grid(True, which="both", ls="--") 
plt.legend(title="Runtime") 
plt.tight_layout() 
plt.show() 

# Plot IOPS
plt.figure(figsize=(10, 6)) 
for rt, points in sorted(runtime_groups.items()): 
    x = [p[0] for p in points] # block sizes in KB 
    y = [p[4] for p in points] # IO/s
    labels = [f"{kb}K" if kb < 1024 else f"{kb//1024}M" for kb in x] 
    plt.plot(x, y, marker='o', label=f"Runtime={rt}") 

plt.xscale("log") 
plt.xticks(x, labels, rotation=45) 
plt.xlabel("Block Size") 
plt.yscale("log")
plt.ylabel("IO commands per second") 
plt.title("fio: IOPS vs Block Size (per Runtime)") 
plt.grid(True, which="both", ls="--") 
plt.legend(title="Runtime") 
plt.tight_layout() 
plt.show() 