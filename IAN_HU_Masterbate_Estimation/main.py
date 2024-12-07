from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Statevector
from qiskit.circuit import Parameter
import numpy as np
import pytz
from datetime import datetime, timedelta

class QASMNeuralNetwork:
    def __init__(self):
        self.num_qubits = 5  # Extra qubit for task-specific context
        self.num_parameters = 4  # Additional parameter for task-specific learning

    def create_quantum_circuit(self, input_data, parameters):
        qc = QuantumCircuit(self.num_qubits)
        
        # Encode input data using rotation gates
        for i, data in enumerate(input_data):
            qc.rx(data, i)
        
        # Add trainable parameters using rotation gates
        for i in range(len(parameters)):
            qc.ry(parameters[i], i)
        
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

    def train_network(self, training_data, labels, epochs=500):
        parameters = np.random.rand(self.num_parameters) * 2 * np.pi
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
            
            if epoch % 100 == 0:
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

def get_current_time_in_taipei():
    taipei_tz = pytz.timezone('Asia/Taipei')
    return datetime.now(taipei_tz).strftime("%Y-%m-%d %H:%M:%S")

def main():
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create sample data: 4 features (date type, mood, physical state, etc.)
    num_samples = 20
    training_data = np.random.rand(num_samples, 5) * 2 * np.pi  # Include task-specific input
    labels = np.random.randint(0, 2, num_samples)  # Binary labels for task occurrence
    
    # Create and train the network
    qnn = QASMNeuralNetwork()
    trained_parameters = qnn.train_network(training_data, labels, epochs=500)
    
    # Test the trained network
    test_data = np.random.rand(5) * 2 * np.pi
    test_circuit = qnn.create_quantum_circuit(test_data, trained_parameters)
    test_statevector = qnn.get_statevector(test_circuit)
    prediction = qnn.calculate_probability(test_statevector)
    
    print(f"\nCurrent time in Taipei: {get_current_time_in_taipei()}")
    print(f"Test prediction (task probability): {prediction}")
    print(f"Final parameters: {trained_parameters}")
    
    # Save the final QASM code
    final_circuit = qnn.create_quantum_circuit(test_data, trained_parameters)
    try:
        qasm_str = final_circuit.qasm()
    except AttributeError:
        print("Warning: Could not generate QASM string.")
        qasm_str = str(final_circuit)
    
    with open('Ian_Hu_Masterbate_On_7A.M_Daily_Schedule_Estimation_Network.qasm', 'w') as f:
        f.write(qasm_str)
    print("\nFinal circuit representation saved to 'task_schedule_network.qasm'")

if __name__ == "__main__":
    main()
