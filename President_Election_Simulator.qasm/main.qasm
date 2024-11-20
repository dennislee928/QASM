OPENQASM 2.0;
include "qelib1.inc";

qreg voter_groups[20];   // 20 qubits represent 2^20 (~1,048,576) states. Each state corresponds to ~21.9 voters.

creg results[20];//store qreg
h voter_groups;  // Superposition for group-based voting choices
measure voter_groups -> results;


