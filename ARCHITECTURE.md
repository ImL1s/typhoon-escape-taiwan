# 🏛️ 系統架構設計文件 (System Architecture)

> 《台灣大逃亡：颱風來啦！(Typhoon Escape Taiwan)》系統架構全景、子系統設計、數學幾何模型與軟體管線全解析。
> 官方 GitHub 專案倉庫：[https://github.com/ImL1s/typhoon-escape-taiwan](https://github.com/ImL1s/typhoon-escape-taiwan)

---

## 📑 目錄

1. [總體架構概覽 (High-Level Architecture)](#1-總體架構概覽-high-level-architecture)
2. [遊戲狀態機 (Game State Machine)](#2-遊戲狀態機-game-state-machine)
3. [座標變換與投影管線 (Coordinate Pipeline)](#3-座標變換與投影管線-coordinate-pipeline)
4. [實體拓撲與空間索引 (Entities & Spatial Indexing)](#4-實體拓撲與空間索引-entities-spatial-indexing)
5. [物理碰撞與板塊力學 (Physics & Mechanics)](#5-物理碰撞與板塊力學-physics-mechanics)
6. [中央山脈護國神山防衛子系統 (Mountain Defense System)](#6-中央山脈護國神山防衛子系統-mountain-defense-system)
7. [颱風生成與大氣環流引擎 (Atmospheric Engine)](#7-颱風生成與大氣環流引擎-atmospheric-engine)
8. [Web Audio 程序化聲學合成圖 (Audio Synthesis Graph)](#8-web-audio-程序化聲學合成圖-audio-synthesis-graph)
9. [渲染管線與雷達著色 (Rendering Pipeline)](#9-渲染管線與雷達著色-rendering-pipeline)
10. [事件監聽與輸入適配層 (Input Layer)](#10-事件監聽與輸入適配層-input-layer)
11. [自動化測試架構 (Test Framework)](#11-自動化測試架構-test-framework)

---

## 1. 總體架構概覽 (High-Level Architecture)

遊戲採用**單一獨立封裝無外部依賴 (Zero-Dependency Single-Bundle)** 架構，所有 HTML5、CSS3、ES6+ JavaScript、GeoJSON 地理多邊形資料及 Web Audio 合成代碼皆整合於單一檔案中。

```
+---------------------------------------------------------------------------------------+
|                                    index.html                                         |
+---------------------------------------------------------------------------------------+
|  [DOM & View Layer]                                                                   |
|   - #cv (HTML5 Canvas 2D)                                                             |
|   - #pad & #knob (Virtual Radar Joystick)                                             |
|   - #ticker (Real-time Meteorological Marquee)                                        |
|   - #popup (Start / Game Over / Victory Modal)                                         |
|   - #menu (Meteorological & Historical Guide)                                         |
|   - #githubbtn (GitHub Repository Direct Link)                                        |
+---------------------------------------------------------------------------------------+
|  [Game Core Loop & Engine]                                                            |
|                                                                                       |
|   +-------------------+      +--------------------+      +------------------------+   |
|   |  Input Processor  | ---> |   Physics & Land   | ---> |  Typhoon Atmospheric   |   |
|   | (Touch/Mouse/Key) |      | (Drift & Collision)|      |  (6 Paths + Fujiwhara) |   |
|   +-------------------+      +--------------------+      +------------------------+   |
|            |                           |                             |                |
|            v                           v                             v                |
|   +-------------------+      +--------------------+      +------------------------+   |
|   | State Controller  |      |  Mountain Defense  |      |   Procedural Audio     |   |
|   |  (FSM & Clock)    |      | (Circulation Shred)|      |   (Web Audio Synth)    |   |
|   +-------------------+      +--------------------+      +------------------------+   |
|                                        |                             |                |
|                                        +--------------+--------------+                |
|                                                       |                               |
|                                                       v                               |
|                                          +-------------------------+                  |
|                                          |   CWA Radar Renderer    |                  |
|                                          |  (Spiral Bands & Waves) |                  |
|                                          +-------------------------+                  |
+---------------------------------------------------------------------------------------+
|  [Embedded Geometry Data: <script id="mapdata">]                                      |
|   - tw: 9 Taiwan Island Rings (Mainland, Penghu, Green, Orchid, Xiaoliuqiu, Guishan)  |
|   - land: 135 East Asia Mainland & Regional Polygons                                  |
+---------------------------------------------------------------------------------------+
```

---

## 2. 遊戲狀態機 (Game State Machine)

遊戲生命週期由明確的有限狀態機 (FSM) 驅動：

```
                    ┌─────────────────────────┐
                    │      INITIALIZING       │
                    │   (Decode JSON & Map)   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
          ┌─────────│        TITLE / IDLE     │
          │         │    (Display Intro Card) │
          │         └────────────┬────────────┘
          │                      │ [User Click / Space]
          │                      ▼
          │         ┌─────────────────────────┐
          │         │         PLAYING         │◄─────────┐
          │         │ (Physics, Audio, Time)  │          │
          │         └────────────┬────────────┘          │
          │          [P / Space] │                       │ [P / Space]
          │                      ▼                       │
          │         ┌─────────────────────────┐          │
          │         │         PAUSED          │──────────┘
          │         │  (Halt Time & Physics)  │
          │         └─────────────────────────┘
          │                      │
          │                      │ [Eye-Wall Landfall Hit]
          │                      ▼
          │         ┌─────────────────────────┐
          │         │        GAME OVER        │
          │         │ (Landmark & Score Card) │
          │         └────────────┬────────────┘
          │                      │
          └──────────────────────┴── [Restart Button / Space]
```

- **TITLE / IDLE：** 地圖預渲染完成，海風輕拂，等待舵手點擊出航。
- **PLAYING：** 物理時鐘以 $60\text{ FPS}$ 推進，颱風依時間隨機生成，海風合成音隨颱風逼近實時增大。
- **PAUSED：** 保留畫面上所有颱風旋轉角度與島嶼座標，停止實體位移，切換 ⏸️/▶️ 圖示。
- **GAME OVER：** 觸發登陸雷暴衝擊音，鎖定戰績（存活天數、閃避颱風數、登陸地標、榮譽稱號），彈出社群分享面板。

---

## 3. 座標變換與投影管線 (Coordinate Pipeline)

遊戲處理三套主要空間座標系：

1. **地理球座標 $(\lambda, \phi)$：** WGS84 經緯度（單位：度）。
2. **標準麥卡托投影平面 $(X_m, Y_m)$：**
   $$X_m = \lambda \cdot \frac{\pi}{180}$$
   $$Y_m = \ln\left(\tan\left(\frac{\pi}{4} + \frac{\phi \cdot \pi}{360}\right)\right)$$
3. **螢幕畫布像素座標 $(x_{px}, y_{px})$：**
   $$x_{px} = \frac{W}{2} + (\text{wrap}(\lambda) - \text{CEN}) \cdot \frac{W}{\text{LONW}}$$
   $$y_{px} = \frac{\text{MY} - Y_m}{\text{MY} - \text{MN}} \cdot H$$

```
   地理經緯度 [lon, lat]
            │
            ▼
   1:1 等角麥卡托投影 [px(lon), py(lat)]
            │
            ▼
   島嶼錨點相對偏移 [(px - CX) * 1.35, (py - CY) * 1.35]
            │
            ▼
   玩家即時操控位置 [twPos.x + pt.ox, twPos.y + pt.oy]
```

- **視窗基準常數：**
  - 中心經度 $\text{CEN} = 123.8^\circ\text{E}$
  - 經度顯示跨度 $\text{LONW} = 22.0^\circ$
  - 基準緯度 $\phi_0 = 23.6^\circ\text{N}$（等角修正因子 $\text{Aspect} \approx 1.091$）
  - 台灣島群微幅縮放倍率 $K = 1.35$（確保手機小螢幕上兼具視覺清晰度與微操空間）

---

## 4. 實體拓撲與空間索引 (Entities & Spatial Indexing)

### 4.1 台灣本島與群島實體 (`twRings` & `twPts`)
- 包含 9 個閉合幾何環，共 562 個幾何頂點。
- 每個頂點結構：`[dx, dy, origLon, origLat]`，其中 `dx, dy` 為相對於台灣質量中心 $(\text{CX}, \text{CY})$ 的像素偏移。

### 4.2 東亞周邊陸塊實體 (`bodies`)
- 提取自 Natural Earth 50m 解析度之東亞大陸、中南半島、菲律賓群島、琉球群島共 135 個多邊形。
- 每個陸塊快取其空間包圍盒：
  `{ outer: [[x, y], ...], minX, minY, maxX, maxY, ox: 0, oy: 0, vx: 0, vy: 0 }`

### 4.3 空間過濾優化 (AABB Culling)
在進行高精度的點-多邊形碰撞檢測前，先執行外接矩形邊界相交檢定：
```javascript
if (twPos.x + 120 < B.minX + B.ox || twPos.x - 120 > B.maxX + B.ox ||
    twPos.y + 120 < B.minY + B.oy || twPos.y - 120 > B.maxY + B.oy) {
  continue; // 距離過遠，略過多邊形頂點射線檢驗
}
```
此優化使單幀碰撞檢驗開銷自 $O(N_{\text{tw}} \times N_{\text{land}}) \approx 2 \times 10^6$ 次降低至數十次計算以內。

---

## 5. 物理碰撞與板塊力學 (Physics & Mechanics)

### 5.1 射線交叉法判定 (Ray Casting Algorithm)
```javascript
function inPoly(pt, ring) {
  var x = pt[0], y = pt[1], inside = false;
  for (var i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    var xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1];
    if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) {
      inside = !inside;
    }
  }
  return inside;
}
```

### 5.2 大陸板塊推擠與滑動 (`pushLand` & `slideLand`)
當台灣島撞上周邊陸塊時，計算重疊點之平均法線推力向量，並施加慣性脈衝：
$$\vec{v}_{\text{body}} = \frac{\sum \vec{p}_{\text{overlap}}}{\|\sum \vec{p}_{\text{overlap}}\|} \cdot (M \times 0.125)$$
滑動時套用指數阻尼衰減：
$$\vec{v}_{t+\Delta t} = \vec{v}_t \cdot 0.12^{\Delta t}$$
當速度低於 $0.5\text{ px/s}$ 時強制歸零，杜絕數值抖動。

---

## 6. 中央山脈護國神山防衛子系統 (Mountain Defense System)

### 6.1 主脊骨幹頂點取樣 (Spine Vertebrae)
在台灣地理主脊樑取樣 16 個座標控制點，構建中央山脈屏障骨架：
$$\text{Spine} = \{P_1(121.85^\circ, 24.95^\circ), \dots, P_{16}(120.85^\circ, 21.90^\circ)\}$$

### 6.2 削弱動力學方程
每一幀計算颱風中心 $(\text{tx}, \text{ty})$ 與山脈主脊的最短距離 $d_{\text{min}}$：
$$\text{If } d_{\text{min}} < 1.05 \cdot r_{\text{typhoon}}:$$
$$r_{\text{typhoon}} \leftarrow r_{\text{typhoon}} - r_{\text{peak}} \cdot 0.35 \cdot \Delta t$$
- 暴風半徑在山脈摩擦下迅速萎縮。
- 同步發射 8~12 顆碧藍能量粒子：
  $$\vec{v}_{\text{particle}} = [\cos(\theta), \sin(\theta)] \cdot \text{rand}(40, 110)$$
- 累積接觸時間 $\tau_{\text{hit}} \ge 0.35\text{s}$ 時，觸發中央山脈特報廣播並播放程序合成音。

---

## 7. 颱風生成與大氣環流引擎 (Atmospheric Engine)

### 7.1 六大路徑參數特徵矩陣
```javascript
const PATTERNS = [
  { name: '直撲穿心', segMin: 3.5, segMax: 6.0, jitter: 0.25, pull: 0.45, spd: 1.25, stall: 0.00, bias:  0.00, tag: '穿心直撲' },
  { name: '西北颱',   segMin: 3.0, segMax: 5.5, jitter: 0.20, pull: 0.25, spd: 1.15, stall: 0.00, bias: -0.35, tag: '西北颱' },
  { name: '迷走怪颱', segMin: 0.8, segMax: 1.8, jitter: 2.20, pull: 0.25, spd: 0.85, stall: 0.35, bias:  0.00, tag: '迷走打轉' },
  { name: '追尾鎖定', segMin: 1.5, segMax: 3.0, jitter: 0.50, pull: 0.85, spd: 0.95, stall: 0.00, bias:  0.00, tag: '追尾鎖定' },
  { name: '鞍形停滯', segMin: 2.0, segMax: 4.0, jitter: 0.80, pull: 0.30, spd: 0.50, stall: 0.60, bias:  0.00, tag: '鞍形場停滯' },
  { name: '急折轉向', segMin: 2.0, segMax: 3.5, jitter: 0.30, pull: 0.20, spd: 1.10, stall: 0.00, bias:  0.65, tag: '拋物轉向' }
];
```

### 7.2 藤原效應雙颱互繞力學 (Binary Vortex Interaction)
當雙颱距離 $15\text{px} < d < 160\text{px}$ 時：
$$\theta_{12} = \text{atan2}(y_2 - y_1, x_2 - x_1)$$
$$\text{Force} = \left(\frac{160 - d}{160}\right) \cdot 0.7 \cdot \Delta t \cdot 55$$
颱風 1 沿 $\theta_{12} + \frac{\pi}{2}$ 方向公轉，颱風 2 沿 $\theta_{12} - \frac{\pi}{2}$ 方向公轉。

---

## 8. Web Audio 程序化聲學合成圖 (Audio Synthesis Graph)

```
[Pink Noise Generator] ──> [BiquadFilter (Bandpass 450Hz)] ──> [WindGain (Distance Modulated)] ──┐
                                                                                                 │
[Dual Oscillator (Triangle)] ──> [Pitch Sweep (460->780Hz)] ──> [SirenGain] ────────────────────┼──> [Master Gain] ──> [Destination]
                                                                                                 │
[Harmonic Sine Array] ───> [High-Pass Filter] ───────────────> [MountainShieldGain] ─────────────┤
                                                                                                 │
[White Noise Blast] ─────> [BiquadFilter (Lowpass 200Hz)] ───> [ExplosionGain (Exp Decay)] ──────┘
```

- **海風暴風背景音：** 5 秒立體聲粉紅噪音環，每幀計算 $d_{\text{closest}}$，動態將增益調諧在 $0.05 \sim 0.35$。
- **警報音：** 音頻參數利用 `exponentialRampToValueAtTime` 進行精確至毫秒級的音調滑動。

---

## 9. 渲染管線與雷達著色 (Rendering Pipeline)

每幀繪製遵循分層次序：
1. **背景海域清屏：** 繪製深海靛藍底色 `#1B2F5E`。
2. **經緯度網格：** 繪製淡藍色麥卡托參考經緯線。
3. **周邊歐亞大陸與島嶼：** 填充墨藍色陸塊 `#0B1B3D` 並描畫高對比海岸線。
4. **颱風 72 小時潛勢預報錐：** 半透明白色漏斗狀機率預報虛線。
5. **颱風動態雷達回波螺旋雨帶：** 
   - 旋轉畫布座標系 `ctx.rotate(rot)`。
   - 繪製 5 階七彩漸層螺旋弧線（綠 ➔ 黃 ➔ 橘 ➔ 紅 ➔ 紫）。
   - 繪製外圍 7 級風虛線警戒圈與內圍 10 級風實線暴風圈。
6. **中央山脈防禦光束與粒子：** 藍綠色高斯發光結界與玉山頂點脈衝。
7. **台灣本島及 8 大離島群：** 填充翡翠綠 `#2E7D32`，內部繪製中央山脈脊樑金色實線與頂峰標記。
8. **UI 與 HUD 疊加層：** 虛擬方向舵、頂部狀態標題、底部動態跑馬燈。

---

## 10. 事件監聽與輸入適配層 (Input Layer)

- **Touch Events (`touchstart`, `touchmove`, `touchend`)：**
  - 支援全螢幕直覺拖曳導航。
  - 左下角虛擬搖桿支援動態觸控中心捕捉與極限半徑約束 ($R_{\text{max}} = 38\text{px}$)。
- **Mouse Events (`mousedown`, `mousemove`, `mouseup`)：**
  - 滑鼠左鍵按住拖曳模擬觸控。
- **Keyboard Events (`keydown`, `keyup`)：**
  - `KeyW`, `KeyS`, `KeyA`, `KeyD`, `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`。
  - `Space`：開始遊戲／暫停／重新開始。
  - `KeyP`：切換暫停狀態。

---

## 11. 自動化測試架構 (Test Framework)

專案配備了基於 Node.js 的全自動化引擎驗證腳本 [test_game_engine.js](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/test_game_engine.js)：

```bash
node test_game_engine.js
```

測試矩陣包含 7 大核心面向：
1. **檔案結構與標籤完整性：** 驗證 DOM 節點、地圖 JSON 結構（9 島嶼環、>50 陸塊多邊形）。
2. **1:1 等角麥卡托數學幾何驗證：** 斷言 $X/Y$ 像素比率與 $\frac{1}{\cos(23.6^\circ)}$ 誤差小於 $5\%$。
3. **初始碰撞與大陸漂移消除測試：** 驗證開局 60 幀內 0 碰撞、0 漂移位移。
4. **21 個沿海地理地標分類器全覆蓋測試：** 100% 準確率斷言。
5. **中央山脈削弱防衛機制驗證：** 斷言擦邊時暴風半徑自 42px 縮小至 34.7px，且警報成功觸發。
6. **颱風 1,000 幀物理模擬與藤原效應測試：** 斷言無 NaN 座標、無內存洩漏，生成與消散生命週期正常。
7. **重新開始狀態乾淨重設與分享連結測試：** 驗證 DOM 狀態、統計欄位重設及社群意圖 URL 格式。
