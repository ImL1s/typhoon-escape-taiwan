# 📝 版本演進歷程 (Changelog)

> 《台灣大逃亡：颱風來啦！(Typhoon Escape Taiwan)》專案版本發布與演進紀錄。

---

## [v1.2.0] - 2026-09-05 (文檔、架構評估與離線參考專案完善)

### ✨ 新增功能與資產整理
- **離線參考專案：** 完整收錄原版日本《Typhoon Escape》單檔專案至 `references/original-typhoon-escape/`，包含完整的離線版 [index.html](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/references/original-typhoon-escape/index.html) 與技術解析文檔 [README.md](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/references/original-typhoon-escape/README.md)。
- **架構對照全景文檔：** 新增 [docs/ARCHITECTURE_COMPARISON.md](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/docs/ARCHITECTURE_COMPARISON.md)，從投影數學、拓撲精度、物理動力學、中央山脈防衛、Web Audio 聲學、雷達回波到本土文化迷因等 12 個維度進行深度技術剖析。
- **系統架構技術手冊：** 新增根目錄 [ARCHITECTURE.md](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/ARCHITECTURE.md)，詳解狀態機、座標管線、AABB 空間過濾、Web Audio 合成拓撲圖與測試框架。
- **遊戲設計企劃書：** 新增 [docs/GAME_DESIGN.md](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/docs/GAME_DESIGN.md)，記載四大設計基石、核心循環、風險回報模型與迷因資料庫。
- **開發者指引手冊：** 新增 [docs/DEVELOPMENT_GUIDE.md](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/docs/DEVELOPMENT_GUIDE.md)，涵蓋本機除錯、測試執行、參數微調與單檔打包規範。
- **預覽伺服器升級：** 升級 [server.py](file:///Users/iml1s/Documents/mine/typhoon-escape-taiwan/server.py)，支援同時列出台灣在地化旗艦版與日本原版對照版之快速切換連結。

---

## [v1.1.0] - 2026-09-03 (等角投影校正與護國神山防衛機制)

### 🚀 核心升級
- **1:1 嚴格等角麥卡托投影 (True Conformal Mercator)：** 依據 $\frac{d\text{lat}}{d\text{lon}} = \frac{1}{\cos(\text{lat})}$ 重新構建投影矩陣，徹底消除地圖垂直拉伸形變，完美還原台灣甘藷（番薯）輪廓。
- **中央山脈護國神山防衛系統：** 建立 16 節點脊梁骨幹，當暴風圈擦過東側山脊時激發碧藍能量結界，以每秒 35% 速度劇烈削減颱風半徑，並伴隨玉山信號與合成音效。
- **六大經典颱風路徑：** 實作穿心直撲、西北颱、韋恩迷走怪颱、追尾鎖定、鞍形場停滯與拋物轉向。
- **藤原效應雙颱互繞：** 實作海面雙颱相互吸引逆時針公轉力學。
- **22 個沿海精準地標分類器：** 告別粗糙分區，提供金門、馬祖、澎湖、綠島、蘭嶼、富貴角、三貂角、知本、安平、枋寮等精確登陸點診斷。
- **Web Audio 純程式合成聲學引擎：** 包含海洋風暴粉紅噪音動態環境音、防颱空襲警報、神山結界音與登陸爆炸低通白噪音。

### 🐛 缺陷修復
- **修復歐亞大陸板塊自動噴飛漂移 Bug：** 重新校準台灣與周邊陸塊起始距離，設定大陸錨定阻尼，開局首幀物理碰撞數清零。
- **修復手機端搖桿遮擋跑馬燈：** 使用動態 CSS `--rows` 自適應調整虛擬方向舵高度。
- **修復遊戲重新開始殘留問題：** 清除遊戲結束彈窗上的統計資料與稱號標籤。

---

## [v1.0.0] - 2026-08-30 (初始在地化原型版本)

- 移植原版遊戲概念至台灣地理。
- 提取 Natural Earth 台灣與東亞海岸線數據。
- 實現基本鍵盤與觸控移動。
