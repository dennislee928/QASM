from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np
import time

class QASMNeuralNetwork:
    def __init__(self, num_qubits=4, num_classes=3):
        if num_qubits < 1:
            raise ValueError("Number of qubits must be positive")
        if num_classes < 2:
            raise ValueError("Number of classes must be at least 2")
        
        self.num_qubits = num_qubits
        self.num_parameters = num_qubits

    def validate_input_data(self, input_data):
        if not isinstance(input_data, np.ndarray):
            input_data = np.array(input_data)
        
        if input_data.ndim != 1:
            raise ValueError("Input data must be 1-dimensional")
        
        if len(input_data) > self.num_qubits:
            raise ValueError(f"Input data length ({len(input_data)}) exceeds number of qubits ({self.num_qubits})")
        
        return input_data

    def create_quantum_circuit(self, input_data, parameters):
        input_data = self.validate_input_data(input_data)
        qc = QuantumCircuit(self.num_qubits)
        
        # Encode input data using rotation gates
        for i, data in enumerate(input_data):
            qc.rx(data, i)
        
        # Add trainable parameters using rotation gates
        for i, param in enumerate(parameters):
            qc.ry(param, i)
        
        # Add entanglement layers
        for i in range(self.num_qubits - 1):
            qc.cx(i, i + 1)
        qc.cx(self.num_qubits - 1, 0)
        
        return qc

    def get_statevector(self, circuit):
        return Statevector.from_instruction(circuit)

    def calculate_probabilities(self, statevector, num_classes):
        probabilities = []
        for i in range(num_classes):
            prob = statevector.probabilities([i])[1] if i < self.num_qubits else 0
            probabilities.append(max(prob, 1e-10))
        return np.array(probabilities)

    def calculate_categorical_loss(self, pred_probs, label_vector):
        if len(pred_probs) != len(label_vector):
            raise ValueError(f"Shape mismatch: pred_probs has shape {len(pred_probs)}, but label_vector has shape {len(label_vector)}")
        
        pred_probs = np.clip(pred_probs, 1e-10, 1.0)
        return -np.sum(label_vector * np.log(pred_probs))

    def calculate_gradient(self, input_data, parameters, label_vector):
        epsilon = 0.01
        gradient = np.zeros_like(parameters)
        
        for i in range(len(parameters)):
            parameters_plus = parameters.copy()
            parameters_minus = parameters.copy()
            parameters_plus[i] += epsilon
            parameters_minus[i] -= epsilon
            
            circuit_plus = self.create_quantum_circuit(input_data, parameters_plus)
            statevector_plus = self.get_statevector(circuit_plus)
            prob_plus = np.clip(self.calculate_probabilities(statevector_plus, len(label_vector)), 1e-10, 1-1e-10)
            
            circuit_minus = self.create_quantum_circuit(input_data, parameters_minus)
            statevector_minus = self.get_statevector(circuit_minus)
            prob_minus = np.clip(self.calculate_probabilities(statevector_minus, len(label_vector)), 1e-10, 1-1e-10)
            
            gradient[i] = (np.sum(prob_plus * label_vector) - np.sum(prob_minus * label_vector)) / (2 * epsilon)
        
        return gradient

    def train_network(self, training_data, labels, epochs=100000, num_classes=3):
        parameters = np.random.rand(self.num_parameters) * 2 * np.pi
        learning_rate = 0.01
        best_loss = float('inf')
        best_parameters = None
        start_time = time.time()
        
        try:
            for epoch in range(epochs):
                total_loss = 0
                for data, label in zip(training_data, labels):
                    # Forward pass
                    circuit = self.create_quantum_circuit(data, parameters)
                    statevector = self.get_statevector(circuit)
                    output_probs = self.calculate_probabilities(statevector, num_classes)
                    
                    output_probs = output_probs / np.sum(output_probs)
                    
                    # Calculate loss
                    loss = self.calculate_categorical_loss(output_probs, label)
                    total_loss += loss
                    
                    # Calculate gradient and update parameters
                    gradient = self.calculate_gradient(data, parameters, label)
                    parameters -= learning_rate * gradient
                
                avg_loss = total_loss/len(training_data)
                
                # Save best parameters
                if avg_loss < best_loss:
                    best_loss = avg_loss
                    best_parameters = parameters.copy()
                
                if epoch % 100 == 0:  # Print every 100 epochs
                    elapsed_time = time.time() - start_time
                    print(f"Epoch {epoch}/{epochs} ({epoch/epochs*100:.1f}%)")
                    print(f"Loss: {avg_loss:.6f}")
                    print(f"Best Loss: {best_loss:.6f}")
                    print(f"Time elapsed: {elapsed_time:.2f} seconds")
                    print(f"Estimated time remaining: {(elapsed_time/(epoch+1))*(epochs-epoch-1):.2f} seconds")
                    print("-" * 50)
                    
        except Exception as e:
            print(f"Error during training: {str(e)}")
            raise
        
        return best_parameters

def normalize_and_scale(data):
    normalized_data = (data - np.min(data)) / (np.max(data) - np.min(data))
    scaled_data = normalized_data * (2 * np.pi)
    return scaled_data

def main():
    np.random.seed(42)
    
    # Define parameters
    num_samples = 10
    num_classes = 3
    input_features = 4
    
    print("Initializing training data...")
    training_data = np.random.rand(num_samples, input_features)
    labels = np.random.randint(0, num_classes, num_samples)
    one_hot_labels = np.eye(num_classes)[labels]
    
    print("Normalizing and scaling data...")
    training_data = normalize_and_scale(training_data)
    
    print("\nInitial training data shape:", training_data.shape)
    print("Initial labels shape:", one_hot_labels.shape)
    
    print("\nStarting training...")
    qnn = QASMNeuralNetwork(num_qubits=input_features, num_classes=num_classes)
    
    start_time = time.time()
    trained_parameters = qnn.train_network(training_data, one_hot_labels, epochs=10000, num_classes=num_classes)
    total_time = time.time() - start_time
    
    print("\nTraining completed!")
    print(f"Total training time: {total_time:.2f} seconds")
    
    # Test the network
    print("\nTesting the network...")
    test_data = normalize_and_scale(np.random.rand(input_features))
    test_circuit = qnn.create_quantum_circuit(test_data, trained_parameters)
    test_statevector = qnn.get_statevector(test_circuit)
    prediction = qnn.calculate_probabilities(test_statevector, num_classes)
    
    print(f"\nTest input: {test_data}")
    print(f"Prediction probabilities: {prediction}")
    print(f"Predicted class: {np.argmax(prediction)}")
    print(f"Final parameters: {trained_parameters}")

    ##save qasm
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
    ##

if __name__ == "__main__":
    main()
