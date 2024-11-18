OPENQASM 2.0;
include "qelib1.inc";

// Define quantum and classical registers
// 定義所有qu和傳統的暫存器
qreg plane[3];      // Flight state (parked, taxiing, etc.)
//飛行的狀態：停在停機坪、滑行、飛行...其他
qreg altitude[3];   // 8 altitude levels (000 = ground, 111 = max altitude)
//高度狀態，共8個，0為在地上，8在最高可承受高度
qreg speed[3];      // 8 speed levels
qreg heading[4];    // 16 possible heading directions
qreg weather[2];    // Weather conditions (00=clear, 01=rain, 10=storm, 11=severe)
qreg delay[2];      // For timing simulation
qreg flying_goblins[2];      // For timing simulation(00=not measurements, 01=meet but only seen, 10=contacted and good goblins, 11=contacted and bad goblins)
//遇到飛行妖精的情況：0-沒遇到,1-遇到但只有看到,2-有接觸，為田中太郎（好的外星人『大概』）,3-有接觸，為佛力札（超壞外星人）
qreg goblin_safety[1];  //遇到佛力札的處理方式
//Define classical registers
creg status[3];     // Classical bits for flight state measurement
creg alt_status[3]; // Altitude measurement
creg spd_status[3]; // Speed measurement
creg hdg_status[4]; // Heading measurement
creg wx_status[2];  // Weather status
creg flying_goblins_status[2];  // flying_goblins status
//遇到佛力札的狀況
creg c_goblin_safety[1]; 

// Initialize all registers to ground state
reset plane;
reset altitude;
reset speed;
reset heading;
reset weather;
reset delay;
reset flying_goblins;
reset goblin_safety;

// Simulate flying_goblins uncertainty using superposition
// Create superposition for flying_goblins
//起飛前先確定全球飛行妖精狀況
h flying_goblins[0];
h flying_goblins[1];

// Simulate weather uncertainty using superposition
// Create superposition for weather conditions
h weather[0];
h weather[1];

// Initialize takeoff sequence
// Parked -> Taxiing
x plane[0];       // 001 = taxiing

// Simulate delay using quantum operations
h delay;
barrier delay;    // Force delay in execution

// Check weather conditions before takeoff
measure weather -> wx_status;
if(wx_status==2) goto end;  // Abort if stormy

// Takeoff roll with speed increase
x plane[1];       // 011 = takeoff roll
x speed[0];       // Begin speed increase
x speed[1];       // Continue acceleration

// Create superposition for altitude gain uncertainty
h altitude[0];
h altitude[1];

// Transition to airborne with altitude gain
x plane[2];       // 111 = airborne
x altitude[0];    // Begin altitude increase
x altitude[1];    // Continue climb

// Cruising altitude and speed
x plane[0];       // Reset first bit
x plane[1];       // 100 = cruising
x altitude[2];    // Maximum altitude
x speed[2];       // Cruising speed

// Apply heading changes using superposition
h heading[0];     // Create uncertainty in heading
h heading[1];     // Multiple possible flight paths

// Begin descent - gradual altitude and speed reduction
x plane[1];       // 110 = descent
x altitude[2];    // Reduce altitude
x speed[2];       // Reduce speed

// Weather check for landing
measure weather -> wx_status;
if(wx_status==3) goto holding_pattern;  // Severe weather diversion

// Final approach
x plane[0];       // 111 = final approach
x altitude[1];    // Continue altitude reduction
x speed[1];       // Further speed reduction

// Check flying_goblins before it is too late
//飛機落地前先確定有沒有碰到佛力札
measure flying_goblins -> flying_goblins_status;
if(flying_goblins_status==2) goto alarm;    // The plane met Frieza
//碰到佛力札，要找悟空
if(flying_goblins_status==3) goto oldhigh;  // The plane met ET, Tell 老高
//碰到田中太郎，要跟老高說
if(flying_goblins_status==1) goto oldhigh;  // The plane saw ET, Tell 老高
//看到田中太郎，要跟老高說

// Touchdown
x plane[2];       // 011 = landing roll
x altitude[0];    // Ground level
x speed[0];       // Landing speed

// Return to taxiing with final speed reduction
x plane[1];       // 001 = taxiing
x speed[0];       // Minimum speed

// Park at gate
x plane[0];       // 000 = parked

// Measure final states
measure plane -> status;
measure altitude -> alt_status;
measure speed -> spd_status;
measure heading -> hdg_status;

// Holding pattern sequence (jumped to if weather/flying_goblins is severe)
holding_pattern:
h heading;        // Uncertain heading during holding
x altitude[1];    // Maintain safe altitude
x speed[1];       // Holding pattern speed
barrier delay;    // Force delay
measure heading -> hdg_status;
measure altitude -> alt_status;
measure speed -> spd_status;
goto end;

alarm:
x goblin_safety[0];          // Set alarm state
measure goblin_safety[0] -> c_goblin_safety[0];
goto end;

oldhigh:         // tell old high
h goblin_safety[0];          // Set oldhigh state
measure goblin_safety[0] -> c_goblin_safety[0];
goto end;

end:
measure weather -> wx_status;
measure delay -> wx_status;
measure flying_goblins -> flying_goblins_status;