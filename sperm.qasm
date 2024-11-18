OPENQASM 2.0;
include "qelib1.inc";
//
qreg milk_owner_ship[3];  // Milk owner_ship state: right_owner(0), thief_owner(1), retailors(2), 
qreg milk_geo_location[2];  // Milk geo_location state: refri(0), not_in_refr(1) .
qreg sperm_status[2];  // sperm state: in_milk(0), not_in_milk(1) .
//classical register
creg measurement_milk_owner_ship[3]
creg measurement_geo_location[3]
creg measurement_sperm_status[3]