# filter_16.py
# 
# Implement the difference equation
# y(n) = b0*x(n) - b1*x(n-1) - a1*y(n-1) - a2*y(n-2)
# H(z) = 1 / (1 + a1/z + a2/z^2)        Initial transfer function
# H(z) = B(z) / (1 + a1/z + a2/z^2)     Modified transfer function
# b0 = 1
# b1 = -rcos(om1)
# a1 = -2rcos(om1)
# a2 = r^2

# 16 bit/sample

from math import cos, pi 
import pyaudio
import struct
import wave


# Fs : Sampling frequency (samples/second)
Fs = 8000
F1 =400
# Also try other values of 'Fs'. What happens? Why?

T = 1       # T : Duration of audio to play (seconds)
N = T*Fs    # N : Number of samples to play
r = 0.999
om1 = 2*pi*(F1/Fs)

# Difference equation coefficients
a1 = -2*r*cos(om1)
a2 = r**2
b0 = 1
b1 = -r*cos(om1)
# Initialization
y1 = 0.0
y2 = 0.0
x1 = 0.0
gain = 10000.0
# Also try other values of 'gain'. What is the effect?
# gain = 20000.0

# Create an audio object and open an audio stream for output
p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,  
                channels = 1, 
                rate = Fs,
                input = False, 
                output = True)

# Set up the wave file
wf = wave.open("output.wav", "w")
wf.setnchannels(1)
wf.setsampwidth(2)
wf.setframerate(Fs)

# paInt16 is 16 bits/sample

# Run difference equation
for n in range(0, N):

    # Use impulse as input signal
    if n == 0:
        x0 = 1.0

    else:
        x0 = 0.0

    # Difference equation
    y0 = b0 * x0 + b1 * x1 - a1 * y1 - a2 * y2 

    # Delays
    y2 = y1
    y1 = y0
    x1 = x0

    # Output
    output_value = gain * y0
    output_string = struct.pack('h', int(output_value))   # 'h' for 16 bits
    stream.write(output_string)

    # Write the output to the wave file
    wf.writeframes(output_string)

print("* Finished *")

stream.stop_stream()
stream.close()
p.terminate()

#How should the gain be set to ensure the impulse response does not exceed the maximum allowed value of 2^15-1 ?
#Answer: 
#We can divide 'y0' by the maximum allowed value of 2^15-1 to scale the 
#impulse response to be within the range of -1 to 1 and then by multiplying
#by desired gain we can make sure the impilse respose has the desired magnitude.





