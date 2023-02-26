% Echo via cicular buffer
% According to python program demo:
% The difference equation is as follow: 

%     y(n) = b0 * x(n) + G * x(n-N)

% x(n): the input signal at time n
% y(n): the output signal at time n
% b0 input gain, G delayed signal gain

% The transfer function of the filter can be obtained 
% by taking the Z-transform of the difference equation:

%     Y(z) = b0 * X(z) + G * z^(-N) * X(z)

% The impulse response of the filter is:

%     h(n) = b0 * delta(n) + G * delta(n-N)

clc
clear
close all

info = audioinfo('author.wav')
[x, Fs] = audioread('author.wav');
soundsc(x, Fs)
%%
delay_sec = 0.05;
G = 0.8;
N = 100 * delay_sec;
b = [1, zeros(1, N-1), G];
a = [1];
zplane(b, a);
