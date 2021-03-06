function [ s,error ] = Problem42
% Thomas Schmelzer, November 2008
% computes the limit of the Kempner series \sum_{n=1}^\infty 1/n
% where n does not contain the substring "42" --- a problem that has been
% proposed by Folkmar Bornemann. For details see
% Schmelzer, Thomas; Robert Baillie (June�July 2008). "Summing a Curious,
% Slowly Convergent Series". American Mathematical Monthly 115 (6): 525�540
% exact solution: 228.44630 41592 30813 25414 80861 26250 58957 81629 ...
%% given the recurrence matrix T, compute f,A and B.
T = [1 1 1 1 2 1 1 1 1 1; 1 1 0 1 2 1 1 1 1 1];
[I,J] = find(T); f = zeros(2,2,10); A = zeros(2,2);
for s = 1:length(I)
    f(T(I(s),J(s)),I(s),J(s))=1;
end
for s = 0:9
    A = A + f(:,:,s+1)/10;
end
I = eye(size(A)); B = inv(I-A)-I;
#disp(B)

%% define the S_1 and S_2 explicitly for integers with up to 5 digits
S = cell(5,2); S{1,1} = [1,2,3,5,6,7,8,9]; S{1,2} = 4;
for i = 2:size(S,1)
    for m = 0:1:9    % possible digits to attend
        [J,L] = find(f(:,:,m+1));
        for s = 1:length(J)
            S{i,J(s)} = [S{i,J(s)},10*S{i-1,L(s)}+m];
        end
    end
end
#disp(S)


%% define the numerical parameters
K = 20;  % extrapolation
P = 30;  % power cutoff
Ignore = -22;
Psi = zeros(K,2,P);
% compute the sums Psi_{i} explicitly for up to 5 digits
for i = 1:size(S,1)      # ... = 5
    for k = 1:P
        Psi(i,1,k) = sum(S{i,1}.^(-k));
        Psi(i,2,k) = sum(S{i,2}.^(-k));
    end
end

#disp(Psi)


warning('off','MATLAB:log:logOfZero');
for i = size(S,1)+1:1:K
    for k = 1:P
        if (Psi(i-1,1,k)>0)
            for m = 0:9
                [J,L] = find(f(:,:,m+1));
                for s = 1:length(J)
                    for w = 0:P-k
                       if log10(abs(aCoeff(k,w,m))) + log10(abs(Psi(i-1,L(s),k+w))) > Ignore;
                           Psi(i,J(s),k) = Psi(i,J(s),k)+aCoeff(k,w,m)*Psi(i-1,L(s),k+w);
                       end
                    end
                end
            end
        end
    end
end
warning('on','MATLAB:log:logOfZero');
% Extrapolation

disp(sum(B*Psi(K,:,1)'))
disp(sum(sum(Psi(:,:,1))))

s = sum(B*Psi(K,:,1)') + sum(sum(Psi(:,:,1)));
error = 228.44630415923081325414 - s;
function [ a ] = aCoeff( k,w,m )
if (m+w==0)
    mw = 1;
else
    mw = m^w;
end
a = 10^(-k-w)*mw*(-1)^w*nchoosek(k+w-1,w);