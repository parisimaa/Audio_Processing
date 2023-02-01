% Recording your audio
clc
clear
close all

% Recording a wav file with one channel, sampling rate of 16 kHz, 16-bits
% per sample
sound = audiorecorder(16000,16,1);
recordblocking(sound,1);
play(sound);
MyAudio = getaudiodata(sound);
speech = MyAudio;
%sound(speech,16000);
audiowrite('MyAudio.wav',speech,16000);
test = audioread('MyAudio.wav');