// OpenQASM 2.0 格式
OPENQASM 2.0;
include "qelib1.inc";

// 定義 6 個 qubit 和 6 個 classical bits 來儲存測量結果(register)
qreg q[4];
creg c[4];

// 狀態初始化（用 H gate，使 qubit 處於superposition）
h q[0];
h q[1];
h q[2];
h q[3];



// 使用旋轉gate RY 來表示不同交通工具/機器人的方位行動
// 這裡直接使用具體角度來展示（可由強化學習做動態調整，要外接python）
ry(0.5) q[0];  // 行動 1，向前
ry(1.0) q[1];  // 行動 2，向後
ry(1.5) q[2];  // 行動 3，向左
ry(2.0)   q[3];  // 行動 4，向右

// 增加量子糾纏，用於加強4種行動之間的依賴和關聯性
cx q[0], q[1];
cx q[0], q[2];
cx q[0], q[3];
cx q[1], q[2];
cx q[1], q[3];
cx q[2], q[3];
cx q[1], q[3];

// 對 qubit 進行測量並儲存結果到 classical bits
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];

