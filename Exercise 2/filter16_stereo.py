from math import cos, pi 
import pyaudio
import struct

# Fs : Sampling frequency (samples/second)
#Fs = 8000
Fs = 12000   
# Fs = 16000

T = 2       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play

# Pole location
f1 = 400.0
f2 = 800.0
om1 = 2.0*pi * f1/Fs # Angle of the pole (rand)
om2 = 2.0*pi * f2/Fs # Angle of the pole (rand)
r = 0.9998     # Try other values, 0.998, 0.9995, 1.0
# Qustion: how to set r to obtain desired time constant? r^N = 0.01
# The duration of the signal is controled by r (if we decrease the r the duration will be shorter)


# Difference equation coefficients
a1 = -2*r*cos(om1)
a2 = r**2

a3 = -2*r*cos(om2)
a4 = r**2

# Initialization
y1 = 0.0
y2 = 0.0
y3 = 0.0
y4 = 0.0
gain = 5000.0

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,  
                channels = 2, 
                rate = Fs,
                input = False, 
                output = True)

for n in range(0, N):

    # Use impulse as input signal
    if n == 0:
        x0 = 1.0
    else:
        x0 = 0.0

    # Difference equation for left channel
    y0 = x0 - a1 * y1 - a2 * y2

    # Delays for left channel
    y2 = y1
    y1 = y0

    # Output for left channel
    output_value1 = gain * y0
    output_string1 = struct.pack('h', int(output_value1))     # 'h' for 16 bits

    # Difference equation for right channel
    y3 = x0 - a3 * y3 - a4 * y4

    # Delays for right channel
    y4 = y3
    y3 = y0

    # Output for right channel
    output_value2 = gain * y3
    output_string2 = struct.pack('h', int(output_value2))     # 'h' for 16 bits

    # Combine the two output strings into one string
    output_string = output_string1 + output_string2
    stream.write(output_string)

print("* Finished *")

stream.stop_stream()
stream.close()
p.terminate()
