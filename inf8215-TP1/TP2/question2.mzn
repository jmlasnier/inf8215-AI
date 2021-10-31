include "globals.mzn"; 

int: n = 5;
% the given results
array[1..4] of int: res = [1,2,5,7];


% number of points for each player
array[1..n] of var 0..3*n: x;

% (i, j) is the result of player i against player j
array[1..n, 1..n] of var {0,1,3}: matches;


constraint  forall(k in 1..n)(matches[k,k]=0);

constraint matches[1,2]+matches[1,3]+matches[1,4]+matches[1,5] = res[1];
constraint matches[2,1]+matches[2,3]+matches[2,4]+matches[2,5] = res[2];
constraint matches[3,1]+matches[3,2]+matches[3,4]+matches[3,5] = res[3];
constraint matches[4,1]+matches[4,2]+matches[4,3]+matches[4,5] = res[4];

constraint forall(i in 1..n, j in 1..n where i<j) (matches[j,i] = if matches[i,j] = 3 then 0 elseif matches[i,j]=1 then 1 else 3 endif);

constraint forall(i in 1..4)(x[i]=res[i]);
constraint x[5] = sum(i in 1..4)(matches[5,i]);

solve satisfy;

output 
[
  "Scores\n"
]
++
[
  show(x)
]
++	
[
  "\nMatches\n"
]
++
[ show(matches[i,j]) ++ 
         if j == n then "\n" else " " endif |
         i in 1..n, j in 1..n
]
;