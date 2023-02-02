%% HW1 - Q5

clc
clear
close all

% Load .wav file
[x, Fs] = audioread('sin.wav');
% listen to audio
soundsc(x, Fs)

% Time axis in seconds
N = length(x);
t = (1:N)/Fs;
figure;
clf
plot(t,x)
xlabel('Time (sec)')
title('Signal')

% Distribution of samples
xs = sort(x);
figure;
clf
plot(xs)
title('Sorted signal values')

% The quantization increment
% smallest positive value (SPV)
SPV = min(x(x>0)); 
1/SPV % 1/2^7 
%% 
% which confirms that the signal is 8-bits per sample

% Frequency spectrum
% Using FFT
% use power of 2 for FFT efficiency
N = length(x);
Nfft = 2^ceil(2+log2(N)); 
% Compute the FT
X = fft(x,Nfft);
k = 0:Nfft-1; % index
figure;
clf
plot(k, abs(X))
xlabel('FFT index')
title('Spectrum')

% Center DC
X2 = fftshift(X);
k2 = -Nfft/2 : Nfft/2-1;
figure;
clf
plot(k2, abs(X2))
xlabel('FFT index')
title('Spectrum')
%% 
% spectrum of sin signal is as we expected!
% 
% There is a slight difference in the quality of the sound.