%% INPUT
Q= [    
    0.1   -0.72   0.69  27.34
    0.81  -0.34  -0.48 -14.72
    0.58   0.6    0.54  18.63
    0     0     0     1  
];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Applying input  to Q values
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
q11 = Q(1,1);
q12 = Q(1,2);
q13 = Q(1,3);
q14 = Q(1,4);
q21 = Q(2,1);
q22 = Q(2,2);
q23 = Q(2,3);
q24 = Q(2,4);
q31 = Q(3,1);
q32 = Q(3,2);
q33 = Q(3,3);
q34 = Q(3,4);

%% Defining Di and Li
% Di vaLues
d1=16.3;
d2=0;
d3=0;
d4=0;
d5=10;

% Li vaLues 
l1=9.28;
l2=9.15;
l3=5.74;
l4=0;
l5=0;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% THETAS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Theta 3
T3 = asind((q34-d5*q33-d1)/l3);

%% Theta 4
T4 = asind(q33)-T3;

%% Theta 5
T5 = atan2d(-q32,q31);

%% Theta Unofficials
T1 = 0;
T2 = 0;
TA = T1 + T2 ;
TB = T3 + T4 ;

%% Theta 1
T1 = asind((q24-d5*sind(TA)*cosd(TB)-l3*sind(TA)*cosd(T3)+d4*cosd(TA)-l2*sind(TA))/l1);

%% Theta 2

if q31 == 0
    T2 = atan2d(q23,q13)-T1;

else
    T2 = asind(q23*cosd(T5)/q31)-T1;
end


TA = T1 + T2 ;
TB = T3 + T4 ;

% Theta 1
T1 = asind((q24-d5*sind(TA)*cosd(TB)-l3*sind(TA)*cosd(T3)+d4*cosd(TA)-l2*sind(TA))/l1);

% Theta 2

if q31 == 0
    T2 = atan2d(q23,q13)-T1;

else
    T2 = asind(q23*cosd(T5)/q31)-T1;
end
TA = T1 + T2 ;
TB = T3 + T4 ;

% Theta 1
T1 = asind((q24-d5*sind(TA)*cosd(TB)-l3*sind(TA)*cosd(T3)+d4*cosd(TA)-l2*sind(TA))/l1);

% Theta 2

if q31 == 0
    T2 = atan2d(q23,q13)-T1;

else
    T2 = asind(q23*cosd(T5)/q31)-T1;
end

% The just incases
% T2 =acosd(q13/cosd(TA))-T3;
% T2 = acosd(q13*cosd(T5)/q31)-T1;
% T2 = atan2d(q23,q13)-T1;
% T2 = acosd((q13*cosd(atan2d(-q32,q31)))/q31)-T1;

%T2 = asind(q23*cosd(T5)/q31)-T1;


t = [-1*real(T1) -1*real(T2) -1*real(T3) real(T4) -1*real(T5)]








