from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector
from qiskit.circuit import Parameter
import numpy as np
import sys

class QASMNeuralNetwork:
    def __init__(self):
        self.num_qubits = 4
        self.num_parameters = 3

    def create_quantum_circuit(self, input_data, parameters):
        qc = QuantumCircuit(self.num_qubits)
        
        # Encode input data using rotation gates
        for i, data in enumerate(input_data):
            qc.rx(data, i)
        
        # Add trainable parameters using rotation gates
        qc.ry(parameters[0], 0)
        qc.ry(parameters[1], 1)
        qc.ry(parameters[2], 2)
        
        # Add entanglement layers
        for i in range(self.num_qubits - 1):
            qc.cx(i, i + 1)
        qc.cx(self.num_qubits - 1, 0)
        
        return qc

    def get_statevector(self, circuit):
        statevector = Statevector.from_instruction(circuit)
        return statevector

    def calculate_probability(self, statevector, qubit_idx=0):
        probabilities = statevector.probabilities([qubit_idx])
        return probabilities[1]  # Probability of |1⟩

    def train_network(self, training_data, labels, epochs=100):
        parameters = np.random.rand(3) * 2 * np.pi
        learning_rate = 0.01
        
        for epoch in range(epochs):
            total_loss = 0
            for data, label in zip(training_data, labels):
                # Forward pass
                circuit = self.create_quantum_circuit(data, parameters)
                statevector = self.get_statevector(circuit)
                output_prob = self.calculate_probability(statevector)
                
                # Calculate loss
                loss = (output_prob - label) ** 2
                total_loss += loss
                
                # Calculate gradient and update parameters
                gradient = self.calculate_gradient(data, parameters, label)
                parameters -= learning_rate * gradient
            
            if epoch % 10 == 0:
                print(f"Epoch {epoch}, Loss: {total_loss/len(training_data)}")
        
        return parameters

    def calculate_gradient(self, input_data, parameters, label):
        epsilon = 0.01
        gradient = np.zeros_like(parameters)
        
        for i in range(len(parameters)):
            parameters_plus = parameters.copy()
            parameters_minus = parameters.copy()
            parameters_plus[i] += epsilon
            parameters_minus[i] -= epsilon
            
            circuit_plus = self.create_quantum_circuit(input_data, parameters_plus)
            statevector_plus = self.get_statevector(circuit_plus)
            prob_plus = self.calculate_probability(statevector_plus)
            
            circuit_minus = self.create_quantum_circuit(input_data, parameters_minus)
            statevector_minus = self.get_statevector(circuit_minus)
            prob_minus = self.calculate_probability(statevector_minus)
            
            gradient[i] = (prob_plus - prob_minus) / (2 * epsilon)
        
        return gradient

def main():
def main():
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create sample data
    num_samples = 10
    training_data = np.random.rand(num_samples, 4) * 2 * np.pi
    labels = np.random.randint(0, 2, num_samples)
    
    # Create and train the network with 1000 epochs
    qnn = QASMNeuralNetwork()
    trained_parameters = qnn.train_network(training_data, labels, epochs=1000)  # Changed to 1000 epochs

    
    # Test the trained network
    test_data = np.random.rand(4) * 2 * np.pi
    test_circuit = qnn.create_quantum_circuit(test_data, trained_parameters)
    test_statevector = qnn.get_statevector(test_circuit)
    prediction = qnn.calculate_probability(test_statevector)
    
    print(f"\nTest prediction: {prediction}")
    print(f"Final parameters: {trained_parameters}")
    
    # Save the final QASM code
    final_circuit = qnn.create_quantum_circuit(test_data, trained_parameters)
    try:
        # Try the new method first
        qasm_str = final_circuit.qasm_str()
    except AttributeError:
        # Fallback for older versions
        try:
            qasm_str = final_circuit.qasm()
        except AttributeError:
            print("Warning: Could not generate QASM string. This version of Qiskit might not support QASM output.")
            qasm_str = str(final_circuit)
    
    with open('trained_neural_network.qasm', 'w') as f:
        f.write(qasm_str)
    print("\nFinal circuit representation saved to 'trained_neural_network.qasm'")

if __name__ == "__main__":
    main()
