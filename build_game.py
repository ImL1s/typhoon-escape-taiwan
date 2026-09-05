import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_DATA_PATH = os.path.join(BASE_DIR, 'map_data.json')
INDEX_HTML_PATH = os.path.join(BASE_DIR, 'index.html')

with open(MAP_DATA_PATH, encoding='utf-8') as f:
    map_data = json.load(f)

map_json_str = json.dumps(map_data, separators=(',', ':'))

html_content = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
<title>台灣大逃亡：颱風來啦！ - 開著台灣島逃離西北太平洋暴風圈</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌀</text></svg>">
<meta name="description" content="全島開動！駕駛台灣島在西北太平洋狂暴颱風陣中蛇行漂移，依靠護國神山中央山脈抵擋狂風暴雨，挑戰存活極限！">
<style>
  :root {{
    --c-bg: #0B162C;
    --c-radar-blue: #102A54;
    --c-card-bg: rgba(13, 27, 54, 0.95);
    --c-text: #EAF2FB;
    --c-gold: #F5B400;
    --c-emerald: #4CAF50;
    --c-danger: #FF3B30;
    --c-accent: #00D2FF;
    --rows: 0;
  }}
  * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
  html, body {{
    margin: 0; padding: 0; height: 100%; width: 100%;
    overflow: hidden; background: var(--c-bg);
    color: var(--c-text);
    font-family: system-ui, -apple-system, "PingFang TC", "Microsoft JhengHei", "Noto Sans TC", sans-serif;
    touch-action: none;
    overscroll-behavior: none;
  }}
  #wrap {{
    position: fixed; inset: 0;
    touch-action: none; user-select: none; -webkit-user-select: none;
  }}
  canvas {{ display: block; width: 100%; height: 100%; }}
  
  /* Top HUD */
  .hud {{
    position: absolute; left: 14px; top: 14px;
    display: flex; flex-direction: column; gap: 6px;
    font-size: 13px; z-index: 10; pointer-events: none;
  }}
  .hud-row {{ display: flex; gap: 8px; align-items: center; }}
  .hud-badge {{
    background: rgba(10, 28, 56, 0.85);
    color: #E2EFFC;
    border: 1px solid rgba(0, 210, 255, 0.3);
    border-radius: 8px;
    padding: 6px 12px;
    font-weight: 500;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    box-shadow: 0 4px 14px rgba(0,0,0,0.35);
    display: flex; align-items: center; gap: 6px;
  }}
  .hud-date {{ font-size: 15px; font-weight: 700; color: #FFF; }}
  .hud-sub {{ font-size: 12px; color: #A0C4E8; }}
  
  /* Top Right Controls */
  .top-btns {{
    position: absolute; right: 14px; top: 14px;
    display: flex; gap: 8px; z-index: 10;
  }}
  .ctrl-btn {{
    width: 42px; height: 42px; border-radius: 10px;
    background: rgba(10, 28, 56, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.22);
    color: #EAF2FB; font-size: 18px;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    box-shadow: 0 4px 14px rgba(0,0,0,0.35);
    transition: all 0.15s ease;
  }}
  .ctrl-btn:active {{ transform: scale(0.92); background: rgba(0, 210, 255, 0.25); }}
  
  /* Virtual Joystick */
  #pad {{
    position: absolute; left: 16px;
    bottom: 84px;
    width: 132px; height: 132px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,210,255,0.08) 0%, rgba(255,255,255,0.08) 60%, rgba(255,255,255,0.18) 100%);
    border: 1.5px solid rgba(0, 210, 255, 0.38);
    box-shadow: 0 0 20px rgba(0, 210, 255, 0.18), inset 0 0 15px rgba(0, 210, 255, 0.12);
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    z-index: 12;
  }}
  #pad::before {{
    content: ""; position: absolute; inset: 18px; border-radius: 50%;
    border: 1px dashed rgba(255, 255, 255, 0.28); pointer-events: none;
  }}
  #pad::after {{
    content: "方向舵"; position: absolute; bottom: 8px; left: 0; right: 0;
    text-align: center; font-size: 10px; color: rgba(255,255,255,0.45);
    letter-spacing: 2px; pointer-events: none;
  }}
  #knob {{
    width: 52px; height: 52px; border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #FFFFFF 0%, #B4D7FE 70%, #76ABDF 100%);
    position: absolute; left: 40px; top: 40px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.5), 0 0 12px rgba(0,210,255,0.6);
    pointer-events: none;
  }}
  
  /* Weather News Ticker */
  #ticker {{
    position: absolute; left: 0; right: 0; bottom: 0;
    display: flex; flex-direction: column; z-index: 20;
    pointer-events: none;
  }}
  .row {{
    height: 36px; display: flex; align-items: stretch; overflow: hidden;
    pointer-events: none;
  }}
  .row.red {{
    background: linear-gradient(90deg, rgba(218, 41, 28, 0.95), rgba(180, 25, 15, 0.95));
    color: #FFF; border-top: 1px solid rgba(255, 120, 120, 0.4);
  }}
  .row.yellow {{
    background: linear-gradient(90deg, rgba(230, 160, 20, 0.95), rgba(190, 130, 10, 0.95));
    color: #261600; border-top: 1px solid rgba(255, 220, 120, 0.4);
  }}
  .row.blue {{
    background: linear-gradient(90deg, rgba(20, 120, 215, 0.95), rgba(15, 90, 175, 0.95));
    color: #FFF; border-top: 1px solid rgba(120, 200, 255, 0.4);
  }}
  .tag {{
    font-size: 13px; font-weight: 700; padding: 0 12px;
    display: flex; align-items: center; white-space: nowrap; flex: none;
    background: rgba(0, 0, 0, 0.28); letter-spacing: 1px;
  }}
  .track {{ flex: 1; position: relative; overflow: hidden; }}
  .ttext {{
    position: absolute; top: 0; left: 100%; height: 36px; line-height: 36px;
    font-size: 14.5px; font-weight: 500; white-space: nowrap;
    animation: tk linear forwards; text-shadow: 0 1px 2px rgba(0,0,0,0.4);
  }}
  @keyframes tk {{ from {{ transform: translateX(0); }} to {{ transform: translateX(var(--dist)); }} }}
  
  /* Popups */
  #popup {{
    position: absolute; left: 50%; top: 48%; transform: translate(-50%, -50%);
    width: min(88vw, 360px);
    background: var(--c-card-bg);
    color: var(--c-text);
    border-radius: 20px;
    padding: 26px 22px;
    text-align: center;
    box-shadow: 0 16px 40px rgba(0,0,0,0.7), 0 0 0 1px rgba(0,210,255,0.25);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    z-index: 50; transition: all 0.25s ease;
  }}
  #popup.hidden {{ display: none; }}
  #popup .logo-icon {{
    font-size: 46px; margin-bottom: 8px; display: inline-block;
    filter: drop-shadow(0 4px 10px rgba(0,210,255,0.4));
  }}
  #popup h1 {{
    margin: 0 0 8px; font-size: 23px; font-weight: 800;
    color: #FFF; letter-spacing: 0.5px;
  }}
  #popup .subhead {{
    font-size: 13.5px; color: #8DB9E8; margin-bottom: 16px; line-height: 1.5;
  }}
  #popup .stat-box {{
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 14px; padding: 14px; margin-bottom: 18px;
    text-align: left; font-size: 13.5px; line-height: 1.7;
  }}
  #popup .stat-row {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }}
  #popup .stat-val {{ font-weight: 700; color: #FFD23F; }}
  #popup .stat-highlight {{
    background: rgba(255, 59, 48, 0.16);
    border-left: 3px solid #FF3B30;
    padding: 6px 10px; margin-top: 8px;
    border-radius: 4px; color: #FFB0AA; font-size: 13px;
  }}
  #popup .title-badge {{
    display: inline-block; background: linear-gradient(135deg, #F5B400, #FF6B00);
    color: #1A0D00; font-weight: 800; font-size: 15px;
    padding: 5px 14px; border-radius: 20px; margin: 8px 0 14px;
    box-shadow: 0 4px 12px rgba(245, 180, 0, 0.4);
  }}
  .btn-primary {{
    height: 48px; width: 100%; font-size: 16px; font-weight: 700;
    background: linear-gradient(135deg, #00D2FF 0%, #0072FF 100%);
    color: #FFF; border: none; border-radius: 12px; cursor: pointer;
    box-shadow: 0 6px 20px rgba(0, 114, 255, 0.45);
    transition: all 0.15s ease;
  }}
  .btn-primary:active {{ transform: scale(0.97); filter: brightness(1.1); }}
  
  .share-grid {{
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 8px; margin-top: 10px;
  }}
  .btn-share {{
    height: 40px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.18);
    background: rgba(255,255,255,0.08); color: #FFF;
    font-size: 12.5px; font-weight: 600; cursor: pointer;
    display: flex; align-items: center; justify-content: center; gap: 4px;
    transition: all 0.15s ease;
  }}
  .btn-share:active {{ background: rgba(255,255,255,0.2); transform: scale(0.95); }}
  .btn-copy {{
    width: 100%; height: 38px; border-radius: 10px;
    border: 1px dashed rgba(0, 210, 255, 0.4);
    background: rgba(0, 210, 255, 0.08); color: #00D2FF;
    font-size: 13px; font-weight: 600; cursor: pointer; margin-top: 8px;
    display: flex; align-items: center; justify-content: center; gap: 6px;
  }}
  .btn-copy:active {{ background: rgba(0, 210, 255, 0.2); }}

  /* Slide-in Menu Modal */
  #menu {{
    position: absolute; inset: 0;
    background: rgba(7, 16, 34, 0.98);
    color: #E6F1FB; padding: 24px 20px 80px;
    overflow-y: auto; display: none; font-size: 14.5px; line-height: 1.7;
    z-index: 100;
  }}
  #menu.open {{ display: block; }}
  #menu h2 {{ font-size: 20px; font-weight: 700; margin: 0 0 16px; color: #00D2FF; }}
  #menu h3 {{
    font-size: 16px; font-weight: 600; margin: 22px 0 8px;
    border-bottom: 1px solid rgba(0, 210, 255, 0.3); padding-bottom: 6px;
    color: #FFD23F;
  }}
  #menu p {{ margin: 0 0 10px; color: #C5DDF5; }}
  #menu ul {{ margin: 0 0 14px; padding-left: 20px; color: #C5DDF5; }}
  #menu li {{ margin-bottom: 6px; }}
  #menu pre {{
    white-space: pre-wrap; font-size: 12px; background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1); padding: 12px; border-radius: 10px;
  }}
  #menuclose {{
    position: absolute; right: 16px; top: 16px; width: 40px; height: 40px;
    border-radius: 10px; background: rgba(255,255,255,0.12);
    color: #FFF; border: none; font-size: 22px; cursor: pointer;
  }}
  
  /* Toast */
  #toast {{
    position: absolute; top: 20px; left: 50%; transform: translateX(-50%) translateY(-60px);
    background: rgba(0, 210, 255, 0.95); color: #07162C;
    padding: 8px 18px; border-radius: 20px; font-size: 13.5px; font-weight: 700;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    pointer-events: none; transition: transform 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28);
    z-index: 200;
  }}
  #toast.show {{ transform: translateX(-50%) translateY(0); }}
</style>
</head>
<body>
<div id="wrap">
  <canvas id="cv"></canvas>
  
  <!-- Top HUD -->
  <div class="hud">
    <div class="hud-row">
      <div class="hud-badge">
        <span>📅</span>
        <span id="time" class="hud-date">2026年7月1日</span>
      </div>
      <div class="hud-badge">
        <span>🛡️</span>
        <span id="daycount">第 1 天</span>
      </div>
    </div>
    <div class="hud-row">
      <div class="hud-badge">
        <span>💨 已閃避</span>
        <span id="evadedcount" style="color: #00D2FF; font-weight: 700;">0</span>
        <span>個颱風</span>
      </div>
      <div class="hud-badge" id="bestbadge">
        <span>👑 紀錄:</span>
        <span id="bestdays" style="color: #FFD23F; font-weight: 700;">0 天</span>
      </div>
    </div>
  </div>
  
  <!-- Top Right Controls -->
  <div class="top-btns">
    <button id="soundbtn" class="ctrl-btn" aria-label="音效開關" title="音效開關">🔊</button>
    <button id="pausebtn" class="ctrl-btn" aria-label="暫停" title="暫停遊戲 (Space/P)">⏸️</button>
    <button id="menubtn" class="ctrl-btn" aria-label="選單說明" title="遊戲指南">ℹ️</button>
  </div>
  
  <!-- Virtual Joystick -->
  <div id="pad"><div id="knob"></div></div>
  
  <!-- Real-time News Marquee -->
  <div id="ticker"></div>
  
  <!-- Main Dialog Popup -->
  <div id="popup">
    <div class="logo-icon" id="picon">🇹🇼</div>
    <h1 id="ptitle">台灣大逃亡：颱風來啦！</h1>
    <div id="psub" class="subhead">開著台灣島，在西北太平洋暴風陣中漂移求生！</div>
    
    <div id="pstats" class="stat-box" style="display:none;">
      <div class="stat-row"><span>存活天數</span><span id="res-days" class="stat-val">0 天</span></div>
      <div class="stat-row"><span>閃避颱風</span><span id="res-evaded" class="stat-val">0 個</span></div>
      <div class="stat-row"><span>堅持至</span><span id="res-date" class="stat-val">2026年7月1日</span></div>
      <div id="res-hit" class="stat-highlight">颱風於台灣登陸</div>
    </div>
    
    <div id="res-title-wrap" style="display:none;">
      <div style="font-size: 12px; color: #8DB9E8;">榮獲全台認證稱號</div>
      <div id="res-title" class="title-badge">【中央山脈實習生】</div>
    </div>
    
    <button id="pbtn" class="btn-primary">迎戰颱風季！發動台灣島！</button>
    
    <div id="sharesection" style="display:none;">
      <button id="copybtn" class="btn-copy">📋 複製戰報成績卡片</button>
      <div class="share-grid">
        <button id="threadbtn" class="btn-share">🧵 Threads</button>
        <button id="xbtn" class="btn-share">𝕏 Post</button>
        <button id="linebtn" class="btn-share">💬 LINE</button>
      </div>
    </div>
  </div>
  
  <!-- Menu Modal -->
  <div id="menu">
    <button id="menuclose" aria-label="關閉選單">✕</button>
    <h2>🌀 台灣大逃亡：颱風來啦！</h2>
    <p>這是一款向《Typhoon Escape》致敬的台灣本地化硬派氣象逃脫遊戲。玩家駕駛整座台灣島，在西北太平洋的強颱狂暴海域中躲避一個接一個襲來的颱風！</p>
    
    <h3>🎮 操作指南</h3>
    <ul>
      <li><b>觸控拖曳：</b>直接在螢幕任何位置滑動，即可牽引台灣島靈活漂移。</li>
      <li><b>虛擬方向舵：</b>使用左下方虛擬搖桿，推向任意方向進行導航。</li>
      <li><b>鍵盤控制：</b>電腦玩家可使用 <b>WASD</b> 或 <b>方向鍵（↑ ↓ ← →）</b> 全方位移動，按 <b>Space</b> 開始/暫停，按 <b>P</b> 暫停。</li>
    </ul>
    
    <h3>⛰️ 護國神山防衛機制</h3>
    <p>中央山脈（護國神山）標高 3952 公尺（玉山主峰），能有效破壞颱風環流！當颱風外圍暴風圈擦過台灣東側山脊時，地形摩擦將激發神山防禦結界，快速削減暴風半徑與強度！請善用神山削減颱風，但切勿讓毀滅性眼牆直接登陸！</p>
    
    <h3>🌀 經典颱風路徑</h3>
    <ul>
      <li><b>直撲穿心颱：</b>高速向西北西直插中央山脈，考驗瞬間閃避！</li>
      <li><b>西北颱：</b>掠過台灣北部海面，西北強風帶來驚人暴雨。</li>
      <li><b>迷走怪颱（韋恩、納莉、山陀兒）：</b>行蹤飄忽不定、原地打轉，甚至會來記回馬槍！</li>
      <li><b>鞍形場停滯：</b>在海面上停滯不動並持續吸取海溫熱量增大暴風半徑！</li>
      <li><b>追尾磁吸：</b>受副熱帶高壓導引氣流影響，死死鎖定台灣追擊！</li>
      <li><b>藤原效應：</b>當雙颱距離接近時，會產生互相牽引繞轉的共舞現象！</li>
    </ul>
    
    <h3>📊 資料來源與授權</h3>
    <p><b>地圖數據：</b>基於 Natural Earth 公共領域海岸線數據（高解析度 10m 台灣本島與離島群、50m 東亞陸塊），採 1:1 等角麥卡托投影無形變還原。</p>
    <p><b>颱風命名：</b>採用世界氣象組織（WMO）西北太平洋颱風命名表及台灣中央氣象署（CWA）官方繁體中文譯名。</p>
    <p><b>音效系統：</b>採用 Web Audio API 純程式合成技術（含海洋風暴粉紅噪音合成環境音），無需任何外部音訊檔案。</p>
    <p><b>原始致敬作品：</b>靈感源自日本經典《Typhoon Escape》（by lovewcycle），本專案已完整收錄其原始離線對照版本於 <a href="references/original-typhoon-escape/index.html" target="_blank" style="color: #00D2FF; text-decoration: underline;">references/original-typhoon-escape/</a>（點擊直接開新視窗對照體驗）。</p>
  </div>
  
  <div id="toast">已複製戰績到剪貼簿！</div>
</div>

<!-- Embedded East Asia & Taiwan Map Geometry -->
<script id="mapdata" type="application/json">
{map_json_str}
</script>

<script>
// Web Audio Synthesizer Engine
var audioCtx = null, soundEnabled = true;
var windNode = null, windGain = null, windFilter = null;

function initAudio() {{
  if (!audioCtx) {{
    try {{
      var AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) audioCtx = new AudioContext();
    }} catch (e) {{}}
  }}
  if (audioCtx && audioCtx.state === 'suspended') {{
    audioCtx.resume();
  }}
  if (audioCtx && !windNode && soundEnabled) {{
    startAmbientWind();
  }}
}}

function startAmbientWind() {{
  if (!audioCtx || !soundEnabled || windNode) return;
  try {{
    var bufferSize = audioCtx.sampleRate * 2.0;
    var buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    var output = buffer.getChannelData(0);
    var b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
    for (var i = 0; i < bufferSize; i++) {{
      var white = Math.random() * 2 - 1;
      b0 = 0.99886 * b0 + white * 0.0555179;
      b1 = 0.99332 * b1 + white * 0.0750759;
      b2 = 0.96900 * b2 + white * 0.1538520;
      b3 = 0.86650 * b3 + white * 0.3104856;
      b4 = 0.55000 * b4 + white * 0.5329522;
      b5 = -0.7616 * b5 - white * 0.0168980;
      output[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.11;
      b6 = white * 0.115926;
    }}
    windNode = audioCtx.createBufferSource();
    windNode.buffer = buffer;
    windNode.loop = true;
    
    windFilter = audioCtx.createBiquadFilter();
    windFilter.type = 'lowpass';
    windFilter.frequency.setValueAtTime(260, audioCtx.currentTime);
    
    windGain = audioCtx.createGain();
    windGain.gain.setValueAtTime(0.04, audioCtx.currentTime);
    
    windNode.connect(windFilter);
    windFilter.connect(windGain);
    windGain.connect(audioCtx.destination);
    windNode.start();
  }} catch(e) {{}}
}}

function updateAmbientWind(intensity) {{
  if (!windGain || !windFilter || !audioCtx) return;
  try {{
    var targetGain = soundEnabled && running && !paused ? (0.025 + intensity * 0.06) : 0.001;
    var targetFreq = 220 + intensity * 380;
    windGain.gain.linearRampToValueAtTime(targetGain, audioCtx.currentTime + 0.15);
    windFilter.frequency.linearRampToValueAtTime(targetFreq, audioCtx.currentTime + 0.15);
  }} catch(e) {{}}
}}

function stopAmbientWind() {{
  if (windGain && audioCtx) {{
    try {{ windGain.gain.linearRampToValueAtTime(0.001, audioCtx.currentTime + 0.15); }} catch(e) {{}}
  }}
}}

function playSiren() {{
  if (!soundEnabled || !audioCtx) return;
  try {{
    var osc = audioCtx.createOscillator();
    var gain = audioCtx.createGain();
    var now = audioCtx.currentTime;
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(460, now);
    osc.frequency.linearRampToValueAtTime(780, now + 0.35);
    osc.frequency.linearRampToValueAtTime(460, now + 0.7);
    gain.gain.setValueAtTime(0.001, now);
    gain.gain.linearRampToValueAtTime(0.12, now + 0.1);
    gain.gain.linearRampToValueAtTime(0.001, now + 0.7);
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.start(now); osc.stop(now + 0.75);
  }} catch(e) {{}}
}}

function playThunder() {{
  if (!soundEnabled || !audioCtx) return;
  try {{
    var now = audioCtx.currentTime;
    var bufferSize = audioCtx.sampleRate * 1.0;
    var buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    var data = buffer.getChannelData(0);
    for (var i = 0; i < bufferSize; i++) {{ data[i] = Math.random() * 2 - 1; }}
    var noise = audioCtx.createBufferSource();
    noise.buffer = buffer;
    var filter = audioCtx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(200, now);
    filter.frequency.exponentialRampToValueAtTime(40, now + 0.9);
    var gain = audioCtx.createGain();
    gain.gain.setValueAtTime(0.3, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.95);
    noise.connect(filter); filter.connect(gain); gain.connect(audioCtx.destination);
    noise.start(now); noise.stop(now + 1.0);
  }} catch(e) {{}}
}}

function playDing() {{
  if (!soundEnabled || !audioCtx) return;
  try {{
    var now = audioCtx.currentTime;
    [587.33, 880].forEach(function(freq, idx) {{
      var osc = audioCtx.createOscillator();
      var gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now + idx * 0.08);
      gain.gain.setValueAtTime(0.001, now + idx * 0.08);
      gain.gain.linearRampToValueAtTime(0.08, now + idx * 0.08 + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.08 + 0.35);
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.start(now + idx * 0.08); osc.stop(now + idx * 0.08 + 0.4);
    }});
  }} catch(e) {{}}
}}

function playDissipate() {{
  if (!soundEnabled || !audioCtx) return;
  try {{
    var now = audioCtx.currentTime;
    [523.25, 659.25, 783.99, 1046.5].forEach(function(freq, idx) {{
      var osc = audioCtx.createOscillator();
      var gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now + idx * 0.06);
      gain.gain.setValueAtTime(0.05, now + idx * 0.06);
      gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.06 + 0.22);
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.start(now + idx * 0.06); osc.stop(now + idx * 0.06 + 0.25);
    }});
  }} catch(e) {{}}
}}

// Sound Button UI
var soundBtn = document.getElementById('soundbtn');
soundBtn.onclick = function() {{
  initAudio();
  soundEnabled = !soundEnabled;
  soundBtn.textContent = soundEnabled ? '🔊' : '🔇';
  soundBtn.style.opacity = soundEnabled ? '1' : '0.6';
  if (!soundEnabled) stopAmbientWind();
  else if (running && !paused) startAmbientWind();
  showToast(soundEnabled ? '音效已開啟' : '音效已靜音');
}};

// Pause Button UI
var pauseBtn = document.getElementById('pausebtn');
pauseBtn.onclick = function() {{
  if (!running || over) return;
  paused = !paused;
  pauseBtn.textContent = paused ? '▶️' : '⏸️';
  if (!paused) {{
    last = performance.now();
    raf = requestAnimationFrame(loop);
    showToast('遊戲繼續');
  }} else {{
    showToast('遊戲已暫停');
  }}
}};

// Conformal Mercator Projection Settings (1:1 Aspect Ratio Guaranteed)
var cv = document.getElementById('cv'), ctx = cv.getContext('2d');
var W = 420, H = 720, M = 720, OX = 0, OY = 0, DPR = 1, SC = 1, TX = 0, TY = 0, VW = 0, VH = 0;
var CEN = 123.8, LONW = 22.0;

function wrap(lon) {{ while (lon < CEN - 180) lon += 360; while (lon >= CEN + 180) lon -= 360; return lon; }}
function merc(lat) {{ lat = Math.max(-85, Math.min(85, lat)) * Math.PI / 180; return Math.log(Math.tan(Math.PI / 4 + lat / 2)); }}
function invMerc(y) {{ return (2 * Math.atan(Math.exp(y)) - Math.PI / 2) * 180 / Math.PI; }}

var yCenterMerc = merc(23.6);
var ySpanRad = (H / W) * (LONW * Math.PI / 180);
var MY = yCenterMerc + ySpanRad / 2;
var MN = yCenterMerc - ySpanRad / 2;
var LATN = invMerc(MY);
var LATS = invMerc(MN);

function px(lon) {{ return W / 2 + (wrap(lon) - CEN) * W / LONW; }}
function py(lat) {{ return (MY - merc(lat)) / (MY - MN) * H; }}

// Central Mountain Range Ridge Points (護國神山脊線)
var SPINE_COORDS = [
  [121.85, 24.95], [121.65, 24.75], [121.52, 24.49], [121.44, 24.36],
  [121.42, 24.31], [121.34, 24.23], [121.28, 24.18], [121.33, 24.11],
  [121.26, 23.99], [121.19, 23.75], [121.05, 23.50], [120.91, 23.23],
  [120.76, 22.63], [120.75, 22.40], [120.72, 22.16], [120.85, 21.90]
];
var YUSHAN_COORD = [120.957, 23.470]; // 玉山主峰 3952m
var XUESHAN_COORD = [121.231, 24.383]; // 雪山主峰 3886m

// Precise Taiwanese Region Classifier (20+ Representative Landmarks)
function region(lon, lat) {{
  // 離島
  if (lon < 118.6 && lat > 24.0) return '金門群島';
  if (lat > 25.5) return '馬祖列島';
  if (lon < 119.8 && 23.0 <= lat && lat <= 23.9) return '澎湖群島';
  if (lon > 121.4 && 22.5 <= lat && lat <= 22.8) return '台東綠島';
  if (lon > 121.4 && 21.8 <= lat && lat <= 22.2) return '台東蘭嶼';
  if (lon < 120.45 && 22.3 <= lat && lat <= 22.45) return '屏東小琉球';
  if (lon >= 121.90 && lat >= 24.80 && lat <= 24.90) return '宜蘭頭城、礁溪';
  
  // 北部
  if (lat >= 25.15) return '基隆北海岸';
  if (lat >= 24.92 && lon >= 121.36 && lon <= 121.8) return '雙北都會區';
  if (lat >= 24.82 && lon > 121.75) return '宜蘭頭城、礁溪';
  if (lat >= 24.90 && lon < 121.36) return '桃園海岸';
  if (lat >= 24.45 && lat < 24.90 && lon <= 121.15) return '新竹、苗栗';
  if (lat >= 24.4 && lat < 24.85 && lon > 121.45) return '宜蘭蘇澳、南澳';
  
  // 中部
  if (lat >= 23.9 && lat < 24.45 && lon <= 120.8) return '台中港、彰化鹿港';
  if (lat >= 23.55 && lat < 24.3 && lon > 120.8 && lon < 121.35) return '南投中央山脈';
  if (lat >= 23.35 && lat < 23.9 && lon <= 120.6) return '雲林麥寮、嘉義布袋';
  
  // 東部
  if (lat >= 23.6 && lat < 24.4 && lon >= 121.35) return '花蓮太魯閣、花蓮港';
  if (lat >= 23.0 && lat < 23.6 && lon >= 121.15) return '台東成功、三仙台';
  if (lat >= 22.5 && lat < 23.0 && lon >= 120.95) return '台東市、知本';
  
  // 南部
  if (lat >= 22.88 && lat < 23.35 && lon <= 120.5) return '台南安平、七股';
  if (lat >= 22.45 && lat < 22.88 && lon <= 120.5) return '高雄旗津、高雄港';
  if (lat >= 22.1 && lat < 22.45 && lon <= 120.8) return '屏東枋寮、大鵬灣';
  if (lat < 22.1) return '恆春半島、墾丁鵝鑾鼻';
  
  return '台灣沿海';
}}

// 140 Official CWA Western North Pacific Typhoon Names (Traditional Chinese)
var NAMES = [
  '山陀兒','凱米','康芮','天兔','海葵','小犬','蘇拉','杜蘇芮','卡努','瑪娃',
  '奈格','尼伯特','莫拉克','韋恩','納莉','賀伯','達維','鴻雁','鴛鴦','布拉萬',
  '三巴','傑拉華','艾維尼','馬力斯','格美','派比安','瑪莉亞','山神','安比','悟空',
  '雲雀','珊珊','摩羯','麗琵','貝碧佳','普拉桑','蘇力','西馬隆','燕子','百里嘉',
  '潭美','銀杏','桃芝','萬宜','帕布','蝴蝶','聖帕','木恩','丹娜絲','百合',
  '韋帕','范斯高','竹節草','羅莎','白鹿','楊柳','玲玲','劍魚','藍湖','琵琶',
  '塔巴','米塔','哈吉貝','浣熊','博羅依','麥德姆','夏浪','娜克莉','風神','海鷗',
  '鳳凰','圓規','洛鞍','班朗','考雷','艾濤','瓦卡','杜鵑','舒力基','彩雲',
  '小熊','薔琵','煙花','查帕卡','盧碧','銀河','妮妲','奧麥斯','康森','燦都',
  '電母','蒲公英','獅子山','南修','瑪瑙','妮亞圖','馬勒卡','鮎魚','暹芭','艾利',
  '桑達','翠絲','木蘭','米雷','馬鞍','軒嵐諾','苗柏','南瑪都','塔拉斯','奧鹿',
  '玫瑰','洛克','桑卡','納沙','海棠','榕樹','帕卡','珊瑚','古超','泰利',
  '蘭恩','凡那比','辛樂克','提姆','碧利斯','象神','柯羅莎','蘇迪勒','梅姬','天鵝',
  '葛樂禮','道姬','寶發','桑美','波密拉','瓊安','賽洛瑪','黛納','芙瑞達','歐珀'
];
var nameIdx = Math.floor(Math.random() * NAMES.length);

// Game State Variables
var geo = null, twRings = [], twPts = [], spinePts = [], bodies = [];
var tw = null, ty = [], elapsed = 0, over = false, running = false, paused = false;
var spawnT = 0, vx = 0, vy = 0, last = 0, raf = null, tsp = 55, tyNo = 0, evadedCount = 0;
var hit = null, popupReady = true, bestDays = 0;
var START_DATE = new Date(2026, 6, 1); // 2026年7月1日

try {{
  bestDays = parseInt(localStorage.getItem('tw_typhoon_best') || '0', 10);
}} catch(e) {{}}
document.getElementById('bestdays').textContent = bestDays + ' 天';

function gameDate() {{
  var d = new Date(START_DATE);
  d.setDate(d.getDate() + Math.floor(elapsed));
  return d;
}}
function fmtDate(d) {{
  return d.getFullYear() + '年' + (d.getMonth() + 1) + '月' + d.getDate() + '日';
}}

function resize() {{
  DPR = window.devicePixelRatio || 1;
  VW = window.innerWidth; VH = window.innerHeight;
  cv.width = VW * DPR; cv.height = VH * DPR;
  SC = Math.min(VW / W, VH / H);
  TX = (VW - W * SC) / 2;
  TY = (VH - H * SC) / 2;
  if (tw) draw();
}}

function init() {{
  cancelAnimationFrame(raf);
  bodies.forEach(function(B) {{ B.ox = 0; B.oy = 0; B.vx = 0; B.vy = 0; }});
  tw = {{ x: px(121.0), y: py(23.6) }};
  ty = []; elapsed = 0; over = false; running = false; paused = false;
  spawnT = 0; tsp = 55; tyNo = 0; evadedCount = 0; hit = null; popupReady = true;
  ticker.innerHTML = ''; updateRows();
  document.getElementById('evadedcount').textContent = '0';
  document.getElementById('daycount').textContent = '第 1 天';
  document.getElementById('time').textContent = fmtDate(START_DATE);
  document.getElementById('pausebtn').textContent = '⏸️';
  
  // Cleanly reset popup elements
  document.getElementById('picon').textContent = '🇹🇼';
  document.getElementById('ptitle').textContent = '台灣大逃亡：颱風來啦！';
  document.getElementById('psub').textContent = '開著台灣島，在西北太平洋暴風陣中漂移求生！';
  document.getElementById('pstats').style.display = 'none';
  document.getElementById('res-title-wrap').style.display = 'none';
  document.getElementById('sharesection').style.display = 'none';
  document.getElementById('pbtn').textContent = '迎戰颱風季！發動台灣島！';
  
  stopAmbientWind();
  draw();
}}

function toward(t) {{ return Math.atan2(tw.y - t.y, tw.x - t.x); }}

// Typhoon Movement Patterns (台灣六大經典路徑)
var PATTERNS = [
  {{ name: '直撲穿心', segMin: 3.5, segMax: 6.0, jitter: 0.25, pull: 0.45, spd: 1.25, stall: 0, bias: 0, tag: '穿心直撲' }},
  {{ name: '西北颱', segMin: 3.0, segMax: 5.5, jitter: 0.20, pull: 0.25, spd: 1.15, stall: 0, bias: -0.35, tag: '西北颱' }},
  {{ name: '迷走怪颱', segMin: 0.8, segMax: 1.8, jitter: 2.20, pull: 0.25, spd: 0.85, stall: 0.35, bias: 0, tag: '迷走打轉' }},
  {{ name: '追尾鎖定', segMin: 1.5, segMax: 3.0, jitter: 0.50, pull: 0.85, spd: 0.95, stall: 0, bias: 0, tag: '追尾鎖定' }},
  {{ name: '鞍形停滯', segMin: 2.0, segMax: 4.0, jitter: 0.80, pull: 0.30, spd: 0.50, stall: 0.60, bias: 0, tag: '鞍形場停滯' }},
  {{ name: '急折轉向', segMin: 2.0, segMax: 3.5, jitter: 0.30, pull: 0.20, spd: 1.10, stall: 0, bias: 0.65, tag: '拋物轉向' }}
];

function spawn() {{
  tyNo++;
  var nm = NAMES[nameIdx % NAMES.length]; nameIdx++;
  
  // Realistic Western Pacific Spawn Locations
  // 65% from Philippine Sea / SE, 20% from South China Sea, 15% from East/NE
  var roll = Math.random(), x, y;
  if (roll < 0.65) {{
    x = W * 0.75 + Math.random() * (W * 0.45);
    y = H * 0.55 + Math.random() * (H * 0.45);
  }} else if (roll < 0.85) {{
    x = Math.random() * (W * 0.5);
    y = H + 50;
  }} else {{
    x = W + 50;
    y = Math.random() * (H * 0.5);
  }}
  
  var pat = PATTERNS[Math.floor(Math.random() * PATTERNS.length)];
  if (pat.name === '急折轉向') {{
    pat.bias = (Math.random() < 0.5 ? 1 : -1) * (0.4 + Math.random() * 0.4);
  }}
  
  var intRoll = Math.random();
  var intensity = intRoll < 0.3 ? '輕度颱風' : (intRoll < 0.75 ? '中度颱風' : '強烈颱風');
  var baseRadius = intensity === '強烈颱風' ? (M * 0.065 + Math.random() * M * 0.03) :
                   (intensity === '中度颱風' ? (M * 0.048 + Math.random() * M * 0.02) : (M * 0.035 + Math.random() * M * 0.015));
  
  var t = {{
    no: tyNo, name: nm, intensity: intensity, pat: pat,
    x: x, y: y,
    r: M * 0.018, rPeak: baseRadius,
    growT: 3 + Math.random() * 3,
    decay: false, entered: false,
    rot: Math.random() * Math.PI * 2,
    ang: 0,
    timer: pat.segMin + Math.random() * (pat.segMax - pat.segMin),
    trail: [[x, y]],
    life: 14 + Math.random() * 12,
    spd: pat.spd * (0.85 + Math.random() * 0.35),
    stalled: false,
    mountainHitCount: 0,
    mountainShredding: false,
    mountainNotified: false
  }};
  
  t.ang = toward(t) + (Math.random() - 0.5) * 0.6;
  setForecast(t);
  ty.push(t);
  
  playSiren();
  news('【警報】第 ' + tyNo + ' 號' + intensity + '『' + nm + '』生成！路徑預測屬『' + pat.tag + '』，請加強防颱！', 'red', '颱風警報');
}}

function setForecast(t) {{
  var v = t.stalled ? tsp * 0.15 : tsp * t.spd, T = t.timer, r;
  if (t.decay || t.life - T <= 5) r = t.r - t.rPeak * 0.12 * T;
  else r = Math.min(t.rPeak, t.r + t.rPeak / t.growT * T);
  t.fx = t.x + Math.cos(t.ang) * v * T;
  t.fy = t.y + Math.sin(t.ang) * v * T;
  t.fr = Math.max(M * 0.014, r) * 0.6;
}}

// Update Loop
function update(dt) {{
  if (over) {{
    dt *= 0.3; slideLand(dt);
    for (var i = ty.length - 1; i >= 0; i--) {{
      var t = ty[i];
      var v = t.stalled ? tsp * 0.15 : tsp * t.spd;
      t.x += Math.cos(t.ang) * v * dt; t.y += Math.sin(t.ang) * v * dt;
      t.rot += dt * 3.5;
    }}
    return;
  }}
  
  elapsed += dt;
  var days = Math.floor(elapsed);
  document.getElementById('daycount').textContent = '第 ' + (days + 1) + ' 天';
  document.getElementById('time').textContent = fmtDate(gameDate());
  
  // Taiwan Movement Speed
  var sp = M * 0.135;
  tw.x = Math.max(30, Math.min(W - 30, tw.x + vx * sp * dt));
  tw.y = Math.max(30, Math.min(H - 30, tw.y + vy * sp * dt));
  
  pushLand(dt);
  slideLand(dt);
  
  // Progressive difficulty (Typhoon speed & frequency rises)
  tsp = M * 0.095 + elapsed * M * 0.0038;
  
  // Fujiwhara Effect: mutual interaction between close typhoons
  for (var i = 0; i < ty.length; i++) {{
    for (var j = i + 1; j < ty.length; j++) {{
      var t1 = ty[i], t2 = ty[j];
      var d = Math.hypot(t2.x - t1.x, t2.y - t1.y);
      if (d < 160 && d > 15) {{
        var th = Math.atan2(t2.y - t1.y, t2.x - t1.x);
        var force = (160 - d) / 160 * 0.7 * dt;
        t1.x += Math.cos(th + Math.PI / 2) * force * tsp;
        t1.y += Math.sin(th + Math.PI / 2) * force * tsp;
        t2.x += Math.cos(th - Math.PI / 2) * force * tsp;
        t2.y += Math.sin(th - Math.PI / 2) * force * tsp;
      }}
    }}
  }}
  
  var closestTyphoonDist = 999;
  
  for (var i = ty.length - 1; i >= 0; i--) {{
    var t = ty[i], pt = t.pat;
    t.rot += dt * 4.5;
    t.timer -= dt;
    
    var distToTw = Math.hypot(tw.x - t.x, tw.y - t.y);
    if (distToTw < closestTyphoonDist) closestTyphoonDist = distToTw;
    
    if (t.timer <= 0) {{
      if (pt.stall > 0 && !t.stalled && Math.random() < pt.stall) {{
        t.stalled = true; t.timer = 1.2 + Math.random() * 1.8;
      }} else {{
        t.stalled = false;
        t.timer = pt.segMin + Math.random() * (pt.segMax - pt.segMin);
        var a = toward(t), d = a - t.ang;
        d = Math.atan2(Math.sin(d), Math.cos(d));
        t.ang += d * pt.pull + (Math.random() - 0.5) * pt.jitter + (pt.bias || 0);
      }}
      t.trail.push([t.x, t.y]);
      if (t.trail.length > 8) t.trail.shift();
      setForecast(t);
    }}
    
    var v = t.stalled ? tsp * 0.15 : tsp * t.spd;
    t.x += Math.cos(t.ang) * v * dt;
    t.y += Math.sin(t.ang) * v * dt;
    t.life -= dt;
    
    // Central Mountain Range weakening effect (護國神山防衛斬斷暴風圈)
    var distToSpineMin = 1e9;
    for (var s = 0; s < spinePts.length; s++) {{
      var sd = Math.hypot(tw.x + spinePts[s][0] - t.x, tw.y + spinePts[s][1] - t.y);
      if (sd < distToSpineMin) distToSpineMin = sd;
    }}
    t.mountainShredding = false;
    if (distToSpineMin < t.r * 1.05) {{
      t.mountainShredding = true;
      t.r -= t.rPeak * 0.35 * dt; // mountainous terrain aggressively shreds circulation
      t.mountainHitCount += dt;
      if (t.mountainHitCount >= 0.35 && !t.mountainNotified) {{
        t.mountainNotified = true;
        news('【護國神山防衛】中央山脈強勢斬斷『' + t.name + '』環流，強度驟降！', 'blue', '護國神山');
        playDissipate();
      }}
    }}
    
    if (t.decay || t.life <= 5) {{
      t.r -= t.rPeak * 0.14 * dt;
    }} else if (t.r < t.rPeak) {{
      t.r = Math.min(t.rPeak, t.r + t.rPeak / t.growT * dt);
    }} else if (Math.random() < dt * 0.05) {{
      t.decay = true;
    }}
    
    // Dissipation or off-screen exit
    if (t.r <= M * 0.012 || t.life <= 0) {{
      ty.splice(i, 1);
      evadedCount++;
      document.getElementById('evadedcount').textContent = evadedCount;
      news('【解除】第 ' + t.no + ' 號颱風『' + t.name + '』減弱為熱帶性低氣壓（TD）！', 'yellow', '消滅');
      playDissipate();
    }} else if (!t.entered && t.x > 0 && t.x < W && t.y > 0 && t.y < H) {{
      t.entered = true;
    }} else if ((t.entered && (t.x < -t.r || t.x > W + t.r || t.y < -t.r || t.y > H + t.r)) ||
               t.x < -140 || t.x > W + 140 || t.y < -140 || t.y > H + 140) {{
      ty.splice(i, 1);
      evadedCount++;
      document.getElementById('evadedcount').textContent = evadedCount;
      news('【遠離】第 ' + t.no + ' 號颱風『' + t.name + '』遠離台灣，解除海上陸上警報！', 'yellow', '解除警報');
      playDissipate();
    }}
  }}
  
  // Update ambient storm wind intensity based on nearest typhoon proximity
  var windIntensity = Math.max(0, Math.min(1, (240 - closestTyphoonDist) / 240));
  updateAmbientWind(windIntensity);
  
  // Typhoon Spawning Schedule
  spawnT += dt;
  var interval = Math.max(1.8, 4.2 - elapsed * 0.06);
  if (spawnT > interval && ty.length < 6) {{
    spawnT = 0;
    spawn();
  }}
  
  // Random Taiwan Cultural / Weather Memes Ticker
  if (Math.random() < dt * 0.07) {{
    triggerCulturalNews();
  }}
  
  // Collision Detection with Taiwan Island Points
  for (var i = 0; i < ty.length && !over; i++) {{
    var t = ty[i];
    var coreRadius = t.r * 0.52; // Destructive eyewall core
    for (var j = 0; j < twPts.length; j++) {{
      var qx = tw.x + twPts[j][0], qy = tw.y + twPts[j][1];
      if (Math.hypot(qx - t.x, qy - t.y) < coreRadius) {{
        over = true;
        hit = {{
          no: t.no, name: t.name, intensity: t.intensity,
          region: region(twPts[j][2], twPts[j][3])
        }};
        popupReady = false;
        release();
        playThunder();
        stopAmbientWind();
        setTimeout(function() {{
          popupReady = true; running = false;
          showGameOver();
          draw();
        }}, 1400);
        break;
      }}
    }}
  }}
}}

// Random Taiwanese weather & lifestyle tickers
var CULTURAL_NEWS = [
  {{ msg: '【停班停課】北北基桃宣布全天停班停課！各大 KTV 官網湧入百萬人塞爆！', col: 'blue', tag: '颱風假' }},
  {{ msg: '【菜價速報】全聯高麗菜一顆標價 280 元！民眾驚呼：買牛排比較划算！', col: 'yellow', tag: '民生快訊' }},
  {{ msg: '【水庫大進補】石門水庫與曾文水庫水位達 100%，實施調節性放水！', col: 'blue', tag: '水庫進補' }},
  {{ msg: '【外送公告】因應暴風圈擴大，各大外送平台全面暫停外送服務！', col: 'red', tag: '外送暫停' }},
  {{ msg: '【賣場搶購】大批民眾湧入超市搶購泡麵，花雕雞麵與統一肉燥麵已被掃空！', col: 'blue', tag: '超市現況' }},
  {{ msg: '【氣象專家】鄭明典提醒：東南部沉降焚風飆上 38 度，出門注意補水！', col: 'yellow', tag: '氣象特報' }},
  {{ msg: '【氣象迷因】韋恩：聽說有人在比誰的路徑最奇怪？納莉：你退後讓我來！', col: 'blue', tag: '氣象迷因' }}
];
var cNewsIdx = 0;
function triggerCulturalNews() {{
  var item = CULTURAL_NEWS[cNewsIdx % CULTURAL_NEWS.length];
  cNewsIdx++;
  news(item.msg, item.col, item.tag);
}}

// Drawing Radar & Map Scene
function draw() {{
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  ctx.fillStyle = '#0B162C';
  ctx.fillRect(0, 0, VW, VH);
  
  ctx.setTransform(DPR * SC, 0, 0, DPR * SC, TX * DPR, TY * DPR);
  ctx.save();
  ctx.beginPath(); ctx.rect(0, 0, W, H); ctx.clip();
  
  // Ocean Background
  var oceanGrad = ctx.createLinearGradient(0, 0, W, H);
  oceanGrad.addColorStop(0, '#0F2449');
  oceanGrad.addColorStop(0.6, '#132C5B');
  oceanGrad.addColorStop(1, '#0C1C3C');
  ctx.fillStyle = oceanGrad;
  ctx.fillRect(0, 0, W, H);
  
  // Grid Lines (經緯度刻度線)
  ctx.strokeStyle = 'rgba(0, 210, 255, 0.12)';
  ctx.lineWidth = 0.8;
  ctx.setLineDash([4, 4]);
  [115, 120, 125, 130, 135].forEach(function(lon) {{
    var x = px(lon);
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
  }});
  [10, 15, 20, 25, 30, 35].forEach(function(lat) {{
    var y = py(lat);
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
  }});
  ctx.setLineDash([]);
  
  // Draw Surrounding Land Bodies (China coast, Philippines, Japan/Ryukyu)
  ctx.fillStyle = '#395342';
  ctx.strokeStyle = '#5E886C';
  ctx.lineWidth = 0.8;
  for (var b = 0; b < bodies.length; b++) {{
    var B = bodies[b];
    ctx.save();
    ctx.translate(B.ox, B.oy);
    ctx.fill(B.path);
    ctx.stroke(B.path);
    ctx.restore();
  }}
  
  // Check if any typhoon is currently shredding against the mountains
  var isShreddingActive = false;
  for (var i = 0; i < ty.length; i++) {{
    if (ty[i].mountainShredding) {{ isShreddingActive = true; break; }}
  }}
  
  // Draw Taiwan Island (Player Ship)
  if (twRings.length) {{
    ctx.save();
    ctx.translate(tw.x, tw.y);
    
    // Coastline Glow
    ctx.shadowColor = isShreddingActive ? 'rgba(0, 210, 255, 0.75)' : 'rgba(76, 175, 80, 0.45)';
    ctx.shadowBlur = isShreddingActive ? 16 : 10;
    
    // Taiwan Island Fill & Stroke
    ctx.fillStyle = '#4CAF50';
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 1.3;
    for (var r = 0; r < twRings.length; r++) {{
      var ring = twRings[r];
      ctx.beginPath();
      for (var i = 0; i < ring.length; i++) {{
        ctx[i ? 'lineTo' : 'moveTo'](ring[i][0], ring[i][1]);
      }}
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }}
    ctx.shadowBlur = 0;
    
    // Central Mountain Range Spine (護國神山綠脈與防衛結界)
    if (spinePts.length > 1) {{
      ctx.strokeStyle = '#27622A';
      ctx.lineWidth = 3.6;
      ctx.lineCap = 'round';
      ctx.beginPath();
      for (var s = 0; s < spinePts.length; s++) {{
        ctx[s ? 'lineTo' : 'moveTo'](spinePts[s][0], spinePts[s][1]);
      }}
      ctx.stroke();
      
      ctx.strokeStyle = isShreddingActive ? '#00D2FF' : '#7BC67E';
      ctx.lineWidth = isShreddingActive ? 2.4 : 1.4;
      if (isShreddingActive) {{
        ctx.shadowColor = '#00D2FF';
        ctx.shadowBlur = 12;
      }}
      ctx.stroke();
      ctx.shadowBlur = 0;
    }}
    
    // Yushan Summit Marker (玉山主峰 3952m)
    var yx = (px(YUSHAN_COORD[0]) - px(121.0)) * 1.35;
    var yy = (py(YUSHAN_COORD[1]) - py(23.6)) * 1.35;
    ctx.fillStyle = isShreddingActive ? '#00D2FF' : '#FFD23F';
    ctx.beginPath();
    ctx.moveTo(yx, yy - 5.0);
    ctx.lineTo(yx + 4.0, yy + 3.5);
    ctx.lineTo(yx - 4.0, yy + 3.5);
    ctx.closePath();
    ctx.fill();
    
    ctx.restore();
  }}
  
  // Draw Typhoons (CWA Radar Reflectivity Style)
  for (var i = 0; i < ty.length; i++) {{
    var t = ty[i];
    
    // Historic Track Trail
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.65)';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([]);
    ctx.beginPath();
    for (var k = 0; k < t.trail.length; k++) {{
      ctx[k ? 'lineTo' : 'moveTo'](t.trail[k][0], t.trail[k][1]);
    }}
    ctx.lineTo(t.x, t.y);
    ctx.stroke();
    
    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
    for (var k = 0; k < t.trail.length; k++) {{
      ctx.beginPath();
      ctx.arc(t.trail[k][0], t.trail[k][1], 2.2, 0, Math.PI * 2);
      ctx.fill();
    }}
    
    // CWA 72h Forecast Cone (潛勢預報虛線與誤差圈)
    var fx = t.fx, fy = t.fy, len = Math.hypot(fx - t.x, fy - t.y);
    var rs = t.r * 0.52, rw = t.fr, rf = rw * 0.5;
    ctx.setLineDash([4, 4]);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.85)';
    ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.moveTo(t.x, t.y); ctx.lineTo(fx, fy); ctx.stroke();
    ctx.beginPath(); ctx.arc(fx, fy, rf, 0, Math.PI * 2); ctx.stroke();
    
    // Expanding Error Circle
    ctx.setLineDash([]);
    ctx.strokeStyle = 'rgba(255, 60, 60, 0.7)';
    ctx.lineWidth = 1.3;
    ctx.beginPath(); ctx.arc(fx, fy, rw, 0, Math.PI * 2); ctx.stroke();
    
    if (len > rw - rs) {{
      var th = Math.atan2(fy - t.y, fx - t.x);
      var al = Math.acos((rs - rw) / len);
      ctx.beginPath();
      for (var sg = -1; sg <= 1; sg += 2) {{
        var a2 = th + sg * al;
        ctx.moveTo(t.x + rs * Math.cos(a2), t.y + rs * Math.sin(a2));
        ctx.lineTo(fx + rw * Math.cos(a2), fy + rw * Math.sin(a2));
      }}
      ctx.stroke();
    }}
    
    // Forecast Waypoint
    ctx.fillStyle = '#FFFFFF';
    ctx.beginPath(); ctx.arc(fx, fy, 2.5, 0, Math.PI * 2); ctx.fill();
    
    // Outer 7-level Gale Warning Radius (7級風暴風圈)
    ctx.fillStyle = t.mountainShredding ? 'rgba(0, 210, 255, 0.25)' : 'rgba(255, 215, 0, 0.22)';
    ctx.strokeStyle = t.mountainShredding ? '#00D2FF' : '#FFE000';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([5, 4]);
    ctx.beginPath(); ctx.arc(t.x, t.y, t.r, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    ctx.setLineDash([]);
    
    // Inner 10-level Storm Core / Eyewall (10級風暴風圈)
    var coreGrad = ctx.createRadialGradient(t.x, t.y, t.r * 0.15, t.x, t.y, t.r * 0.55);
    coreGrad.addColorStop(0, 'rgba(153, 0, 153, 0.75)'); // Purple eyewall
    coreGrad.addColorStop(0.5, 'rgba(235, 30, 45, 0.8)'); // Red rainband
    coreGrad.addColorStop(1, 'rgba(255, 140, 0, 0.75)'); // Orange band
    ctx.fillStyle = coreGrad;
    ctx.strokeStyle = '#E61E2D';
    ctx.lineWidth = 1.6;
    ctx.beginPath(); ctx.arc(t.x, t.y, t.r * 0.52, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    
    // Rotating Cyclonic Rainbands (逆時針旋轉螺旋雨帶)
    ctx.save();
    ctx.translate(t.x, t.y);
    ctx.rotate(t.rot);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
    ctx.lineWidth = 2.0;
    for (var a = 0; a < 3; a++) {{
      ctx.beginPath();
      var baseA = a * (Math.PI * 2 / 3);
      for (var st = 0; st < 10; st++) {{
        var curA = baseA - st * 0.25;
        var curR = (t.r * 0.15) + (st / 10) * (t.r * 0.35);
        var rx = Math.cos(curA) * curR, ry = Math.sin(curA) * curR;
        ctx[st ? 'lineTo' : 'moveTo'](rx, ry);
      }}
      ctx.stroke();
    }}
    
    // Calm Typhoon Eye (颱風眼)
    ctx.fillStyle = '#0F2449';
    ctx.beginPath(); ctx.arc(0, 0, Math.max(3, t.r * 0.12), 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#FFFFFF';
    ctx.lineWidth = 1.2;
    ctx.stroke();
    ctx.restore();
    
    // Typhoon Label
    ctx.font = 'bold 11px system-ui, sans-serif';
    ctx.fillStyle = '#FFFFFF';
    ctx.shadowColor = 'rgba(0,0,0,0.85)';
    ctx.shadowBlur = 4;
    ctx.fillText(t.no + '號 ' + t.name, t.x + t.r * 0.55 + 6, t.y + 4);
    ctx.shadowBlur = 0;
  }}
  
  ctx.restore();
}}

// Ticker News Engine
var ticker = document.getElementById('ticker');
function updateRows() {{
  document.documentElement.style.setProperty('--rows', ticker.children.length);
}}
function news(msg, color, tag) {{
  while (ticker.children.length >= 2) {{
    ticker.firstElementChild.remove();
  }}
  var row = document.createElement('div');
  row.className = 'row ' + color;
  row.innerHTML = '<div class="tag">' + tag + '</div><div class="track"><div class="ttext"></div></div>';
  var tt = row.querySelector('.ttext'), tr = row.querySelector('.track');
  tt.textContent = msg;
  ticker.appendChild(row);
  updateRows();
  playDing();
  
  var dist = (tr.clientWidth || 320) + (tt.offsetWidth || 280) + 30;
  tt.style.setProperty('--dist', -dist + 'px');
  tt.style.animationDuration = Math.max(7, dist / 85) + 's';
  tt.addEventListener('animationend', function() {{
    row.remove(); updateRows();
  }});
}}

// Game Loop
function loop(now) {{
  if (!running || paused) return;
  var dt = Math.min(0.05, (now - last) / 1000);
  last = now;
  update(dt);
  draw();
  raf = requestAnimationFrame(loop);
}}

// Title Calculation based on Survived Days
function getEvaluationTitle(days) {{
  if (days < 6) return '【泡麵還沒買好】';
  if (days < 16) return '【中央山脈實習生】';
  if (days < 30) return '【颱風假精算師】';
  if (days < 50) return '【護國神山防衛隊長】';
  if (days < 75) return '【開著台灣島漂移的航海王】';
  return '【太平洋不沉航母．台灣之神】';
}}

// Game Over Modal Handling
function showGameOver() {{
  var pop = document.getElementById('popup');
  var days = Math.floor(elapsed);
  
  if (days > bestDays) {{
    bestDays = days;
    try {{ localStorage.setItem('tw_typhoon_best', bestDays.toString()); }} catch(e) {{}}
    document.getElementById('bestdays').textContent = bestDays + ' 天';
  }}
  
  document.getElementById('picon').textContent = '💥';
  document.getElementById('ptitle').textContent = '颱風登陸！風雨肆虐全台！';
  document.getElementById('psub').textContent = '面對大自然的狂暴威力，台灣島光榮迎戰到底！';
  
  document.getElementById('pstats').style.display = 'block';
  document.getElementById('res-days').textContent = days + ' 天';
  document.getElementById('res-evaded').textContent = evadedCount + ' 個';
  document.getElementById('res-date').textContent = fmtDate(gameDate());
  document.getElementById('res-hit').textContent = '第 ' + hit.no + ' 號' + hit.intensity + '『' + hit.name + '』於【' + hit.region + '】暴力登陸！';
  
  document.getElementById('res-title-wrap').style.display = 'block';
  document.getElementById('res-title').textContent = getEvaluationTitle(days);
  
  document.getElementById('pbtn').textContent = '再戰下一個夏天（重新開始）';
  document.getElementById('sharesection').style.display = 'block';
  pop.className = '';
}}

// Toast Notification
function showToast(msg) {{
  var t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'show';
  setTimeout(function() {{ t.className = ''; }}, 2200);
}}

// Social Share Generators
function generateShareText() {{
  var days = Math.floor(elapsed);
  var title = getEvaluationTitle(days);
  return '🌊【台灣大逃亡：颱風來啦！】\\n' +
         '我駕駛整座台灣島在西北太平洋狂暴漂移，在颱風季堅守了 ' + days + ' 天！\\n' +
         '閃避了 ' + evadedCount + ' 個強烈颱風，榮獲評級：' + title + '！\\n' +
         '第 ' + hit.no + ' 號颱風『' + hit.name + '』於【' + hit.region + '】登陸。\\n\\n' +
         '#台灣大逃亡 #颱風エスケープ #護國神山';
}}

function fallbackCopy(text) {{
  try {{
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast('✅ 戰報成績已複製到剪貼簿！');
  }} catch(e) {{
    showToast('戰報已產生！');
  }}
}}

document.getElementById('copybtn').onclick = function() {{
  var text = generateShareText();
  if (navigator.clipboard && navigator.clipboard.writeText) {{
    navigator.clipboard.writeText(text).then(function() {{
      showToast('✅ 戰報成績已複製到剪貼簿！');
    }}).catch(function() {{
      fallbackCopy(text);
    }});
  }} else {{
    fallbackCopy(text);
  }}
}};

document.getElementById('threadbtn').onclick = function() {{
  var text = generateShareText();
  window.open('https://threads.net/intent/post?text=' + encodeURIComponent(text), '_blank');
}};

document.getElementById('xbtn').onclick = function() {{
  var text = generateShareText();
  window.open('https://x.com/intent/post?text=' + encodeURIComponent(text), '_blank');
}};

document.getElementById('linebtn').onclick = function() {{
  var text = generateShareText();
  window.open('https://line.me/R/msg/text/?' + encodeURIComponent(text), '_blank');
}};

// Menu Open/Close
document.getElementById('menubtn').onclick = function() {{
  document.getElementById('menu').className = 'open';
}};
document.getElementById('menuclose').onclick = function() {{
  document.getElementById('menu').className = '';
}};

// Start Button
var pbtn = document.getElementById('pbtn');
pbtn.onclick = function() {{
  initAudio();
  if (over) init();
  if (running) return;
  running = true;
  document.getElementById('popup').className = 'hidden';
  spawn();
  startAmbientWind();
  last = performance.now();
  raf = requestAnimationFrame(loop);
}};

// Controls: Virtual Joystick & Dragging
var pad = document.getElementById('pad'), knob = document.getElementById('knob'), wrapEl = document.getElementById('wrap');
var active = false, pid = null, cx0 = 0, cy0 = 0, KM = 40, KR = 40;

function setKnob(ex, ey) {{
  var dx = ex - cx0, dy = ey - cy0, d = Math.hypot(dx, dy);
  if (d > KR) {{ dx = dx / d * KR; dy = dy / d * KR; }}
  vx = dx / KR; vy = dy / KR;
  knob.style.left = (KM + dx) + 'px';
  knob.style.top = (KM + dy) + 'px';
}}

function release() {{
  active = false; pid = null; vx = 0; vy = 0;
  knob.style.left = KM + 'px'; knob.style.top = KM + 'px';
}}

wrapEl.addEventListener('pointerdown', function(e) {{
  if (over || e.target.closest('#popup') || e.target.closest('.top-btns') || e.target.closest('#menu') || active) return;
  initAudio();
  active = true; pid = e.pointerId;
  wrapEl.setPointerCapture(e.pointerId);
  if (e.target.closest('#pad')) {{
    var r = pad.getBoundingClientRect();
    cx0 = r.left + r.width / 2; cy0 = r.top + r.height / 2;
  }} else {{
    cx0 = e.clientX; cy0 = e.clientY;
  }}
  setKnob(e.clientX, e.clientY);
  e.preventDefault();
}});

wrapEl.addEventListener('pointermove', function(e) {{
  if (active && e.pointerId === pid) setKnob(e.clientX, e.clientY);
}});
wrapEl.addEventListener('pointerup', function(e) {{ if (e.pointerId === pid) release(); }});
wrapEl.addEventListener('pointercancel', function(e) {{ if (e.pointerId === pid) release(); }});

// Keyboard Controls (WASD, Arrows, Space, P)
var keys = {{}};
function keyVel() {{
  vx = (keys.ArrowRight || keys.d || keys.D ? 1 : 0) - (keys.ArrowLeft || keys.a || keys.A ? 1 : 0);
  vy = (keys.ArrowDown || keys.s || keys.S ? 1 : 0) - (keys.ArrowUp || keys.w || keys.W ? 1 : 0);
}}
window.addEventListener('keydown', function(e) {{
  initAudio();
  if (e.code === 'Space') {{
    e.preventDefault();
    if (!running || over) {{
      pbtn.click();
    }} else {{
      pauseBtn.click();
    }}
    return;
  }}
  if (e.key === 'p' || e.key === 'P') {{
    e.preventDefault();
    if (running && !over) pauseBtn.click();
    return;
  }}
  if (over || paused) return;
  keys[e.key] = true;
  keyVel();
}});
window.addEventListener('keyup', function(e) {{
  keys[e.key] = false;
  keyVel();
}});

// Unlock audio on any first gesture
['click', 'touchstart', 'touchend', 'pointerdown'].forEach(function(evt) {{
  window.addEventListener(evt, function() {{
    initAudio();
  }}, {{ once: true }});
}});

// Map Construction & Collision System
function buildMap() {{
  twRings = []; twPts = []; bodies = []; spinePts = [];
  var K = 1.35;
  var CX = px(121.0), CY = py(23.6);
  
  // Build Taiwan Island Geometry
  geo.tw.forEach(function(ring) {{
    var out = [];
    ring.forEach(function(c) {{
      var rx = (px(c[0]) - CX) * K;
      var ry = (py(c[1]) - CY) * K;
      out.push([rx, ry, c[0], c[1]]);
    }});
    twRings.push(out);
    twPts = twPts.concat(out);
  }});
  
  // Build Central Mountain Range Spine Points
  SPINE_COORDS.forEach(function(c) {{
    spinePts.push([(px(c[0]) - CX) * K, (py(c[1]) - CY) * K]);
  }});
  
  // Build Surrounding East Asian Land Bodies
  geo.land.forEach(function(ring) {{
    var path = new Path2D(), outer = [], cur = [];
    var minX = 1e9, minY = 1e9, maxX = -1e9, maxY = -1e9;
    var prev = null;
    
    ring.forEach(function(c) {{
      var lon = wrap(c[0]), x = px(lon), y = py(c[1]);
      if (prev === null || Math.abs(lon - prev) > 180) {{
        if (prev !== null) path.closePath();
        path.moveTo(x, y);
        cur = []; outer.push(cur);
      }} else {{
        path.lineTo(x, y);
      }}
      prev = lon;
      cur.push([x, y]);
      if (x < minX) minX = x; if (x > maxX) maxX = x;
      if (y < minY) minY = y; if (y > maxY) maxY = y;
    }});
    path.closePath();
    outer = outer.filter(function(r) {{ return r.length > 2; }});
    bodies.push({{
      path: path, outer: outer,
      minX: minX, minY: minY, maxX: maxX, maxY: maxY,
      ox: 0, oy: 0, vx: 0, vy: 0
    }});
  }});
}}

function inPoly(pt, ring) {{
  var x = pt[0], y = pt[1], inside = false;
  for (var i = 0, j = ring.length - 1; i < ring.length; j = i++) {{
    var xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1];
    if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) inside = !inside;
  }}
  return inside;
}}

function pushLand(dt) {{
  var spd = M * 0.125;
  for (var b = 0; b < bodies.length; b++) {{
    var B = bodies[b], sx = 0, sy = 0, n = 0;
    if (tw.x + 120 < B.minX + B.ox || tw.x - 120 > B.maxX + B.ox ||
        tw.y + 120 < B.minY + B.oy || tw.y - 120 > B.maxY + B.oy) continue;
    for (var j = 0; j < twPts.length; j++) {{
      var q = [tw.x + twPts[j][0] - B.ox, tw.y + twPts[j][1] - B.oy];
      if (q[0] < B.minX || q[0] > B.maxX || q[1] < B.minY || q[1] > B.maxY) continue;
      for (var r = 0; r < B.outer.length; r++) {{
        if (inPoly(q, B.outer[r])) {{
          sx += twPts[j][0]; sy += twPts[j][1]; n++; break;
        }}
      }}
    }}
    if (n) {{
      var d = Math.hypot(sx, sy) || 1;
      B.vx = sx / d * spd; B.vy = sy / d * spd;
    }}
  }}
}}

function slideLand(dt) {{
  var k = Math.pow(0.12, dt);
  for (var b = 0; b < bodies.length; b++) {{
    var B = bodies[b];
    if (!B.vx && !B.vy) continue;
    B.ox += B.vx * dt; B.oy += B.vy * dt;
    B.vx *= k; B.vy *= k;
    if (Math.abs(B.vx) < 0.5 && Math.abs(B.vy) < 0.5) {{ B.vx = 0; B.vy = 0; }}
  }}
}}

// Initialize Map & Start
window.addEventListener('resize', resize);
(function() {{
  try {{
    var txt = document.getElementById('mapdata').textContent.trim();
    geo = JSON.parse(txt);
    buildMap();
    resize();
    init();
  }} catch(e) {{
    console.error('Failed to parse map data', e);
  }}
}})();
</script>
</body>
</html>
'''

with open(INDEX_HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'Successfully built index.html! Size: {os.path.getsize(INDEX_HTML_PATH)} bytes')
