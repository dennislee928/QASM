OPENQASM 2.0;
include "qelib1.inc";
//
qreg milk_owner_ship[2];  // Milk owner_ship state: right_owner(0), thief_owner(1), 
qreg milk_geo_location[2];  // Milk geo_location state: refri(0), not_in_refr(1) .
qreg sperm_status[2];  // sperm state: in_milk(0), not_in_milk(1) .
//classical register
creg measurement_milk_owner_ship[3]
creg measurement_geo_location[2]
creg measurement_sperm_status[2]
// Initialize all registers
reset milk_owner_ship;
reset milk_geo_location;
reset sperm_status;
// Simulate milk milk_owner_ship uncertainty
h milk_owner_ship[0];
cx milk_geo_location[0],sperm_status[0];
h milk_owner_ship[1];
cx milk_geo_location[1],sperm_status[1];
//
measure milk_owner_ship -> measurement_milk_owner_ship;
measure milk_geo_location -> measurement_geo_location;
measure sperm_status -> measurement_sperm_status;





