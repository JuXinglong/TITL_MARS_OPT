import numpy as np
import pandas as pd
import MARS
from datetime import datetime
from MARS_OPT import *
import time

#######
# This part is train the TITL MARS model
#######
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


# mars = MARS.MARS()
# mars.load_mars_model_from_file("TITL_MARS.mars")
# mars.draw(-2.0, +2.0, -2.0, +2.0, 100)

#########
# TITL MARS OPT
#########
# create the a MARS object and load the trained MARS model
mars = MARS.MARS()
mars.load_mars_model_from_file("TITL_MARS.mars")

# create a TITL MARS OPT object
mars_opt = MARS_OPT()

# find the maximum of the TITL MARS model
max1 = mars_opt.max_optimize(mars)

print(max1)
# [-0.05274081296657257, 1.998290807400001, 10.084549773597132]
# find the minimum of the TITL MARS model
min1 = mars_opt.min_optimize(mars)
# [0.15040898573205055, -1.9982908070000007, -8.099636884123703]
print(min1)

# mars.draw_with_extremes_(-2.0, +2.0, -2.0, +2.0, 100, max1, min1)
# print("Hello")
