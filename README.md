## ECE6327_SGS_Python_Sample_Codes
This repo provides about 40 Python/Pyomo programs, including codes for tutorial-level examples and codes for course-level DCOPF, SCUC, DSM, SUC, transmission switching, FACTS, energy storage, and microgrid energy management and sizing examples that are used for the class ECE6327 Smart Grid Systems at University of Houston for 2026 Spring.

Special thanks to Haoxiang Wan for translating the AMPL programs into Python programs that are enclosed in this repo. He is a PhD student who joined us in August 2025.

This repo is part of the open source materials for the following course taught by Dr. Xingpeng Li.
* ECE6327 Smart Grid Systems (SGS) at University of Houston (2026 Spring version)

The course materials such as lecture slides and assignments can be found with the following link:
* https://rpglab.github.io/resources/ECE6327-SGS/


This repository is a **Python port** of the course materials for ECE6327 *Smart Grid Systems* (University of Houston, 2026 Spring). Every AMPL program from the original distribution has been converted into a Pyomo Jupyter notebook solved with Gurobi.

The port was carried out by **Haoxiang Wan**, PhD student of Dr. Xingpeng Li.

#### Shared Contents:
1. The repo contains the converted Jupyter notebooks (`*.ipynb`), organized to match the lecture slide numbering (`05_DCOPF`, `06_SCUC`, `10_DSM2`, `15_RE_Intgrtn1_Uncertainty`, ...).
2. The original AMPL data files (`*.txt`) are shipped verbatim alongside the notebooks that read them &mdash; the Pyomo notebooks load them through a small parser at `ampl_data.py` (`parse_ampl_data`, `parse_text`), preserving the original AMPL data-file workflow.
3. All notebooks are **pre-executed**; solver logs and final numerical results are visible directly.


#### Software Requirements:
* Python 3.10+
* Pyomo, Gurobi (`pip install pyomo gurobipy jupyter nbconvert`)

The pip-installed `gurobipy` ships with a size-limited license that already covers every example in this repo; no separate Gurobi license is required.


## Conversion notes
* Same folder layout, same file naming as the original AMPL repo.
* Same external `.txt` data files; the Pyomo notebooks load them through `ampl_data.py`.
* Solver options mirror the original (`MIPGap=0`, `TimeLimit=90`).


## Contact:
Dr. Xingpeng Li

University of Houston

Email: xli83@central.uh.edu

Website: https://rpglab.github.io/

## Figshare:
The codes in this repo was initially included in the following package uploaded on Figshare. The link is as follows:
https://figshare.com/articles/online_resource/ECE6379_PSOM_zip/17161805

## Citation:
Li, Xingpeng: ECE6379_PSOM.zip. figshare. Online resource. https://doi.org/10.6084/m9.figshare.17161805

## License:
This work is licensed under the terms of the Creative Commons Attribution 4.0 (CC BY 4.0) license. 
https://creativecommons.org/licenses/by/4.0/

## Disclaimer:
The author doesn’t make any warranty for the accuracy, completeness, or usefulness of any information disclosed and the author assumes no liability or responsibility for any errors or omissions for the information (data/code/results etc) disclosed.
