[![Codacy Badge](https://api.codacy.com/project/badge/Grade/aa032a2503064abfbfdf2931050bc289)](https://app.codacy.com/app/mortele/OccamBayesian?utm_source=github.com&utm_medium=referral&utm_content=mortele/OccamBayesian&utm_campaign=Badge_Grade_Dashboard)
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

## OccamBayesian
Bayesian optimization applied to OCCAM hybrid particle-field simulations, built on top of [fmfn/BayesianOptimization](https://github.com/fmfn/BayesianOptimization).

### Dependencies
Install the BayesianOptimization package and the [file_read_backwards](https://file-read-backwards.readthedocs.io/en/latest/readme.html) package by
```
> pip3 install bayesian-optimization
> pip3 install file_read_backwards
```

### Usage
Set the `OCCAM_PATH` in `occam_bayesian.py` to wherever the OCCAM executable is located, and run
```
> python3 occam_bayesian.py
```
