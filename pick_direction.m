function which_dir = pick_direction()
% Pick one of 4 orthogonal directions in the complex plane with equal
% probability

num = randi(4,1);

if num==1
    which_dir = 1;
elseif num==2
    which_dir = -1;
elseif num==3
    which_dir = j;
elseif num==4
    which_dir = -j;
end

end