# Reputation Is Farmable: sleeper-attack simulator for bridging rankers
All code written during the AI x Epistemics sprint (no pre-existing code).
Run: `python run.py && python run_h.py && python analyse.py` (about 10 min, 1 CPU, numpy + matplotlib).
- bridge.py: synthetic population, ALS fits (baseline MF, QS-MF, rho<=1, zero-prior), attack builder
- run.py: main experiment (3 attackers x 4 rules x 5 K x 6 seeds); run_h.py: history-length sweep
- analyse.py: tables and figures; results*.json: raw outputs reported in the paper
Idea of QS-MF is from Goyal, Arora & Goel (2026), reimplemented independently. Simulation only; not for use against live platforms.
