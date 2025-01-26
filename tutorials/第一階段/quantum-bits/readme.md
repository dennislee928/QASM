# 量子計算的基本概念

量子計算並非傳統意義上的計算，而是利用量子力學的原理來解決問題。其目標是設計出能夠根據量子力學定律運作，並適用於解決多種問題的組件。量子電腦基於量子物體，這些物體易於測量和操控。

## 量子位元（Qubit）

- 量子位元是量子資訊的基本單位，類似於傳統電腦的位元（bit）。
- 量子位元可以處於疊加態（superposition），即同時存在於多個狀態的組合。
  - 疊加態表示為 ∣ψ⟩=a∣0⟩+b∣1⟩，其中 a 和 b 是複數係數。
  - 係數的相對大小決定了測量到每個狀態的機率。
  - 測量會使量子位元坍縮為一個確定的狀態 ∣0⟩ 或 ∣1⟩。
- 量子位元的物理實現包括自旋粒子、偏振光子和量子導線等。

## 量子位元的操作和測量

- 量子位元可以通過電脈衝或光照等方式從一個狀態翻轉到另一個狀態。
- 測量是機率性的，無法準確預測結果。
  - 例如，狀態 ∣ψ⟩=0.1∣0⟩+0.995∣1⟩ 中，測量到 ∣0⟩ 的機率為 1%，而 ∣1⟩ 為 99%。

## 量子計算的應用

- 潛在應用包括密碼學、量子化學、藥物開發、材料科學、優化問題和通訊。
- 量子電腦能夠處理傳統電腦難以解決的問題。
- 課程中使用的程式語言為 Q#,openQASM,Qiskit。

## 量子計算的挑戰

- 挑戰在於如何操控量子位元，並在不失去量子疊加態的複雜性的情況下進行計算。
- 單次測量通常不足以確定量子位元的狀態組成。
- 測量會改變量子位元的狀態，使資訊丟失。

# IBM quantum composer-
https://quantum.ibm.com/composer

# 程式碼視覺化呈現（可實際運算）

![Screenshot 2025-01-26 at 9 42 00 PM](https://github.com/user-attachments/assets/7a7cd37f-1e91-4ed9-90d4-e8fb16a78090)


# 執行程式碼
![Screenshot 2025-01-26 at 9 43 17 PM](https://github.com/user-attachments/assets/3d714702-0547-48ca-851c-902f256cc41a)

# 程式碼執行中
![Screenshot 2025-01-26 at 9 44 43 PM](https://github.com/user-attachments/assets/5b21e5eb-1399-4373-9b20-c550761dbd82)

# 程式碼執行結果
![Screenshot 2025-01-26 at 9 46 09 PM](https://github.com/user-attachments/assets/c4a7f40e-96fb-4821-89ad-482826d7091d)


- ref: https://brilliant.org/courses/quantum-computing/introduction-108/quantum-bits-2/up-next/
