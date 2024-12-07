from qiskit import QuantumCircuit

# Create a quantum circuit
qc = QuantumCircuit(5, 1)  # 5 features, 1 output

# Add gates based on model logic
qc.h(0)  # Holiday
qc.x(1)  # Weekend
qc.rz(3.14 / 2, 2)  # Mood
qc.ry(3.14 / 4, 3)  # Stress level
qc.cx(3, 4)  # Physical interaction

# Measurement
qc.measure(4, 0)

# Save to QASM
qasm_code = qc.qasm()
with open("task_schedule.qasm", "w") as file:
    file.write(qasm_code)
