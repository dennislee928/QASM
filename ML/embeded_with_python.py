from qiskit import QuantumCircuit
from qiskit.primitives import Sampler  # New way to handle execution
from qiskit.quantum_info import Operator
from qiskit.circuit import Parameter
import numpy as np
import sys
#print("Python executable:", sys.executable)
#print("Python path:", sys.path)
#try:
 #   import qiskit
  #  print("Qiskit version:", qiskit.__version__)
#except ImportError as e:#
#    print("Import error:", e)


class QASMNeuralNetwork:
    def __init__(self):
        # Rest of your __init__ code remains the same
        pass

    def create_quantum_circuit(self, input_data, parameters):
        # Your existing code remains the same
        pass

    def train_network(self, training_data, labels, epochs=100):
        parameters = np.random.rand(3) * 2 * np.pi
        learning_rate = 0.01
        
        # Create a sampler
        sampler = Sampler()
        
        for epoch in range(epochs):
            total_loss = 0
            for data, label in zip(training_data, labels):
                # Forward pass
                circuit = self.create_quantum_circuit(data, parameters)
                # New way to execute circuits
                result = sampler.run(circuit, shots=1000).result()
                counts = result.quasi_dists[0]
                
                # Calculate output probability
                output_prob = self.calculate_output_probability(counts)
                
                # Rest of your training code remains the same
                loss = (output_prob - label) ** 2
                total_loss += loss
                
                gradient = self.calculate_gradient(data, parameters, label)
                parameters -= learning_rate * gradient
            
            if epoch % 10 == 0:
                print(f"Epoch {epoch}, Loss: {total_loss/len(training_data)}")
        
        return parameters

    def calculate_gradient(self, input_data, parameters, label):
        epsilon = 0.01
        gradient = np.zeros_like(parameters)
        sampler = Sampler()
        
        for i in range(len(parameters)):
            parameters_plus = parameters.copy()
            parameters_plus[i] += epsilon
            
            parameters_minus = parameters.copy()
            parameters_minus[i] -= epsilon
            
            # Calculate forward passes with new execution method
            circuit_plus = self.create_quantum_circuit(input_data, parameters_plus)
            result_plus = sampler.run(circuit_plus, shots=1000).result()
            prob_plus = self.calculate_output_probability(result_plus.quasi_dists[0])
            
            circuit_minus = self.create_quantum_circuit(input_data, parameters_minus)
            result_minus = sampler.run(circuit_minus, shots=1000).result()
            prob_minus = self.calculate_output_probability(result_minus.quasi_dists[0])
            
            gradient[i] = (prob_plus - prob_minus) / (2 * epsilon)
        
        return gradient

    def calculate_output_probability(self, counts):
        # You might need to adjust this method based on the new counts format
        total_shots = sum(counts.values())
        ones = sum(counts[k] for k in counts if isinstance(k, int) and k & 1)
        return ones / total_shots

# In your main function
def main():
    # Create sample data
    num_samples = 10
    training_data = np.random.rand(num_samples, 4) * 2 * np.pi
    labels = np.random.randint(0, 2, num_samples)
    
    qnn = QASMNeuralNetwork()
    trained_parameters = qnn.train_network(training_data, labels)
    
    # Test the trained network
    test_data = np.random.rand(4) * 2 * np.pi
    test_circuit = qnn.create_quantum_circuit(test_data, trained_parameters)
    
    # New way to execute test circuit
    sampler = Sampler()
    result = sampler.run(test_circuit, shots=1000).result()
    counts = result.quasi_dists[0]
    prediction = qnn.calculate_output_probability(counts)
    
    print(f"\nTest prediction: {prediction}")
    print(f"Final parameters: {trained_parameters}")
    
    # Save the final QASM code
    final_circuit = qnn.create_quantum_circuit(test_data, trained_parameters)
    with open('trained_neural_network.qasm', 'w') as f:
        f.write(final_circuit.qasm())
    print("\nFinal QASM code saved to 'trained_neural_network.qasm'")
