# wave_filter_python.py

import pyaudio
import wave
import struct
import math

from myfunctions import clip16

wavefile = 'author.wav'

print('Play the wave file %s.' % wavefile)

# Open wave file (should be mono channel)
wf = wave.open( wavefile, 'rb' )

# Read the wave file properties
num_channels    = wf.getnchannels()     # Number of channels
RATE            = wf.getframerate()     # Sampling rate (frames/second)
signal_length   = wf.getnframes()       # Signal length
width           = wf.getsampwidth()     # Number of bytes per sample

print('The file has %d channel(s).'            % num_channels)
print('The frame rate is %d frames/second.'    % RATE)
print('The file has %d frames.'                % signal_length)
print('There are %d bytes per sample.'         % width)

# Difference equation coefficients
b0 =  0.008442692929081
b1 = 0
b2 = -0.016885385858161
b3 = 0
b4 =  0.008442692929081

# a0 =  1.000000000000000
a1 = -3.580673542760982
a2 =  4.942669993770672
a3 = -3.114402101627517
a4 =  0.757546944478829

# Initialization
w1 = 0.0
w2 = 0.0
w3 = 0.0
w4 = 0.0


p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format      = pyaudio.paInt16,
    channels    = num_channels,
    rate        = RATE,
    input       = False,
    output      = True )

# Get first frame from wave file
input_bytes = wf.readframes(1)

while len(input_bytes) > 0:

    # Convert binary data to number
    input_tuple = struct.unpack('h', input_bytes)  # One-element tuple
    input_value = input_tuple[0]                    # Number

    # Set input to difference equation
    x0 = input_value

    # Difference equation
    w0 = x0 - a1 * w1 - a2 * w2 - a3 * w3 - a4 * w4
    y0 = b0*w0 + b1*w1 + b2*w2 + b3*w3 + b4*w4
    #The general form of the canonical difference equation is:
    #y(n) = b0w0 + b1w1 + ... + bM*wM
    #w0 = x(n) - a1w1 - a2w2 - ... - aM*wM
    # Delays
    w4 = w3
    w3 = w2
    w2 = w1
    w1 = w0

    # Compute output value
    output_value = int(clip16(y0))    # Integer in allowed range

    # Convert output value to binary data
    output_bytes = struct.pack('h', output_value)  

    # Write binary data to audio stream
    stream.write(output_bytes)                     

    # Get next frame from wave file
    input_bytes = wf.readframes(1)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
