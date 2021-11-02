include "globals.mzn"; 

int: n; % num rows and columns

int: L = 1; % Lamp
int: P = 2; % Plant

% 1 for a lamp, 2 for a plant and 0 for nothing 
array[1..n,1..n] of 0..2: garden;

% number of plants by row/col
array[1..n] of int: rows;
array[1..n] of int: cols;

% decision variables
array[1..n,1..n] of var 0..P: x;

% nombre total de plantes par colonnes et par rangees
constraint forall(k in 1..n)(sum(i in 1..n)(x[k,i]==P) == rows[k]);
constraint forall(k in 1..n)(sum(i in 1..n)(x[i,k]==P) == cols[k]);

%lampes doivent etre fix
constraint forall(i in 1..n, j in 1..n)(if garden[i,j]=L then x[i,j]=L endif);

% plantes ne doivent pas se toucher (etre voisin)(verti, horizon ou diag)
constraint forall(i in 1..n, j in 1..n)(x[i,j]=P ->
                                          (if i+1<=n then x[i+1,j]!=P endif ) \/
                                          (if j+1<=n then x[i,j+1]!=P endif ) \/
                                          (if i+1<=n /\ j+1<=n then x[i+1,j+1]!=P endif ) \/
                                          (if i-1>0 then x[i-1,j]!=P endif ) \/
                                          (if j-1>0 then x[i,j-1]!=P endif ) \/
                                          (if i-1>0 /\ j-1>0 then x[i-1,j-1]!=P endif ));
                                          
     
% plante doit avoir une lampe solaire direct a cote (verti ou horizon)
% constraint x[1,1]=P;
constraint forall(i in 1..n, j in 1..n)(x[i,j]=P ->
                                          (if i+1<=n then x[i+1,j]=L else false endif) \/
                                          (if j+1<=n then x[i,j+1]=L else false endif) \/
                                          (if i-1>0 then x[i-1,j]=L else false endif) \/
                                          (if j-1>0 then x[i,j-1]=L else false endif));


% % chaque lampe doit avoir au moins 1 plante direct a cote (verti ou horizon)
constraint forall(i in 1..n, j in 1..n)(x[i,j]=L ->
                                          (if i+1<=n then x[i+1,j]=P else false endif) \/
                                          (if j+1<=n then x[i,j+1]=P else false endif) \/
                                          (if i-1>0 then x[i-1,j]=P else false endif) \/
                                          (if j-1>0 then x[i,j-1]=P else false endif));

solve satisfy;

output 
[
 if j = 1 then "\n" ++ show(rows[i]) ++ " " else " " endif ++
   if fix(x[i,j]) = L then "L" elseif fix(x[i,j]) = P then "P" else "_" endif
| i,j in 1..n
] ++ ["\n  "] ++ [show(cols[i]) ++ " " | i in 1..n];
