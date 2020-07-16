# TITL MARS OPT Python code
by Xinglong Ju (*xinglong.ju@mavs.uta.edu*); Jay M. Rosenberger (*jrosenbe@uta.edu*); Victoria C. P. Chen (*vchen@uta.edu*); Feng Liu (*fliu0@mgh.harvard.edu*).

Xinglong Ju, Jay M. Rosenberger, Victoria C. P. Chen, and Feng Liu. "TITL MARS OPT Python code". 2020.
[![DOI](https://zenodo.org/badge/275648852.svg)](https://zenodo.org/badge/latestdoi/275648852)

Xinglong Ju, Jay M. Rosenberger, Victoria CP Chen, and Feng Liu. "Global optimization using mixed integer quadratic programming on non-convex two-way interaction truncated linear multivariate adaptive regression splines." arXiv preprint arXiv:2006.15707 (2020). [![DOI](/arXiv2006.15707.svg)](https://arxiv.org/abs/2006.15707)<br/>

Xinglong Ju, Jay M. Rosenberger, and Victoria C. P. Chen<br/>
Department of Industrial, Manufacturing, & Systems Engineering
The University of Texas at Arlington, Arlington, TX 76019, USA

Feng Liu<br/>
Department of Anesthesia, Critical Care and Pain Medicine
Massachusetts General Hospital, Harvard Medical School, Boston, MA 02114, USA
The Picower The Picower Institute for Learning and Memory
Massachusetts Institute of Technology, Cambridge, MA 02139, USA

TITL MARS OPT is short for two-way interaction truncated linear multivariate adaptive regression splines optimization.

This python code is accompanied by "Global optimization using mixed integer quadratic programming on non-convex two-way interaction truncated linear multivariate adaptive regression splines".

## Reference
[1] Xinglong Ju, and Victoria C. P. Chen. "A MARS Python version using truncated linear function." 2019. [![DOI](https://zenodo.org/badge/226974692.svg)](https://zenodo.org/badge/latestdoi/226974692)<br/>

## TITL MARS OPT Python code guide
### Import necessary libraries
```python
import numpy as np
import pandas as pd
import MARS
from datetime import datetime
from MARS_OPT import *
import time
```

### This part is train the TITL MARS model.
```python
#parameters to train the MARS model
# number of independent variables, user could change this parameter
n_variables = 2
# size of training dataset, user could change this parameter
n_points = 1000
# specify the number of candidate knots to train the MARS model, user could change this parameter
n_candidate_knots = [40, 40]
# number of maximum basis functions, user could change this parameter
n_max_basis_functions = 100
# maximum degree of interaction terms
# Must be 2 for TITL MARS
n_max_interactions = 2
# a stopping criteria, user could change this parameter
difference = 1.0e-3

# load the training X
x_original = pd.read_csv("x.dat", header=None, nrows=n_points, delim_whitespace=True)
x_original = x_original.values

# load the training Y
y_original = pd.read_csv("y.dat", header=None, nrows=n_points, delim_whitespace=True)
y_original = y_original.values

# create the MARS object
mars = MARS.MARS(n_variables=n_variables, n_points=n_points, x=x_original, y=y_original,
                 n_candidate_knots=n_candidate_knots, n_max_basis_functions=n_max_basis_functions,
                 n_max_interactions=n_max_interactions, difference=difference)
# train the TITL MARS model
mars.MARS_regress()
# save the MARS model to a file
mars.save_mars_model_to_file("TITL_MARS.mars")
```
<p align="center"> 
    <img width="400" src="/TITL_MARS_model.png" alt="TITL MARS model illustration"/><br/>
    TITL MARS model illustration.
</p>

### TITL MARS Optimization
```python
# create the a MARS object and load the trained MARS model
mars = MARS.MARS()
mars.load_mars_model_from_file("TITL_MARS.mars")

# create a TITL MARS OPT object
mars_opt = MARS_OPT()

# find the maximum of the TITL MARS model
max1 = mars_opt.max_optimize(mars)

print(max1)
# [x1, x2, y]
# [-0.05274081296657257, 1.998290807400001, 10.084549773597132]
# find the minimum of the TITL MARS model
min1 = mars_opt.min_optimize(mars)
# [x1, x2, y]
# [0.15040898573205055, -1.9982908070000007, -8.099636884123703]
print(min1)
```
<p align="center"> 
    <img width="400" src="/TITL_MARS_OPT_Result.png" alt="TITL MARS optimization result illustration"/><br/>
    TITL MARS optimization result illustration.
</p>
