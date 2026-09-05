<p align="center">
  <img src="assets/banner.jpg" alt="台灣大逃亡：颱風來啦！(Typhoon Escape Taiwan)" width="100%">
</p>

# 🇹🇼 台灣大逃亡：颱風來啦！(Typhoon Escape Taiwan)

<p align="center">
  <a href="https://iml1s.github.io/typhoon-escape-taiwan/"><img src="https://img.shields.io/badge/🎮_線上立即玩-Play_Now-00D2FF?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Play Online"></a>
  <a href="https://github.com/ImL1s/typhoon-escape-taiwan/releases"><img src="https://img.shields.io/github/v/release/ImL1s/typhoon-escape-taiwan?style=for-the-badge&color=F5B400" alt="GitHub Release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-4CAF50?style=for-the-badge" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/Dependencies-Zero-brightgreen?style=for-the-badge" alt="Zero Dependencies">
  <img src="https://img.shields.io/badge/Platform-Web%20%2F%20Mobile-blue?style=for-the-badge" alt="Platform: Web & Mobile">
</p>

<h3 align="center">
  🌀 <b><a href="https://iml1s.github.io/typhoon-escape-taiwan/">點擊此處立即線上遊玩 (Click to Play Online)</a></b> 🌀
</h3>

<p align="center">
  <i>全島開動！駕駛整座台灣島，在西北太平洋狂暴颱風陣中蛇行漂移，依靠護國神山中央山脈抵擋狂風暴雨，挑戰存活極限！<br>
  免下載、免安裝，手機觸控、平板、電腦瀏覽器隨開即玩！</i>
</p>

---

## 📸 遊戲畫面預覽 (Screenshots)

<p align="center">
  <img src="assets/gameplay_action.png" alt="遊戲實戰畫面：雙颱夾擊與中央山脈護國神山防衛結界" width="49%">
  <img src="assets/gameplay.png" alt="遊戲標題畫面：出發啟動台灣島" width="49%">
</p>

---

## 📖 專案介紹

本專案靈感源自經典網頁遊戲《Typhoon Escape》，並進行了全方位的**台灣在地化、1:1 等角地理重繪與玩法升級**。

玩家不再只是看著雷達回波圖乾著急，而是親自擔任「全島總指揮舵手」，操控**台灣本島及澎湖群島、綠島、蘭嶼、小琉球、龜山島等島群**，在風雲變色的西北太平洋與南海海域間穿梭，躲避接踵而來的穿心颱、西北颱、迷走怪颱！

遊戲為**單一獨立 HTML 檔案（Zero Dependencies）**，所有高精度海岸線地理座標、物理引擎、氣象雷達渲染以及 Web Audio 合成音效皆完整內嵌，**雙擊即可離線遊玩**！

---

## 🎮 玩法與操作方式

- **手機／平板觸控：**
  - **全螢幕任意拖曳：** 在螢幕任何位置滑動，即可牽引台灣島靈活避難。
  - **虛擬雷達方向舵：** 使用左下角半透明虛擬搖桿推動方向（位於跑馬燈上方，不遮擋、不跳動）。
- **電腦鍵盤：**
  - 使用 **WASD** 或 **方向鍵（↑ ↓ ← →）** 進行全方位無段位導航。
  - 按 **Space（空白鍵）**：開始遊戲 / 再戰下一個夏天 / 暫停遊戲。
  - 按 **P 鍵**：暫停與繼續遊戲。
- **滑鼠控制：**
  - 按住滑鼠左鍵並拖曳進行操控。
- **輔助控制：**
  - **🔊 / 🔇 音效按鈕：** 切換颱風警報、呼嘯風聲、背景海風與雷暴音效。
  - **⏸️ / ▶️ 暫停按鈕：** 隨時暫停戰局或截圖存檔。
  - **ℹ️ 說明按鈕：** 查看氣象科普、操作指引與逃生密技。

---

## ✨ 核心特色與台灣在地靈魂

### 1. 護國神山（中央山脈）防衛削弱機制
- 台灣脊梁中央山脈（標高 3952 公尺玉山主峰）名不虛傳！
- 當颱風暴風圈掠過台灣東側山脊時，陸地摩擦力與地形屏障會激發**神山防禦結界**（碧藍能量光條與玉山信號閃爍），**快速削弱颱風結構、縮小其暴風半徑**，為玩家爭取寶貴的逃生時間！（但切記：颱風眼牆核心若直接撞上依然會造成登陸滅頂！）

### 2. 1:1 完美等角麥卡托投影（True Conformal Mercator）
- 依據嚴格數學公式 `dlat / dlon = 1 / cos(lat)` 重建投影矩陣，徹底消除地圖垂直形變，真實呈現台灣經典「番薯（甘藷）」輪廓。
- 台灣本島與澎湖、綠島、蘭嶼、外傘頂洲、小琉球、龜山島等 9 大幾何環，共 562 個節點精準繪製；金門、馬祖與歐亞大陸海岸線真實錨定，遊戲開局絕無板塊自動漂移 Bug！

### 3. 逼真 CWA 氣象雷達回波與 72 小時路徑潛勢預報
- **雷達回波七彩螺旋雨帶：** 綠色（輕度雨帶） ➔ 黃色 ➔ 橘色 ➔ 腥紅 ➔ 紫色破壞性眼牆，依逆時針氣旋旋轉。
- **雙重警戒暴風圈：** 外圈黃色虛線為 7 級風暴風半徑；內圈紅色實線為 10 級風毀滅性眼牆。
- **潛勢預報虛線錐：** 結合中央氣象署經典 72 小時機率潛勢圈，提前預判路徑走向。

### 4. 六大台灣經典路徑與藤原效應
- **直撲穿心颱：** 高速自東部海面直插花蓮台東，考驗瞬間反應。
- **西北颱：** 緊貼基隆北海岸西行，北部引進狂暴西北風。
- **迷走怪颱（韋恩、納莉、山陀兒）：** 原地打轉、醉漢漫步、出其不意來記回馬槍！
- **鞍形場停滯：** 陷入高壓夾縫一動不動，卻在海面上持續吸熱長成龐然巨怪。
- **追尾鎖定：** 導引氣流強勢引導，死死緊咬台灣不放。
- **藤原效應（雙颱共舞）：** 雙颱距離接近時會產生互繞公轉運動！

### 5. 22 個台灣沿海與離島精準登陸位置判定
當不幸遭颱風眼核心登陸時，系統會精確回報登陸縣市與地標：
> 「第 8 號強烈颱風『山陀兒』於【屏東枋寮、大鵬灣】暴力登陸！」  
> 「第 3 號中度颱風『凱米』於【宜蘭蘇澳、南澳】登陸！狂風暴雨肆虐全島！」

### 6. 爆笑且真實的中央氣象署跑馬燈
- 🔴 **紅色特警：** 海上陸上警報、外送平台暫停營業、全台停班停課。
- 🟡 **黃色快訊：** 颱風生成消滅、減弱為熱帶性低氣壓（TD）、高麗菜一顆 280 元。
- 🔵 **藍色民生迷因：** KTV 官網湧入百萬人塞爆、花雕雞泡麵被掃空、水庫大進補。

### 7. 六階全台認證稱號與社群一鍵分享
- **0～5 天：** 【泡麵還沒買好】
- **6～15 天：** 【中央山脈實習生】
- **16～29 天：** 【颱風假精算師】
- **30～49 天：** 【護國神山防衛隊長】
- **50～74 天：** 【開著台灣島漂移的航海王】
- **75+ 天：** 【太平洋不沉航母．台灣之神】
- 提供 **Threads、𝕏、LINE 一鍵分享** 與 **戰報文字卡片複製** 功能！

### 8. Web Audio API 純程式合成聲學引擎
- **海洋風暴粉紅噪音合成環境音：** 隨颱風逼近自動增強呼嘯海風。
- **防颱空襲警報：** 460Hz ~ 780Hz 三角波升降警報。
- **神山削弱氣流音：** 多階正弦波填平降調合成。
- **登陸雷暴低通白噪音衝擊。**

---

## 🚀 快速啟動

### 方式一：直接雙擊開啟（最簡單，零安裝）
直接用 Chrome、Safari、Edge、Firefox 點擊開啟本目錄下的 `index.html` 即可立即遊玩！

### 方式二：使用內附 Python 伺服器
```bash
cd ~/Documents/mine/typhoon-escape-taiwan
python3 server.py
```
終端機會自動啟動伺服器並在瀏覽器中開啟 `http://localhost:8080/index.html`。

---

## 📂 檔案目錄結構

```
~/Documents/mine/typhoon-escape-taiwan/
├── index.html                           # 🇹🇼 台灣大逃亡完整遊戲本體（Zero Dependencies，雙擊即玩）
├── server.py                            # 輕量級 Python 本地預覽伺服器（支援雙版本切換）
├── map_data.json                        # 原始提取之台灣 10m 與東亞 50m 地理幾何 GeoJSON 備份
├── build_game.py                        # 遊戲產生器與幾何建置編譯腳本
├── test_game_engine.js                  # 自動化單元測試與物理模擬驗證套件
├── README.md                            # 專案中文主說明文件
├── ARCHITECTURE.md                      # 系統架構全景、狀態機、座標管線與數學模型手冊
├── docs/                                # 📚 核心設計與開發技術文件庫
│   ├── ARCHITECTURE_COMPARISON.md       # 台日兩版全方位架構深度技術對照分析
│   ├── GAME_DESIGN.md                   # 遊戲設計企劃書 (GDD) 與數值迷因規格
│   ├── DEVELOPMENT_GUIDE.md             # 開發者除錯、測試執行與調參維護指南
│   └── CHANGELOG.md                     # 版本演進歷史與功能修復紀錄
└── references/                          # 🔍 參考專案與離線原型對照
    └── original-typhoon-escape/         # 🇯🇵 原版日本《Typhoon Escape》完整離線收錄版
        ├── index.html                   # 原始單檔遊戲本體（116 KB，完全離線可執行）
        └── README.md                    # 原版專案解析與授權說明
```

---

## 📚 系統文件與技術參考 (Documentation)

本專案提供完整的軟體工程技術文檔，供架構審查、二次開發或改裝參考：

1. **[ARCHITECTURE.md](ARCHITECTURE.md)：**
   詳細記載系統整體架構、狀態機生命週期、1:1 等角麥卡托三層座標變換管線、AABB 空間過濾、中央山脈削弱力學方程、Web Audio 節點連接拓撲圖與自動化測試架構。
2. **[docs/ARCHITECTURE_COMPARISON.md](docs/ARCHITECTURE_COMPARISON.md)：**
   深度剖析原版日本《Typhoon Escape》與《台灣大逃亡》在投影數學、海岸拓撲、板塊漂移修復、颱風行為樹、護國神山防衛、程序聲學等 12 大維度的完整技術評估。
3. **[docs/GAME_DESIGN.md](docs/GAME_DESIGN.md)：**
   遊戲設計企劃書（GDD），記載四大設計基石、核心玩法循環、六大經典路徑參數特徵、22 沿海地標分類庫、紅黃藍三色跑馬燈迷因庫與六階認證稱號體系。
4. **[docs/DEVELOPMENT_GUIDE.md](docs/DEVELOPMENT_GUIDE.md)：**
   開發者手冊，包含本機開發環境、雙版本預覽操作、自動化測試執行、地圖幾何重建、物理平衡參數微調與單檔打包分發指引。
5. **[docs/CHANGELOG.md](docs/CHANGELOG.md)：**
   記錄專案從初始原型到當前功能完備版本的演進軌跡。
6. **[references/original-typhoon-escape/](references/original-typhoon-escape/README.md)：**
   原版日本遊戲離線對照專案，包含原始 HTML 本體與逆向技術分析。

---

## 🧪 驗證與測試

本專案已通過完整 Node.js 自動化測試：
```bash
node test_game_engine.js
```
測試覆蓋項目：
1. `index.html` 結構完整性與 9 個台灣幾何環、135 個周邊陸塊 JSON 解析驗證
2. 1:1 等角麥卡托（Conformal Mercator）投影無形變比率檢驗（`conformalRatio ≈ 1 / cos(lat)`）
3. 初始狀態 0 碰撞與 0 大陸板塊漂移檢查（徹底排除開局板塊自動噴飛 Bug）
4. 22 個台灣代表性地理地標分類器 100% 精準測試
5. 中央山脈護國神山防衛削弱與通報機制觸發驗證
6. 颱風 1,000 幀物理更新無 NaN、無坐標異常、生命週期與藤原效應消散測試
7. 遊戲重新開始（Restart）DOM 狀態乾淨重設驗證與社群分享連結有效性檢查
8. 離線參考專案（Original Typhoon Escape）完整性與核心規格檢定
9. 專案全套技術文檔齊全性檢驗

---

## 📜 資料來源與鳴謝
- 地理數據：Natural Earth（Public Domain）
- 颱風命名：世界氣象組織（WMO）西北太平洋颱風命名表、中華民國交通部中央氣象署（CWA）
- 原始靈感與參考原型：[https://lovewcycle.com/games/others/typhoon-escape.html](https://lovewcycle.com/games/others/typhoon-escape.html)（收錄於 [references/original-typhoon-escape/](references/original-typhoon-escape/README.md)）

---

## 🌐 English Overview

**Typhoon Escape Taiwan (台灣大逃亡：颱風來啦！)** is a pure HTML5 web arcade survival game inspired by the classic *Typhoon Escape*. Navigate the entire island of Taiwan across the Northwestern Pacific and South China Sea while dodging relentless typhoons!

- **True Conformal Mercator Projection:** Mathematical aspect-ratio matching eliminates vertical distortion for true cartographic precision.
- **Central Mountain Range Defense System:** Grazing typhoons have their wind radius and structural intensity shredded by the mountain barrier.
- **Dynamic Weather Radar Simulation:** Realistic spiral rainbands, dual warning circles (Level 7 gale & Level 10 storm), and 72-hour forecast cones.
- **22 Landfall Landmarks:** Accurate geographic detection when typhoons make landfall across coastal counties and offshore islands.
- **Procedural Web Audio Engine:** Atmospheric ocean wind, air raid siren, and storm effects synthesized dynamically in code.
- **Zero Dependencies:** Single self-contained HTML file, offline playable, mobile touch & desktop keyboard friendly!

---

## 📄 授權條款 (License)

本專案採用 [MIT License](LICENSE) 授權開放。


