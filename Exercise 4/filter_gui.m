function filter_gui

N = 500;
n = 1:N;
x = sin(5*pi*n/N) + 0.5 * randn(1, N);        % Input signal

figure(1)
set(gcf,'Position',[100 100 800 600])
clf
subplot(3,1,1)
line_handle = plot(n, x, 'LineWidth', 1); % Ploting input signal
title('Noisy data', 'fontsize', 12 )
xlabel('Time')
box off
xlim([0, N]);
ylim([-3 3])

% Impulse response
subplot(3,1,2)
h = zeros(1,N*500);
h_imp = plot(h, 'LineWidth', 1, 'color', 'r', 'LineStyle', '-');
title('Impulse Response', 'fontsize', 12)
xlabel('Time')
ylabel('Amplitude')
box off
xlim([0, N/10]);
ylim([-0.5 1])

% Frequency response
subplot(3,1,3)
f = zeros(1,N*500);
h_freq = plot(f, 'LineWidth', 1, 'color', 'r', 'LineStyle', '-');
title('Frequency Response', 'fontsize', 12)
xlabel('Frequency (Hz)')
ylabel('Magnitude (dB)')
box off
xlim([0, N/2]);
ylim([-60 0])

uicontrol('Style', 'slider', ...
    'Min', 0.0, 'Max', 0.5,...
    'Value', 0.2, ...
    'SliderStep', [0.02 0.05], ...
    'Position', [5 5 200 20], ...           % [left, bottom, width, height]
    'Callback',  {@fun1, line_handle, x, h_imp, h_freq}    );

end


function fun1(hObject, eventdata, line_handle, x, h_imp, h_freq)

fc = get(hObject, 'Value');  % fc : cut-off frequency
N = 500;

fc = max(fc, 0.01);
fc = min(fc, 0.49);

[b, a] = butter(3, 2*fc);   % Order-2 Butterworth filter (multiply fc by 2 due to non-conventional Matlab convention)
y = filtfilt(b, a, x);

% Impulse response
h = impz(b, a);

% Frequency response
f = fft(y);
f = f(1:N/2+1);
f = abs(f);
f = f / max(f);  % Normalize to 0-1 range
f = 20*log10(f);


title( sprintf('Output of LPF. Cut-off frequency = %.3f', fc), 'fontsize', 12 )
set(h_imp, 'ydata',  h); 
set(h_freq, 'xdata', linspace(0,1,N/2+1)*500/2, 'ydata', f);
set(line_handle, 'ydata',  y);        % Update data in figure
end
