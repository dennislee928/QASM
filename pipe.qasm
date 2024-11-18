OPENQASM 2.0;
include "qelib1.inc";

// Define quantum and classical registers
qreg plane[3];    // 3 qubits to represent flight states
creg status[3];   // Classical bits to store measurement

// Initialize plane in ground state (000 = parked)
reset plane[0];
reset plane[1];
reset plane[2];

// Takeoff sequence
// Transition from parked to taxiing
x plane[0];       // 001 = taxiing

// Transition to takeoff roll
x plane[1];       // 011 = takeoff roll

// Transition to airborne
x plane[2];       // 111 = airborne
x plane[0];       // Reset first bit
x plane[1];       // Reset second bit
                  // 100 = cruising altitude

// Begin landing sequence
x plane[1];       // 110 = descent

// Final approach
x plane[0];       // 111 = final approach

// Touchdown
x plane[2];       // 011 = landing roll

// Return to taxiing
x plane[1];       // 001 = taxiing

// Park at gate
x plane[0];       // 000 = parked

// Measure final state
measure plane -> status;
