import csv
import numpy as np
import GPy

# needed for retraining
# from quadratic import *

data = []
with open('data/estimated_heights.csv', 'r') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    next(datareader)  # skip header
    for row in datareader:
        del row[0]  # skip id
        data.append(row)

num_series = len(data)
num_days   = len(data[0])

# apply a logit transformation to height data clamping predictions between [0,
# 400] cm

max_height = 400;

logit = lambda x: np.log(x / (max_height - x) )  # element-wise if vector
inverse_logit = lambda x: (np.exp(x) / (1 + np.exp(x))) * max_height

# extract time series for use with GPy interface

xs = [0] * num_series  # days after planting with measurements for each subplot
ys = [0] * num_series  # logit-transformed estimated heights for each subplot

for i in range(num_series):
    idx = [j+1 for j in range(num_days) if data[i][j].lower() != 'nan' ]
    xs[i] = np.array(idx, ndmin=2).T
    ys[i] = np.array([logit(float(data[i][j-1])) for j in idx], ndmin=2).T

# create predictive model; commented code will retrain model

# noise model
inference_method = GPy.inference.latent_function_inference.ExactGaussianInference()

# mean function: 2nd order polynomial
# const_part     = GPy.mappings.Constant(1, 1)
# linear_part    = GPy.mappings.Linear(1, 1)
# affine_part    = GPy.mappings.Additive(const_part, linear_part)
# class Quadratic(GPy.core.Mapping):
#     # only applicable to one-dimensional data
#     def __init__(self, input_dim, output_dim, name='quadmap'):
#         super(Quadratic, self).__init__(input_dim=input_dim, output_dim=output_dim, name=name)
#         self.A = GPy.core.parameterization.Param('A', \
#                     np.random.randn(self.input_dim, self.input_dim))
#         self.link_parameter(self.A)
#
#     def f(self, X):
#         return self.A * X * X
#
#     def update_gradients(self, dL_dF, X):
#         self.A.gradient = np.dot((X*X).T, dL_dF)
#
#     def gradients_X(self, dL_dF, X):
#         return dL_dF * 2*self.A*X
# quadratic_part = Quadratic(1, 1)
# mean_function  = GPy.mappings.Additive(affine_part, quadratic_part)

mean_function = GPy.core.Mapping(1,1)
mean_function.f = lambda x: -5.4026 + 0.11652 * x - 0.00049594 * x**2
mean_function.update_gradients = lambda a, b: None

# specify kernel functions
kern1 = GPy.kern.RBF(input_dim=1, variance=np.exp(-2.3482), \
                      lengthscale=np.exp(0.92936))
kern2 = GPy.kern.RBF(input_dim=1, variance=np.exp(-0.71296), \
                      lengthscale=np.exp(2.4556))
kernel  = kern1 + kern2
likelihood     = GPy.likelihoods.Gaussian(variance=np.exp(-2.1274))

# currently does not support training on multiple datasets
# m = GPy.models.GPRegression(xs[0],ys[0],kernel=kernel, mean_function=mean_function)
# m.optimize(messages=True, max_f_eval = 1000)

cutoff = 30  # use data up to data
maes   = [0] * num_series

for i in range(num_series):

    ind = xs[i] <= cutoff
    target_height = inverse_logit(ys[i][-1])

    x = np.array(xs[i][ind], ndmin=2).T
    y = np.array(ys[i][ind], ndmin=2).T
    model = GPy.core.GP(x, y, kernel=kernel, \
                    likelihood=likelihood, \
                    mean_function=mean_function, \
                    inference_method=inference_method, normalizer=False)

    last_measured = np.array(xs[i][-1], ndmin=2).T
    predictive_mean, predictive_variance = model.predict(last_measured)

    predicted_height = inverse_logit(predictive_mean);

    # compute MAE, for example
    maes[i] = abs(predicted_height - target_height)
