# Single program for mono and stereo
#
# A single Python program that play both mono and stereo wave files. 
# The program determine the number of channels by reading the wave file information.
# This program can play both mono and stereo wave files encoded with 16-bits per sample.

import pyaudio
import wave
import struct
import math
import time

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return (x)

gain1 = 1.0
gain2 = 0.5

# Loading mono and stereo signals
wavefile_mono = 'author.wav'
wavefile_stereo = 'sin01_stereo.wav'

print('Play the wave file %s.' % wavefile_mono)
print('Play the wave file %s.' % wavefile_stereo)

# Open wave file 
wf_mono = wave.open( wavefile_mono, 'rb')
wf_stereo = wave.open( wavefile_stereo, 'rb' )

# Read the wave file properties (Mono signal)
num_channels1    = wf_mono.getnchannels()     # Number of channels
RATE1            = wf_mono.getframerate()     # Sampling rate (frames/second)
signal_length1   = wf_mono.getnframes()       # Signal length
width1           = wf_mono.getsampwidth()     # Number of bytes per sample

# Read the wave file properties (Stereo signal)
num_channels2    = wf_stereo.getnchannels()     # Number of channels
RATE2            = wf_stereo.getframerate()     # Sampling rate (frames/second)
signal_length2   = wf_stereo.getnframes()       # Signal length
width2           = wf_stereo.getsampwidth()     # Number of bytes per sample

print('MONO SIGNAL INFORMATION')
print('The file has %d channel(s).'            % num_channels1)
print('The frame rate is %d frames/second.'    % RATE1)
print('The file has %d frames.'                % signal_length1)
print('There are %d bytes per sample.'         % width1)

print('STEREO SIGNAL INFORMATION')
print('The file has %d channel(s).'            % num_channels2)
print('The frame rate is %d frames/second.'    % RATE2)
print('The file has %d frames.'                % signal_length2)
print('There are %d bytes per sample.'         % width2)

p1 = pyaudio.PyAudio()
p2 = pyaudio.PyAudio()

# Open audio stream
stream1 = p1.open(
    format      = pyaudio.paInt16,
    channels    = num_channels1,
    rate        = RATE1,
    input       = False,
    output      = True )

stream2 = p2.open(
    format      = pyaudio.paInt16,
    channels    = num_channels2,
    rate        = RATE2,
    input       = False,
    output      = True )

# Get first frame
input_bytes1 = wf_mono.readframes(1)
input_bytes2 = wf_stereo.readframes(1)

# Processing Mono signal
while len(input_bytes1) > 0:

    # Convert binary data to number
    input_tuple1 = struct.unpack('h', input_bytes1)  # One-element tuple (unpack produces a tuple)
    input_value = input_tuple1[0]                    # Number

    # Compute output value
    output_value = int(clip16(gain1 * input_value))  # Integer in allowed range

    # Convert output value to binary data
    output_bytes1 = struct.pack('h', output_value)  

    # Write binary data to audio stream
    stream1.write(output_bytes1)                     

    # Get next frame
    input_bytes1 = wf_mono.readframes(1)

# Delay between two audio
time.sleep(1)

# Processing Stereo signal
while len(input_bytes2) > 0:

    # Convert binary data to numbers
    input_tuple2 = struct.unpack('hh', input_bytes2)  # produces a two-element tuple

    # Compute output values
    output_value0 = int(clip16(gain2 * input_tuple2[0]))
    output_value1 = int(clip16(gain2 * input_tuple2[1]))

    # Convert output value to binary data
    output_bytes2 = struct.pack('hh', output_value0, output_value1)

    # Write output value to audio stream
    stream2.write(output_bytes2)

    # Get next frame
    input_bytes2 = wf_stereo.readframes(1)

print('* Finished *')
# Ending the process of both signals
# Also these lines can be after each while loop
stream1.stop_stream()
stream1.close()
p1.terminate()
stream2.stop_stream()
stream2.close()
p2.terminate()
