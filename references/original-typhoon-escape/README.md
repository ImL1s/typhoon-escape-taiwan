# 🇯🇵 原版 Typhoon Escape（タイフーンエスケープ）參考專案

> 本目錄保存了經典網頁遊戲《Typhoon Escape》的原始離線版本與技術分析，作為《台灣大逃亡：颱風來啦！(Typhoon Escape Taiwan)》的對照參考專案。

[⬅️ 返回《台灣大逃亡》專案主頁](../../README.md) | [🎮 啟動台灣在地化旗艦版](../../index.html) | [🏗️ 查看全方位架構技術對照](../../docs/ARCHITECTURE_COMPARISON.md)

---

## 📌 專案來源與原始資訊

- **原始線上發布網址：** [https://lovewcycle.com/games/others/typhoon-escape.html](https://lovewcycle.com/games/others/typhoon-escape.html)
- **作者／發布方：** lovewcycle
- **發布時間：** 2024–2026
- **語言：** 日文（日本語）
- **主題：** 駕駛日本列島（Japan Archipelago）在西北太平洋躲避颱風襲擊
- **檔案形式：** 單一獨立 HTML 檔案（Zero External Dependencies，約 116 KB）

---

## 🚀 離線運行方式

### 方式一：直接以瀏覽器開啟（零安裝）
直接使用任何現代網頁瀏覽器（Chrome, Safari, Edge, Firefox）雙擊本目錄下的 [index.html](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/references/original-typhoon-escape/index.html) 即可離線遊玩。

### 方式二：透過專案本地伺服器
在專案根目錄啟動伺服器：
```bash
python3 server.py
```
接著在瀏覽器中開啟：
[http://localhost:8080/references/original-typhoon-escape/index.html](http://localhost:8080/references/original-typhoon-escape/index.html)

---

## 🎮 原始玩法與操作方式

- **操作目標：** 操控日本列島在太平洋上移動，避免被不斷生成的颱風眼登陸。
- **手機觸控：** 螢幕左下方提供半透明虛擬圓盤搖桿（Pad / Knob）進行方向牽引。
- **鍵盤控制：** 支援鍵盤 WASD 與方向鍵移動列島。
- **碰撞判定：** 
  - 當颱風中心與日本陸地頂點重疊時，視為登陸（Game Over），並依經緯度標記 8 大地方（北海道、東北、關東、中部、近畿、中國、四國、九州）。
  - 當日本列島碰撞周邊歐亞大陸或島嶼時，觸發 `pushLand` 與 `slideLand` 將其他陸地推擠開。
- **跑馬燈機制：** 底部提供雙層跑馬燈（Ticker），以紅色（緊急警戒）與黃色（颱風速報）跑馬顯示颱風動態。
- **成績分享：** 結算時計算存活天數與登陸颱風資訊，可一鍵轉發至 𝕏 (Twitter)。

---

## 🔬 技術架構與原始程式碼分析

### 1. 單檔結構 (Self-Contained Bundle)
- **DOM 結構：**
  - `<canvas id="cv">`：全螢幕繪圖畫布。
  - `<div class="hud">`：頂部遊戲時間與資訊欄。
  - `<div id="popup">`：開始畫面與遊戲結束結算彈窗。
  - `<div id="pad">`：左下方虛擬方向盤搖桿。
  - `<div id="ticker">`：底部跑馬燈容器。
  - `<div id="menu">`：說明與授權彈窗。
- **內嵌地圖資料 (`#worlddata`)：**
  - 內嵌一組 TopoJSON 資料，解碼後包含 `countries`（日本國界，id: 392）與 `land`（周邊世界陸塊幾何多邊形）。

### 2. 核心技術實作
- **投影方式 (`merc`)：** 使用標準球面麥卡托投影（Spherical Mercator），公式為：
  $$y = \ln(\tan(\frac{\pi}{4} + \frac{\text{lat}}{2}))$$
- **多邊形內點檢驗 (`inPoly`)：** 採用射線法（Ray casting algorithm）計算點是否落在日本或周圍陸塊輪廓內。
- **颱風生成與移動 (`spawn`, `update`)：**
  - 颱風於地圖隨機邊緣生成，計算朝向日本列島的角度向量 `toward(jp)`。
  - 以定速前進，無複雜氣象雷達或多樣路徑分類。
- **音效：** 無音效實作（全靜音）。

---

## ⚖️ 資料來源與開源授權聲明

1. **地圖資料：**
   - Natural Earth（Public Domain）
   - world-atlas（Copyright 2013-2019 Michael Bostock，ISC License）：
     > Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted...
2. **颱風命名：**
   - 日本氣象廳（JMA）「台風の番号とアジア名の付け方」亞洲颱風命名表。

---

## 🔄 與《台灣大逃亡》的差異摘要

| 比較維度 | 原版 Typhoon Escape (日本列島) | 台灣大逃亡 (Typhoon Escape Taiwan) |
| :--- | :--- | :--- |
| **主角陸塊** | 日本列島（3 大幾何塊） | 台灣本島 + 澎湖、綠島、蘭嶼、小琉球等 9 大離島環 |
| **地圖投影** | 一般麥卡托（未針對局部緯度縱橫比修正） | 1:1 嚴格等角麥卡托（消除垂直壓縮，番薯輪廓精準） |
| **地形互動** | 碰撞其他陸塊會將大陸推飛（板塊漂移 Bug） | 歐亞大陸穩固錨定，中央山脈具備**護國神山防衛削弱機制** |
| **颱風路徑** | 單一隨機直線向量朝日本移動 | 6 大經典路徑（穿心、西北、韋恩迷走、鞍形停滯、藤原效應雙颱） |
| **氣象雷達** | 單色同心圓與單層圈線 | CWA 5 階七彩動態螺旋雨帶、雙重風級警戒圈、72hr 潛勢預報錐 |
| **音效系統** | 無（完全靜音） | Web Audio API 純程式合成海洋風暴、空襲警報、神山光束、登陸爆炸 |
| **登陸判定** | 8 個廣域地方行政區 | 22 個精準沿海鄉鎮、岬角港灣與離島地標 |
| **社群分享** | 僅支援 𝕏 (Twitter) | 支援 Threads、𝕏、LINE 一鍵發布與戰報卡片複製 |

---

## 🔗 相關技術文檔連結
- 📐 [全方位系統架構深度對照 (ARCHITECTURE_COMPARISON.md)](../../docs/ARCHITECTURE_COMPARISON.md)
- 🏛️ [系統全景架構設計與狀態機 (ARCHITECTURE.md)](../../ARCHITECTURE.md)
- 🎮 [遊戲設計企劃書 GDD (GAME_DESIGN.md)](../../docs/GAME_DESIGN.md)
- 🛠️ [開發者維護與建置指引 (DEVELOPMENT_GUIDE.md)](../../docs/DEVELOPMENT_GUIDE.md)
