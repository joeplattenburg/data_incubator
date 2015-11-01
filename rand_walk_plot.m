% Plot an animation of a random walk

% Starting point
loc = 0;
% How many steps
num_steps=1000;

figure; hold on;
axis(sqrt(num_steps)*[-1 1 -1 1])
plot(0,0,'r*')

for n = 1:num_steps
    old_loc = loc;
    % Pick a random direction (N, E, S, or W)
    loc = loc + pick_direction();
    hold on
    axis(sqrt(num_steps)*[-1 1 -1 1])
    plot(real([loc old_loc]),imag([loc old_loc]),'o-')
    pause(.02)
end

range_walk = abs(loc);
