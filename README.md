# QASM

## 專案簡介
本專案收錄 OpenQASM 2.0 量子電路教學範例與本機模擬練習，主題包含 superposition、entanglement、phase 與 measurement basis 等基本概念。

本模擬以「日常規律事件是否準時發生」為教學情境，示範如何把二元事件編碼為量子電路輸入；情境為虛構，不指涉任何真實人物。

## 範例輸出說明
本範例使用隨機合成資料，輸出僅供教學示範，不代表任何真實人物或行為的機率估計；機率值應介於 [0, 1]。

此為教學 demo，未經校準與驗證，不適用於預測真實個人行為；調整 qubit 狀態數、解讀方式與閾值等參數僅供課堂練習比較。

範例輸出（合成示意）：電路執行後之量測分布，數據為教學範例。

## 範例目錄

| 路徑 | 主題 | 說明 |
|---|---|---|
| `daily_schedule_estimation/` | 二元事件教學範例 | 以隨機合成資料示範電路建立與本機模擬，輸出不代表真實人物 |
| `ML/` | Quantum ML 教學範例 | rotation、entanglement 與參數更新的課堂練習 |
| `daily_life_simulation/` | Superposition 概念 | 以 Hadamard 閘示範疊加態 |
| `tutorials/` | 量子位元入門 | qubit、superposition 與量測概念說明 |
| `*.qasm`（根目錄） | OpenQASM 練習 | 各主題的獨立電路範例 |

## 如何執行（本機模擬）

```bash
pip install qiskit numpy
python daily_schedule_estimation/main.py
```

OpenQASM 範例可載入本機 QASM simulator 執行；執行環境與套件版本以各子目錄說明為準。

## 限制與免責

- 本 repo 為教學 demo，未經校準與驗證，不適用於預測真實個人行為。
- 範例使用隨機合成資料時，輸出僅供教學示範，機率值應介於 [0, 1]。
- 目前未驗證 IBM Quantum 硬體／Lab 部署；workflow 狀態以最近一次 run 為準。

## 技術

<img src="https://img.shields.io/badge/PYTHON-black?style=for-the-badge&logo=python&logoColor=gold"/>
<img src="https://img.shields.io/badge/numpy-black?style=for-the-badge&logo=numpy&logoColor=white"/>
<img src="https://img.shields.io/badge/QISKIT-black?style=for-the-badge&logo=qiskit&logoColor=white"/>
