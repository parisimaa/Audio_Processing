import pyaudio
import wave
import struct
import math
import time
import sys

if len(sys.argv) < 2:
    print('Error: filename.wav required')
    sys.exit(-1)

filename = sys.argv[1]

def clip16(x):
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x
    return x

gain1 = 1.0
gain2 = 0.5

# Open wave file
wf = wave.open(filename, 'rb')

print('Play the wave file %s.' % filename)

# Read the wave file properties
num_channels = wf.getnchannels()  # Number of channels
RATE = wf.getframerate()  # Sampling rate (frames/second)
signal_length = wf.getnframes()  # Signal length
width = wf.getsampwidth()  # Number of bytes per sample

print('SIGNAL INFORMATION')
print('The file has %d channel(s).' % num_channels)
print('The frame rate is %d frames/second.' % RATE)
print('The file has %d frames.' % signal_length)
print('There are %d bytes per sample.' % width)

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format=pyaudio.paInt16,
    channels=num_channels,
    rate=RATE,
    input=False,
    output=True
)

# Get first frame
input_bytes = wf.readframes(1)

# Processing signal
while len(input_bytes) > 0:

    # Convert binary data to numbers
    if num_channels == 1:
        input_tuple = struct.unpack('h', input_bytes)  # One-element tuple
        input_value = input_tuple[0]  # Number
        output_value = int(clip16(gain1 * input_value))
        output_bytes = struct.pack('h', output_value)
    else:
        input_tuple = struct.unpack('hh', input_bytes)  # Two-element tuple
        output_value0 = int(clip16(gain2 * input_tuple[0]))
        output_value1 = int(clip16(gain2 * input_tuple[1]))
        output_bytes = struct.pack('hh', output_value0, output_value1)

    # Write output value to audio stream
    stream.write(output_bytes)

    # Get next frame
    input_bytes = wf.readframes(1)

print('* Finished *')

# Ending the process of both signals
# Also these lines can be after each while loop
stream.stop_stream()
stream.close()
p.terminate()
