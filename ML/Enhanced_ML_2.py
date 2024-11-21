from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.providers.aer import AerSimulator
from qiskit.providers.aer.noise import NoiseModel
from multiprocessing import Pool
import numpy as np
import time


class QASMNeuralNetwork:
    def __init__(self, num_qubits=4, num_classes=3, num_layers=2):
        if num_qubits < 1:
            raise ValueError("Number of qubits must be positive")
        if num_classes < 2:
            raise ValueError("Number of classes must be at least 2")
        
        self.num_qubits = num_qubits
        self.num_classes = num_classes
        self.num_parameters = num_qubits * num_layers
        self.num_layers = num_layers

        # Noise model for simulation
        self.noise_model = NoiseModel.from_backend(AerSimulator())
        self.simulator = AerSimulator(noise_model=self.noise_model)

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

        # Add variational layers
        for layer in range(self.num_layers):
            for i in range(self.num_qubits):
                qc.ry(parameters[layer * self.num_qubits + i], i)
            # Add all-to-all entanglement
            for i in range(self.num_qubits):
                for j in range(i + 1, self.num_qubits):
                    qc.cx(i, j)
        
        return qc

    def get_statevector(self, circuit):
        return Statevector.from_instruction(circuit)

    def calculate_probabilities(self, statevector):
        probabilities = statevector.probabilities()
        return probabilities[:self.num_classes]

    def calculate_fidelity(self, statevector, target_state):
        return statevector.overlap(target_state) ** 2

    def calculate_categorical_loss(self, pred_probs, label_vector):
        pred_probs = np.clip(pred_probs, 1e-10, 1.0)
        return -np.sum(label_vector * np.log(pred_probs))

    def calculate_gradient(self, args):
        input_data, parameters, label_vector, i, epsilon = args
        parameters_plus = parameters.copy()
        parameters_minus = parameters.copy()
        parameters_plus[i] += epsilon
        parameters_minus[i] -= epsilon
        
        circuit_plus = self.create_quantum_circuit(input_data, parameters_plus)
        statevector_plus = self.get_statevector(circuit_plus)
        prob_plus = self.calculate_probabilities(statevector_plus)
        
        circuit_minus = self.create_quantum_circuit(input_data, parameters_minus)
        statevector_minus = self.get_statevector(circuit_minus)
        prob_minus = self.calculate_probabilities(statevector_minus)
        
        gradient = (np.sum(prob_plus * label_vector) - np.sum(prob_minus * label_vector)) / (2 * epsilon)
        return gradient

    def train_network(self, training_data, labels, epochs=1000, learning_rate=0.01, epsilon=0.01):
        parameters = np.random.rand(self.num_parameters) * 2 * np.pi
        best_loss = float('inf')
        best_parameters = None
        start_time = time.time()
        
        for epoch in range(epochs):
            total_loss = 0
            for data, label in zip(training_data, labels):
                # Forward pass
                circuit = self.create_quantum_circuit(data, parameters)
                statevector = self.get_statevector(circuit)
                output_probs = self.calculate_probabilities(statevector)

                # Calculate loss
                loss = self.calculate_categorical_loss(output_probs, label)
                total_loss += loss

                # Calculate gradients in parallel
                with Pool() as pool:
                    gradients = pool.map(
                        self.calculate_gradient,
                        [(data, parameters, label, i, epsilon) for i in range(len(parameters))]
                    )
                gradients = np.array(gradients)
                parameters -= learning_rate * gradients
            
            avg_loss = total_loss / len(training_data)
            if avg_loss < best_loss:
                best_loss = avg_loss
                best_parameters = parameters.copy()
            
            if epoch % 100 == 0:
                elapsed_time = time.time() - start_time
                print(f"Epoch {epoch}, Loss: {avg_loss:.6f}, Best Loss: {best_loss:.6f}, Elapsed Time: {elapsed_time:.2f}s")
        
        return best_parameters


def normalize_and_scale(data):
    normalized_data = (data - np.min(data)) / (np.max(data) - np.min(data))
    scaled_data = normalized_data * (2 * np.pi)
    return scaled_data


def main():
    np.random.seed(42)

    num_samples = 10
    num_classes = 3
    input_features = 4
    
    training_data = np.random.rand(num_samples, input_features)
    labels = np.random.randint(0, num_classes, num_samples)
    one_hot_labels = np.eye(num_classes)[labels]
    training_data = normalize_and_scale(training_data)

    qnn = QASMNeuralNetwork(num_qubits=input_features, num_classes=num_classes, num_layers=2)
    trained_parameters = qnn.train_network(training_data, one_hot_labels, epochs=1000)

    # Test the network
    test_data = normalize_and_scale(np.random.rand(input_features))
    test_circuit = qnn.create_quantum_circuit(test_data, trained_parameters)
    test_statevector = qnn.get_statevector(test_circuit)
    prediction = qnn.calculate_probabilities(test_statevector)
    print(f"Test prediction: {prediction}")

    # Save the final QASM code
    final_circuit = qnn.create_quantum_circuit(test_data, trained_parameters)
    with open('trained_neural_network.qasm', 'w') as f:
        f.write(final_circuit.qasm())
    print("QASM saved successfully!")


if __name__ == "__main__":
    main()
