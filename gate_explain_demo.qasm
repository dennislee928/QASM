OPENQASM 2.0;
include "qelib1.inc";
// Teaching demo: phase gates and measurement basis; it does not predict game outcomes.
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

// Phase gates change relative phase, not computational-basis measurement outcomes on their own.
// Without a later interference step (for example, additional Hadamard or controlled operations
// before measurement), a phase gate does not change the probability distribution of
// computational-basis measurements; the phases below are shown for teaching notation only.
t p1[0]; // T gate (pi/8 gate): applies a relative phase of e^(i*pi/4) around the Z axis.
tdg p2[0]; // T-dagger gate: inverse of T, applies a relative phase of e^(-i*pi/4).
s p3[0]; // S gate (phase gate): applies a relative phase of i.
sdg p4[0]; // S-dagger gate: inverse of S, applies a relative phase of -i.

// Measure the states
measure p1 -> c1;
measure p2 -> c2;
measure p3 -> c3;
measure p4 -> c4;