# Quantum Machine Learning Project

This repository demonstrates the use of quantum computing for machine learning tasks. The project combines classical Python programming with quantum circuits written in QASM (Quantum Assembly Language).

## Project Structure

The repository includes the following files:

- **`embeded_with_python.py`**: A Python script that integrates quantum operations with classical programming. It showcases how quantum machine learning models can be embedded into Python workflows.

- The code uses Qiskit for quantum computing operations

- Initializes a network with 4 qubits and 3 trainable parameters

- 1. Circuit Creation
- Creates a quantum circuit with 4 qubits
- Encodes input data using RX (rotation around X-axis) gates
- Applies trainable parameters using RY (rotation around Y-axis) gates
- Adds entanglement using CNOT gates between adjacent qubits

- 2. State Vector and Probability Calculation
- Computes the quantum state vector of the circuit
- Calculates the probability of measuring |1⟩ on the specified qubit (default is qubit 0)

- 3.Training Process
- Initializes random parameters between 0 and 2π
- Uses gradient descent with learning rate 0.01
- For each epoch:
- a.Creates circuit with current parameters
- b.Calculates output probability
- c.Computes loss (mean squared error)
- d.Updates parameters using gradients

- 4.Gradient Calculation
- Uses numerical differentiation (finite differences)
- Calculates gradient for each parameter by:
- a.Adding/subtracting small epsilon
- b.Computing probability difference
- c.Approximating derivative

- 5.Main Execution
- Sets random seed for reproducibility

- Creates random training data and binary labels

- Trains the network for 5000 epochs

- Tests the trained network on new data

- Saves the final circuit in QASM format

- 6.Conclusion:
- Key Features:
- Uses hybrid quantum-classical approach

- Implements gradient descent optimization

- Supports binary classification

- Includes data encoding through rotation gates

- Creates entanglement between qubits

- Provides both training and inference capabilities

- Exports to QASM format for quantum hardware compatibility

- The network learns by adjusting the rotation angles (parameters) to minimize the difference between predicted probabilities and actual labels, using quantum operations for computation and classical optimization for parameter updates.

- **`basic_ML.qasm`**: A QASM file defining a basic quantum machine learning circuit.
- **`trained_neural_network.qasm`**: A QASM file representing a trained quantum neural network.
- **`readme.md`**: Documentation for the project (this file).

## Requirements

To run this project, you need the following:

- Python 3.7 or later
- Quantum computing tools such as:
  - IBM Qiskit (for simulating and running quantum circuits)
  - A QASM-compatible quantum simulator or hardware
- Additional Python dependencies, which can be installed using:

  ```bash
  pip install -r requirements.txt
  ```

## How to Use

### 1. Running the Quantum Circuits

- Use a QASM simulator or quantum hardware to execute the `.qasm` files.
- Load the `basic_ML.qasm` or `trained_neural_network.qasm` into your quantum environment to simulate the circuits.

### 2. Embedding with Python

- Run the `embeded_with_python.py` script to see how quantum operations integrate with classical machine learning workflows.

  ```bash
  python embeded_with_python.py
  ```

### 3. Customization

- Modify the `.qasm` files to explore different quantum machine learning algorithms.
- Enhance the Python script to include data preprocessing, result analysis, or more complex workflows.

## Files Overview

### **`embeded_with_python.py`**

This script demonstrates:

- How to embed quantum circuits into a Python environment.
- A basic hybrid quantum-classical machine learning model.

### **`basic_ML.qasm`**

Defines a simple quantum circuit for basic machine learning tasks. Suitable for understanding foundational quantum operations.

### **`trained_neural_network.qasm`**

Represents a more advanced quantum neural network that has been trained to perform specific tasks.

## Future Enhancements

- Add more advanced quantum machine learning models.
- Integrate with cloud-based quantum platforms like IBM Quantum or Google Cirq.
- Explore hybrid quantum-classical optimization techniques.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
