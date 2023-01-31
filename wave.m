clc
clear
close all

% Load .wav file
[x, Fs] = audioread('cat01.wav');
% x: the signal
% Fs: sampling frequency
% x has one column so it is one channel signal

% listen to audio
soundsc(x, Fs)
% slower by multiplying Fs to smaller number or faster by multiplying to
% larger number

% Plot waveform
figure;
clf
plot(x)
xlabel('Time (sample)')
title('Signal')

% Time axis in seconds
N = length(x);
t = (1:N)/Fs;
figure;
clf
plot(t,x)
xlabel('Time (sec)')
title('Signal')

% Zoom in to 50 msec
xlim(0.4+[0 0.050])

% Distribution of samples
xs = sort(x);
figure;
clf
plot(xs)
title('Sorted signal values')

% See quantization
ylim([-0.0002 0.0002])
grid

% The quantization increment
% smallest positive value (SPV)
SPV = min(x(x>0)); % 1/2^15

% All values x(n) are integer multiplies of 1/2^15, why?
% The signal is represented with 16 bits per sample

% Frequency spectrum
% Using FFT
% use power of 2 for FFT efficiency
N = length(x);
Nfft = 2^ceil(2+log2(N)); % length of the FFT
% smallest power of 2 greater than signal length

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

% it is better for the x-axis scale to be in HZ but if we dont know the
% sampling rate, it's better to use normalized frequency
% Normalized frequency in in units of [cycles per sample]

% Normalized frequency
fn = (-Nfft/2 : Nfft/2-1)/ Nfft;
figure;
clf
plot(fn, abs(X2))
xlabel('Frequency (cycles/sample)')
title('Spectrum')

% Frequency in Hz
f = fn * Fs;
figure, clf
plot(f, abs(X2))
xlabel('Frequency (cycles/second, i.e. Hz)')
title('Spectrum')








