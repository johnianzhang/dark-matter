"""A function for loading a folder of audio files in WAV format"""
# Created by Brendon Matusch, June 2018

import os
import sys
import numpy as np

# The number of piezo channels present in the file (not all of them work)
CHANNELS = 8


def load_audio(file_path: str) -> np.ndarray:
    """Load an audio file in the MATLAB binary format present in the PICO-60 data set"""
    # Open the file for binary reading
    with open(os.path.expanduser(file_path), 'rb') as audio_file:
        # Read and ignore 4 bytes which comprise the header
        audio_file.read(4)
        # The next 2 bytes are the length of the string describing the channels
        channels_description_length = int.from_bytes(
            audio_file.read(2), sys.byteorder)
        # Read the channels description string from the file now, and decode it as a string
        channels_description = audio_file.read(
            channels_description_length).decode()
        # Read the number of samples from the file, which is used in parsing the rest of the file
        samples = int.from_bytes(audio_file.read(4), sys.byteorder)
        # The rest of the file consists of 2-byte integers, one per channel per sample; read all of it
        raw_data = audio_file.read(CHANNELS * samples * 2)
    # Convert the data into a 1-dimensional NumPy array
    data_array_flat = np.fromstring(raw_data, dtype=np.int16)
    # Reshape the 1-dimensional array into channels and samples
    data_array = np.reshape(data_array_flat, (samples, CHANNELS))
    # Transpose it so that the channels axis comes first
    data_array = np.transpose(data_array)
    print(data_array)


load_audio('~/Desktop/20170101_0/20170101_0/0/fastDAQ_0.bin')
