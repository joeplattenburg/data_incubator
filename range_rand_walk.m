function [range_walk] = range_rand_walk(num_steps)
% Returns the range (i.e. modulus in the complex plane) of a given random
% walk

% Start at origin
loc = 0;

for n = 1:num_steps
    loc = loc + pick_direction();
end

range_walk = abs(loc);

end
