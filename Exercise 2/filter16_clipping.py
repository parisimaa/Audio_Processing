# Implement the second-order recursive difference equation
# y(n) = x(n) - a1 y(n-1) - a2 y(n-2)

# 16 bit/sample

from math import cos, pi 
import pyaudio
import struct

# Fs : Sampling frequency (samples/second)
Fs = 8000


T = 1       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play

# Difference equation coefficients
a1 = -1.9
a2 = 0.998

# Initialization
y1 = 0.0
y2 = 0.0
#gain = 10000.0
gain = 20000.0

# Create an audio object and open an audio stream for output
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16, channels = 1, rate = Fs, input = False, output = True)
# Input signal True if you have a microphone 
# paInt16 is 16 bits/sample

# Run difference equation
for n in range(0, N):

    # Use impulse as input signal
    if n == 0:
        x0 = 1.0
    else:
        x0 = 0.0

    # Difference equation
    y0 = x0 - a1 * y1 - a2 * y2

    # Delays
    y2 = y1
    y1 = y0

    # Output
    output_value = gain * y0
    # Overflow checking and clipping
    if output_value > 2**15 - 1:
    	output_value = 2**15 - 1
    elif output_value < -2**15:
    	output_value = -2**15
    output_string = struct.pack('h', int(output_value))   # 'h' for 16 bits
    stream.write(output_string)

print("* Finished *")

stream.stop_stream()
stream.close()
p.terminate()

# Also try other values of 'gain'. What is the effect?
# If we decrease the gain in our code the audio will be less loud and vice versa. (increasing gain to sth out of range will cause overflow and cause error)
# Also try other values of 'Fs'. What happens? Why?
# Frequency of the total signal can be changed by Fs but it is also depends on a1 and a2.

# For preventing an overflow with larger choosen gains, I added a condition
# to check if the output_value is within the range and it is compatible with 
# 'h' format

# We can choose a1 and a2 to change frequency of signal without changing Fs itself. (Please check the note)
# The result:
# a1 = -2rcos(w1)
# a2 = r^2
# Given N we find r in this way:
# r^N = 0.01