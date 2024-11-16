OPENQASM 2.0;
include "qelib1.inc";
// Simulates 4 person palying black jack, and predict each winning prbabilities of these 4 individuals
// 1.Register for 4 players (2 qubits each to represent basic states)
qreg p1[2];
qreg p2[2];
qreg p3[2];
qreg p4[2];

// 2.Classical registers to measure results
creg c1[2];
creg c2[2];
creg c3[2];
creg c4[2];

// 3.Apply superposition to represent different possible card combinations
h p1[0];
h p1[1];
h p2[0];
h p2[1];
h p3[0];
h p3[1];
h p4[0];
h p4[1];

// Add some entanglement between players (representing shared cards/deck)
cx p1[0],p2[0];
cx p2[0],p3[0];
cx p3[0],p4[0];

// Add phase shifts to represent different winning probabilities
t p1[0]; //t p1[0]: The T gate (also known as π/8 gate),Rotates the qubit state by π/4 (45 degrees) around the Z-axis,Adds a phase of e^(iπ/4),This gives player 1 a specific phase shift that affects their probability distribution
tdg p2[0];//The T-dagger gate (inverse of T gate),Rotates the qubit state by -π/4 (-45 degrees) around the Z-axis,Adds a phase of e^(-iπ/4),Applied to player 2, giving them a different probability distribution
s p3[0];//S gate (also known as Phase gate)
sdg p4[0];//S-dagger gate (also known as Phase gate)

// Measure the states
measure p1 -> c1;
measure p2 -> c2;
measure p3 -> c3;
measure p4 -> c4;