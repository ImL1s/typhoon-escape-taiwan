# 🛠️ 開發者指引與維護手冊 (Developer Guide)

> 本文件提供《台灣大逃亡：颱風來啦！》專案的完整開發環境配置、本機預覽、自動化測試、地圖資料生成與調參指引。

---

## 📑 目錄

1. [開發環境準備](#1-開發環境準備)
2. [專案目錄結構詳解](#2-專案目錄結構詳解)
3. [啟動本機伺服器與雙版本對照](#3-啟動本機伺服器與雙版本對照)
4. [執行自動化測試與驗證套件](#4-執行自動化測試與驗證套件)
5. [地圖資料處理與建置管線 (build_game.py)](#5-地圖資料處理與建置管線-build_gamepy)
6. [遊戲核心物理與氣象參數微調手冊](#6-遊戲核心物理與氣象參數微調手冊)
7. [Web Audio 音效除錯與合成調整](#7-web-audio-音效除錯與合成調整)
8. [打包發布與單檔分發規範](#8-打包發布與單檔分發規範)

---

## 1. 開發環境準備

本專案堅持「**零構建複雜度、零外部 npm 依賴**」原則：
- **Node.js：** v18.0.0 以上（僅用於執行單元測試 `test_game_engine.js`）。
- **Python：** 3.8 以上（內建模組 `http.server`, `urllib` 用於預覽伺服器與地圖建置）。
- **網頁瀏覽器：** 支援 ES6+ 與 Web Audio API 的現代瀏覽器（Chrome 90+, Safari 15+, Edge 90+, Firefox 90+）。

### 複製專案庫 (Clone Repository)
```bash
git clone https://github.com/ImL1s/typhoon-escape-taiwan.git
cd typhoon-escape-taiwan
```

---

## 2. 專案目錄結構詳解

```
~/Documents/mine/typhoon-escape-taiwan/
├── index.html                           # 🇹🇼 台灣大逃亡遊戲本體（單檔發布版，內嵌地圖、音效與雷達）
├── server.py                            # 輕量級 Python 本地預覽伺服器（雙版本入口）
├── map_data.json                        # 高精度台灣 10m 與東亞 50m GeoJSON 幾何數據備份
├── build_game.py                        # 遊戲原始碼建置與地圖注入編譯腳本
├── test_game_engine.js                  # Node.js 全自動化物理模擬與規格檢驗腳本
├── README.md                            # 專案中文主說明文件
├── ARCHITECTURE.md                      # 系統架構全景與數學模型文件
├── docs/                                # 開發與設計技術文件庫
│   ├── ARCHITECTURE_COMPARISON.md       # 台日兩版全方位架構深度對照
│   ├── GAME_DESIGN.md                   # 遊戲設計企劃書 (GDD)
│   ├── DEVELOPMENT_GUIDE.md             # 本開發手冊
│   └── CHANGELOG.md                     # 版本演進歷程與修復紀錄
└── references/                          # 參考專案與原型對照
    └── original-typhoon-escape/         # 🇯🇵 原版 Typhoon Escape 離線完整專案
        ├── index.html                   # 原版單檔遊戲本體（116 KB，離線可直接執行）
        └── README.md                    # 原版專案技術解析與說明
```

---

## 3. 啟動本機伺服器與雙版本對照

專案內附輕量級 Python 伺服器，可在無任何第三方套件下啟動：

```bash
cd ~/Documents/mine/typhoon-escape-taiwan
python3 server.py [指定連接埠，預設 8080]
```

終端機將顯示雙版本訪問連結：
- **台灣在地化旗艦版：** [http://localhost:8080/index.html](http://localhost:8080/index.html)
- **日本原版離線對照版：** [http://localhost:8080/references/original-typhoon-escape/index.html](http://localhost:8080/references/original-typhoon-escape/index.html)

---

## 4. 執行自動化測試與驗證套件

在修改任何物理演算法、地圖頂點或狀態機邏輯後，必須執行全套自動化測試：

```bash
node test_game_engine.js
```

### 測試覆蓋矩陣說明：
1. **結構完整性：** 檢驗 `<canvas>`, `<script id="mapdata">`, 虛擬搖桿, 跑馬燈, 按鈕與 9 大島嶼環資料結構。
2. **1:1 等角麥卡托驗證：** 斷言 $X/Y$ 經緯像素縮放比嚴格符合 $\frac{1}{\cos(23.6^\circ)} \approx 1.091$。
3. **初始碰撞與大陸漂移檢驗：** 確保開局第一幀無歐亞大陸板塊自動位移噴飛問題。
4. **22 個沿海地理地標分類檢驗：** 輸入 22 處台灣極點、名港與離島經緯度，驗證文字地標 100% 精準吻合。
5. **護國神山防衛削弱機制：** 模擬颱風掠過山脈主脊 30 幀，檢驗暴風半徑削減與通報觸發。
6. **1,000 幀颱風物理動態模擬：** 驗證 6 種路徑生成、移動、藤原效應、邊界消散過程中無 `NaN` 或記憶體異常。
7. **重新開始與社群分享：** 驗證重置時統計面板隱藏、稱號重置及 Threads/𝕏/LINE 連結協議格式。

---

## 5. 地圖資料處理與建置管線 (build_game.py)

當需要更新或重新提取 Natural Earth 地圖幾何時，可使用 [build_game.py](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/build_game.py)：

### 執行建置：
```bash
python3 build_game.py
```

### 建置腳本職責：
1. 讀取 [map_data.json](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/map_data.json)。
2. 將經緯度序列簡化壓縮並過濾超出視野半徑之極遠島礁。
3. 合併 HTML 模板、CSS 樣式表、核心物理 JS 代碼、Web Audio 合成模組與 JSON 資料島。
4. 輸出最終發布檔 [index.html](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/index.html)。

---

## 6. 遊戲核心物理與氣象參數微調手冊

所有核心遊戲平衡常數皆集中宣告於 `index.html` 前段，方便微調：

```javascript
// === 視窗與投影參數 ===
var CEN = 123.8;      // 視野中心經度（台灣東側海域）
var LONW = 22.0;      // 視窗經度涵蓋範圍（度）
var K = 1.35;         // 台灣島幾何放大倍率（調大更利於觸控，調小海域更寬闊）

// === 玩家移動力學 ===
var TILT_SPEED = 180; // 虛擬方向舵推力速度（像素/秒）
var DRAG_FORCE = 0.12;// 慣性滑動衰減係數（越接近 0 停得越快，越接近 1 滑得越遠）

// === 護國神山防衛參數 ===
var SHRED_RATE = 0.35;// 暴風圈掠過山脊時每秒削減率（35%/秒）
var HIT_THRESHOLD = 0.35; // 累積接觸多少秒觸發全台特報廣播

// === 颱風生成與雙颱力學 ===
var MAX_TYPHOONS = 5; // 畫面上最多同時存在之颱風上限
var FUJI_DIST = 160;  // 觸發藤原效應之臨界距離（像素）
var FUJI_FORCE = 0.7; // 雙颱互繞公轉角速度倍率
```

---

## 7. Web Audio 音效除錯與合成調整

為遵守瀏覽器自動播放政策（Autoplay Policy），`AudioContext` 採用**惰性延遲初始化**：
- 僅在玩家第一次點擊畫面（觸發 `touchstart` / `mousedown` / `keydown`）時呼叫 `getAudio().resume()`。
- 音效合成完全由原生震盪器 (`OscillatorNode`)、緩衝區來源 (`AudioBufferSourceNode`) 與雙極濾波器 (`BiquadFilterNode`) 構成。

若欲調整海風背景音：
- 尋找 `makePinkNoise()` 函式，可調整濾波器中心頻率（預設 `450Hz`）及 $Q$ 值。
- 尋找 `updateWindAudio(closestDist)`，可微調暴風逼近時海風最大增益音量（預設 `0.35`）。

---

## 8. 打包發布與單檔分發規範

1. **零外部伺服器依賴：** 不引用 CDN（如 unpkg, cdnjs），不引用 Google Fonts，不下載外部音效或圖檔。
2. **本機雙擊即玩：** 確保直接使用 `file://` 協定開啟 [index.html](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/index.html) 時所有功能 100% 正常。
3. **離線存檔支援：** 遊戲設定（如音效開關、最高分紀錄）保存在使用者的 `localStorage` 中。
4. **Git 與 GitHub 協作同步：**
   - 官方 GitHub 專案倉庫：[https://github.com/ImL1s/typhoon-escape-taiwan](https://github.com/ImL1s/typhoon-escape-taiwan)
   - 發布前必須執行 `python3 build_game.py` 重新編譯幾何與模板，確保 `index.html` 狀態與代碼庫完全同步。
   - 發布前必須執行 `node test_game_engine.js` 通過所有測試。

