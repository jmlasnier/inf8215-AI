include "globals.mzn";

int: n_nurse; % Number of nurses
int: n_week; % Number of weeks in our horizon
int: n_day; % Number of days in our horizon (7 * n_week). Monday is the first day of the week
int: n_work_period; % Number of work period. It equals 4 (MATIN, SOIREE, NUIT, REPOS)

% Indexing the work periods
int: MATIN = 1;
int: SOIREE = 2;
int: NUIT = 3;
int: REPOS = 4;

int: dur_work_period; % Duration of the work periods (6h)

array[1..n_day,1..n_work_period] of int: demande_min; % Number of nurses required for each day and each work period (= 0 for REPOS)
array[1..n_nurse,1..n_day,1..n_work_period] of int: preference; % Work preference for each nurse

% Decision variables
array[1..n_nurse,1..n_day,1..n_work_period] of var 0..1: x; % work period [MATIN, SOIREE, NUIT, REPOS]
var int: sum_preference;

%Constraints


% %OK 4- 1 periode par jour par infirmière
constraint forall(i in 1..n_nurse, j in 1..n_day)(sum( k in 1..n_work_period)(x[i,j,k])==1);

% %OK 5- max 36hrs par semaine pour une infirmière
constraint forall(i in 1..n_nurse)(sum(j in 1..n_day, k in 1..n_work_period where k!=REPOS)(x[i,j,k])*dur_work_period <=36*n_week);

% %OK 6- can work min 4 jours dans la semaine
constraint forall(i in 1..n_nurse)(sum(j in 1..n_day, k in 1..n_work_period where k!=REPOS)(x[i,j,k])>=4);

% % %toVerif 7- jour j=nuit, alors obligé d'avoir jour j+1 = repos
constraint forall(i in 1..n_nurse, j in 1..n_day, k in 1..n_work_period)(if j+1 <= n_day then x[i,j,NUIT]==1 -> x[i,j+1,REPOS]==1 endif);

% %toVerif 8- sequence repos-travail-repos interdit
constraint forall(i in 1..n_nurse, j in 1..n_day, k in 1..n_work_period)(if j+2 <=n_day then (if x[i,j,4]=1 /\ x[i,j+1,4]=0 then x[i,j+2,4]=0 endif)endif);

% %OK 9- ne peut pas work plus de 3 jours consécutifs
constraint forall(i in 1..n_nurse, j in 1..n_day, k in 1..n_work_period)(if j+3<=n_day then(if x[i,j,4]=0 /\ x[i,j+1,4]=0 /\ x[i,j+2,4]=0 then x[i,j+3,4]=1 endif)endif);

% respecter demande_minimums de l'hopital
constraint forall(j in 1..n_day, k in 1..n_work_period)(sum(i in 1..n_nurse)(x[i,j,k]) >= demande_min[j, k]);

% prioriser les préférences des infirmières
sum_preference = sum(i in 1..n_nurse, j in 1..n_day, k in 1..n_work_period)(x[i,j,k]*preference[i,j,k]);

% solve satisfy;
solve maximize sum_preference;

output
[
  "total: " ++ show(sum_preference) ++ "\n" ++
  "solution:\n\t    "
]
++
["Day \(j)\t" | j in 1..n_day]
++ 
[ 
  if j = 1 then "\n NURSE \(i): " else "\t" endif ++
    if fix(x[i,j,4]) == 1 then "--" elseif fix(x[i,j,3]) == 1  then "NUIT" elseif fix(x[i,j,2]) == 1  then "SOIREE" elseif fix(x[i,j,1]) == 1 then "MATIN" else "NONE" endif
  | i in 1..n_nurse, j in 1..n_day
];

