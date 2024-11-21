OPENQASM 3.0;
include "stdgates.inc";

// Define quantum registers for the feature space and classification
qubit[2] feature_register;   // For encoding 2 features
qubit classification;        // For the classification result

// Define classical register to store the measurement
bit[3] result;              // To store measurement results

// Data encoding circuit - prepare the quantum state
// Encode features using rotation gates
rx(pi/4) feature_register[0];
ry(pi/3) feature_register[1];

// Create entanglement between features
cx feature_register[0], feature_register[1];

// Classification layer
h classification;
cx feature_register[0], classification;
cx feature_register[1], classification;

// Optional: Add a measurement barrier
barrier feature_register, classification;

// Measure the results
measure feature_register[0] -> result[0];
measure feature_register[1] -> result[1];
measure classification -> result[2];
