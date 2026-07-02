import streamlit as st
import random

# --- 職業データの定義 ---
JOB_STATS = {
    "学生": {"salary": 0, "luck_bonus": 0},
    "サラリーマン": {"salary": 20, "luck_bonus": 0},
    "起業家": {"salary": 50, "luck_bonus": -20},
    "公務員": {"salary": 10, "luck_bonus": 10},
    "医者": {"salary": 40, "luck_bonus": 5},
    "芸術家": {"salary": 15, "luck_bonus": -10},
    "スポーツ選手": {"salary": 30, "luck_bonus": -5},
    "インフルエンサー": {"salary": 25, "luck_bonus": -15},
    "投資家": {"salary": 5, "luck_bonus": 5},
    "冒険家": {"salary": 5, "luck_bonus": 15}
}

# --- ページ設定とスマホ向けCSS ---
st.set_page_config(page_title="Life Quest 2026", page_icon="🎲", layout="centered")

st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 60px; font-size: 18px; border-radius: 15px; background-color: #4F46E5; color: white; }
    .status-card { padding: 20px; border-radius: 15px; background-color: #f8fafc; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ゲームデータ ---
BOARD_DATA = {
    0: {"text": "スタート！希望に満ちた朝。", "img": "images/akari1.png"},
    5: {"text": "【運命の分かれ道】職業選択マス", "img": "images/akari2.png", "type": "checkpoint"},
    12: {"text": "【運命の分かれ道】結婚選択", "img": "images/akari3.png", "type": "checkpoint"},
    20: {"text": "ゴール！", "img": "images/akari4.png"}
}
CHECKPOINTS = [5, 12]

# --- 初期化 ---
if 'pos' not in st.session_state:
    st.session_state.update({'pos': 0, 'money': 100, 'job': "学生", 'partner': "独身", 'log': [], 'waiting_choice': False})

st.title("🎲 Life Quest 2026")

# ステータス表示
with st.container():
    st.markdown(f"""
    <div class="status-card">
        <b>職業:</b> {st.session_state.job} | <b>状況:</b> {st.session_state.partner}<br>
        <b>所持金:</b> {st.session_state.money}万円
    </div>
    """, unsafe_allow_html=True)

# イベント表示
current_cell = BOARD_DATA.get(st.session_state.pos, {"text": "平凡な日常。", "img": "images/akari5.png"})
st.image(current_cell["img"], width=150)
st.subheader(current_cell["text"])

# --- ロジック ---
if st.session_state.waiting_choice:
    if st.session_state.pos == 5:
        st.write("職業を選択してください")
        # 3列にボタンを配置してスマホでも選びやすく
        cols = st.columns(3)
        jobs = list(JOB_STATS.keys())[1:] # 学生以外を表示
        for i, job in enumerate(jobs):
            if cols[i % 3].button(job):
                st.session_state.job = job
                st.session_state.waiting_choice = False
                st.rerun()
    elif st.session_state.pos == 12:
        if st.button("結婚する（費用30万）"):
            st.session_state.partner = "既婚"
            st.session_state.money -= 30
            st.session_state.waiting_choice = False
            st.rerun()
        if st.button("独身を貫く"):
            st.session_state.waiting_choice = False
            st.rerun()

else:
    if st.button("サイコロを振る！"):
        roll = random.randint(1, 6)
        next_pos = min(st.session_state.pos + roll, 20)
        
        # 職業補正の適用（収入イベント）
        stats = JOB_STATS[st.session_state.job]
        salary = stats["salary"] + random.randint(-5, stats["luck_bonus"])
        st.session_state.money += salary
        
        # チェックポイント判定
        for cp in CHECKPOINTS:
            if st.session_state.pos < cp <= next_pos:
                next_pos = cp
                st.session_state.waiting_choice = True
                break
        
        st.session_state.pos = next_pos
        st.session_state.log.append(f"進んだ！(+{salary}万円)")
        # ゴール判定（ロジック内の既存のゴール判定をこれに置き換えてください）
        if st.session_state.pos >= 20:
            st.balloons()
            # 最終結果の表示
            st.success(f"""
            🎉 **ゴール！あなたの人生の結果**
            - **職業:** {st.session_state.job}
            - **状況:** {st.session_state.partner}
            - **最終資産:** {st.session_state.money}万円
            """)
            
            # リセットボタン
            if st.button("もう一度遊ぶ"):
                st.session_state.update({
                    'pos': 0, 'money': 100, 'job': "学生", 
                    'partner': "独身", 'log': [], 'waiting_choice': False
                })
                st.rerun()

# 履歴
for m in reversed(st.session_state.log[-3:]): st.caption(m)
