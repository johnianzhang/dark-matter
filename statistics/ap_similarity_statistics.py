#!/usr/bin/env python3
"""A script for searching a folder of saved validation sets, and finding the ones that behave the most like Acoustic Parameter"""
# Created by Brendon Matusch, August 2018

import os
import sys

import numpy as np

from data_processing.experiment_serialization import load_test
from utilities.verify_arguments import verify_arguments

# A path to a folder of validation sets should be provided
verify_arguments('folder of saved validation sets')
# Get the full path and iterate over the files in the folder
folder = os.path.expanduser(sys.argv[1])
for file_name in os.listdir(folder):
    # Get the full path of the file
    file_path = os.path.join(folder, file_name)
    # Load the validation events and network outputs from the JSON file (ignoring the ground truths)
    events, _, network_outputs = load_test(file_path)
    # Convert the network outputs to binary predictions
    network_predictions = np.array([output >= 0.5 for output in network_outputs])
    # Do the same with the Acoustic Parameter
    ap_predictions = np.array([event.logarithmic_acoustic_parameter > 0.25 for event in events])
    # Calculate the number of events on which AP and the network disagree
    disagreements = np.count_nonzero(network_predictions != ap_predictions)
    print(disagreements)
