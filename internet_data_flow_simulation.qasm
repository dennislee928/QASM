OPENQASM 2.0;
include "qelib1.inc";//import library

// 量子存取單位和古典存取單位定義
qreg q[4]; // 4個qubit表示流量特徵
creg c[4]; // 4個bit，用於儲存測量結果

// ref狀態: 模擬正常網路流量的量子態（含糾纏、疊加等）
// 正常流量初始化，這裡使用Ha gate和CNOT gate創建疊加態
h q[0];
h q[1];
cx q[0], q[2]; // 讓正常流量中的兩個qubit做糾纏
cx q[1], q[3];

// 變分量子電路: 模擬不同參數化的惡意流量
// 根據測試流量調整gate的rotation
rx(0.5) q[0];
ry(0.8) q[1];
rz(0.6) q[2];
rx(0.4) q[3];

// 模擬網路流量交互作用
cx q[1], q[2];
cx q[0], q[3];

// 增加更多Gate rotation來代表不同的流量特徵
rz(0.9) q[0];
ry(0.7) q[1];
rx(0.2) q[2];
rz(0.3) q[3];

// 測量（坍陷）所有qubit
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
