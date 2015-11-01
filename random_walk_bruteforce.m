% Joe Plattenburg
% This code simulates many random walks to see if they converge to an
% approximate solution (i.e. brute force) as a sanity check

clear; clc; close all

% How many steps
N_steps = 10;
% What distance to check
dist = 3;
% How many times to repeat
N_repeats=50;

% On each repeat, simulate more random walks to see if they are converging
repeats = logspace(2,5,N_repeats);
for kk = 1:length(repeats)
    disp(kk)
    N_times = ceil(repeats(kk));
    % Compute the range of a random walk (as the crow flies)
    range_walk = zeros(N_times,1);
    for n=1:N_times
        range_walk(n) = range_rand_walk(N_steps);
    end
    % What percentage of the walks go outside distance
    p(kk) = sum(range_walk >= dist)/N_times;
end

figure;
semilogx(repeats,p)
xlabel('Number of iterations')
ylabel(['Probability of traveling ' num2str(dist) 'blocks'])