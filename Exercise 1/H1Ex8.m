%% Hw1-Q8

clc
clear
close all

% Load .wav file
[x, Fs] = audioread('sin_01_Multi.wav');
% listen to audio
%soundsc(x, Fs)
whos

% Time axis in seconds
N = length(x);
t = (1:N)/Fs;
figure;
clf
plot(t,x)
xlabel('Time (sec)')
title('Signal')

% Extracting different channels

% Extract the first channel
channel1 = x(:,1);

% Plot the first channel
figure
plot(channel1)
title('First Channel')
xlim([1500 2000])
ylim([-1 1])
% Extract the second channel
channel2 = x(:,2);

% Plot the second channel
figure
plot(channel2)
title('Second Channel')
xlim([1500 2000])
ylim([-1 1])
% Extract the third channel
channel3 = x(:,3);

% Plot the third channel
figure
plot(channel3)
title('Third Channel')
xlim([1500 2000])
ylim([-1 1])