% commented code was used to train the model (with some extraneous bits removed
% like searching for a good model)
%
% uncommneted code up to "example usage" specifies the trained GP model
%
% "example usage" shows a quick example for how to make/evaluate predictions
%
% email Roman Garnett (garnett@wustl.edu) with any questions

% load data
data_directory = 'data/';

data = csvread(sprintf('%s/estimated_heights.csv', data_directory), 1, 1);

num_series = size(data, 1);
num_days   = size(data, 2);

% apply a logit transformation to height data clamping predictions between [0,
% 400] cm

max_height = 400;

logit = @(x) log(x ./ (max_height - x));
inverse_logit = @(x) (exp(x) ./ (1 + exp(x))) * max_height;

% extract time series for use with GPML interface

xs = cell(num_series, 1); % days after planting with measurements for each subplot
ys = cell(num_series, 1); % logit-transformed estimated heights for each subplot

for i = 1:num_series
  xs{i} = find(~isnan(data(i, :)))';
  ys{i} = logit(data(i, xs{i}))';
end

% create predictive model; commented code will retrain model

% noise model
inference_method = @infExact;
% theta.lik = log(0.1);

% mean function
mean_function = {@meanSum, {@meanConst, {@meanPoly, 2}}};
% theta.mean = [-5.2303; 0.11096; -0.0004531]; % from polynomial fit

% covariance function
covariance_function = {@covSum, {@covSEiso, @covSEiso}};
% theta.cov = [log(21); log(0.2); log(7); log(0.2)];

% learn hyperparameters via gradient descent

% p.length = 100;
% p.method = 'BFGS';
% theta = minimize_v2(theta, @gp_likelihood_independent, p, inference_method, ...
%                     mean_function, covariance_function, [], xs, ys);

% learned theta
theta.mean = [-5.4026; 0.11652; -0.00049594];
theta.cov  = [2.4556; -0.71296; 0.92936; -2.3482];
theta.lik  = -2.1274;

% example usage: predict terminal height for each time series from data before
% day `cutoff`

cutoff = 60; % use data up to day 30

maes              = zeros(num_series, 1);
target_heights    = zeros(num_series, 1);
predicted_heights = zeros(num_series, 1);
for i = 1:num_series

  % find last-measured height
  target_heights(i) = inverse_logit(ys{i}(end));

  % data to use for prediction
  ind = (xs{i} <= cutoff);

  [~, ~, predictive_mean, predictive_variance] = ...
      gp(theta, [], mean_function, covariance_function, ...
         [], xs{i}(ind), ys{i}(ind), xs{i}(end));

  predicted_heights(i) = inverse_logit(predictive_mean);

  % compute MAE, for example
  maes(i) = abs(predicted_heights(i) - target_heights(i)); % 20.89 cm for (i = 951)

end

fprintf('mean mean absolute error: %0.2f cm\n', mean(maes));
fprintf('rank correlation: %0.2f \n', ...
        corr(target_heights, predicted_heights, 'type', 'spearman'));

% load kinship
genotypes = ...
    csvread(sprintf('%s/field_genotypes.csv', data_directory), 1, 3);

normalized_kinship = ...
    csvread(sprintf('%s/normalized_kinship.csv', data_directory), 1, 1);

centered_kinship = ...
    csvread(sprintf('%s/centered_kinship.csv', data_directory), 1, 1);

% extract subset of data with kinship information
subset = (~isnan(genotypes));
with_kinship = data(subset, :);

field_centered_kinship = ...
    centered_kinship(genotypes(subset), genotypes(subset));

field_normalized_kinship = ...
    normalized_kinship(genotypes(subset), genotypes(subset));