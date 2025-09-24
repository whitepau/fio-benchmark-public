# USB 3.1 Gen 1 Benchmarking of Agilex 5 HPS

This repository contains resources I used for benchmarking the USB 3.1 interface on Agilex 5 HPS.

## Methods

Follow the instructions below to reproduce the results of this benchmark for yourself.

### Pre-requisites

This benchmark was conducted using [PNY DUO LINK™ V3 USB 3.2 Gen 2 Type-C® Dual Flash Drive](https://www.pny.com/PNY-DUO-Link-V3-USB-3-2-Gen-2-Type-C-OTG?sku=P-FDI256DULNK3TYC-GE) USB flash drive. This USB flash drive was chosen because it supports up to USB 3.2 Gen 2 10 Gbps reads (1000 MB/s) and writes (800 MB/s). These were verified using [CrystalDiskMark](https://sourceforge.net/projects/crystaldiskmark/) on my personal machine.

For FPGA hardware, the following development kits were used:

* [Agilex™ 5 FPGA E-Series 065B Premium Development Kit](https://www.intel.com/content/www/us/en/products/details/fpga/development-kits/agilex/a5e065b-premium.html)
![alt text](Readme_assets/agilex5_prem.png)

* [Kria KV260 Vision AI Starter Kit](https://www.amd.com/en/products/system-on-modules/kria/k26/kv260-vision-starter-kit.html)
![alt text](Readme_assets/kv260_board.png)

### Instructions

You can run the benchmarks and generate graphics as follows:

1. Ensure that `fio` is available on your devkit, either by installing it from a package manager or including it in your root file system as part of your build process.
2. Copy this repository to your devkit.
3. Run `fio`:
   ```
   fio bs_qd_sweep.fio --output=bs_qd_results.json --output-format=json 
   ```
4. Run the `bs_qd_graph.py` script:
   ```
   python3 bs_qd_graph.py bs_qd_results.json
   ```
   If you don't have a desktop GUI available on your devkit, you can copy the `bs_qd_results.json` over to a workstation to generate the graphics.

## Results

The following graphs result from running the code on various test platforms.

![alt text](Readme_assets/workstation.png)

Workstation 

![alt text](Readme_assets/agilex5.png)

Agilex™ 5 - 20s runtime

![alt text](Readme_assets/agilex5_40s.png)

Agilex™ 5 - 40s runtime
 
![alt text](Readme_assets/kv260.png)

KV260 