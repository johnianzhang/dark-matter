#!/usr/bin/env python3
"""A script for training a logistic regression model to separate loud from quiet triplet events"""
# Created by Brendon Matusch, August 2018

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from data_processing.load_triplet_classification_data import load_triplet_classification_data

# Load the triplet events
loud_events, quiet_events = load_triplet_classification_data()
# Stack an input array of flattened position-corrected 8-band Fourier transforms for all of the events together
inputs = np.stack([event.banded_frequency_domain.flatten() for event in loud_events + quiet_events])
# Make a binary output list, where 1 is loud and 0 is quiet
outputs = np.concatenate([np.ones(len(loud_events)), np.zeros(len(quiet_events))])
# Split the inputs and outputs into training and validation sets
training_inputs, validation_inputs, training_outputs, validation_outputs = train_test_split(inputs, outputs, test_size=0.15)
# Create a logistic regression classifier
classifier = LogisticRegression()
# Fit the classifier on the training input and output arrays
classifier.fit(training_inputs, training_outputs)
# Score the classifier on the validation arrays
score = classifier.score(validation_inputs, validation_outputs)
# Output the score to the user
print('Validation score:', score)
