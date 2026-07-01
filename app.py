import streamlit as st
import random

# --- ページ設定とスマホ向けCSS ---
st.set_page_config(page_title="Life Quest 2026", page_icon="🎲", layout="centered")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px;
        border-radius: 15px;
        background-color: #4F46E5;
        color: white;
    }
    .status-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ゲームデータ定義 ---
# マスごとのデータ (画像はサンプルURL。実際には自前の画像パスに変更可能)
BOARD_DATA = {
    0: {"text": "スタート！希望に満ちた朝。", "img": "https://cdn-icons-png.flaticon.com/512/3062/3062634.png"},
    1: {"text": "近所の猫と仲良くなった。", "img": "https://cdn-icons-png.flaticon.com/512/616/616408.png", "money": 0},
    2: {"text": "資格試験に合格！", "img": "https://cdn-icons-png.flaticon.com/512/2991/2991148.png", "money": 10},
    3: {"text": "財布を落としてしまった...", "img": "https://cdn-icons-png.flaticon.com/512/2919/2919736.png", "money": -5},
    4: {"text": "初任給が出た！", "img": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png", "money": 20},
    5: {"text": "【運命の分かれ道】職業選択マス", "img": "https://cdn-icons-png.flaticon.com/512/1063/1063376.png", "type": "checkpoint"},
    6: {"text": "仕事で大きな成果を上げた！", "img": "https://cdn-icons-png.flaticon.com/512/3112/3112946.png", "money": 30},
    # ... 中略 (本来は全てのマスを定義)
    12: {"text": "【運命の分かれ道】結婚・独身選択", "img": "https://cdn-icons-png.flaticon.com/512/2525/2525143.png", "type": "checkpoint"},
    20: {"text": "ゴール！最高の人生だった！", "img": "https://cdn-icons-png.flaticon.com/512/3112/3112946.png"}
}

CHECKPOINTS = [5, 12] # 必ず止まるマス

# --- セッション状態の初期化 ---
if 'pos' not in st.session_state:
    st.session_state.update({'pos': 0, 'money': 100, 'job': "学生", 'partner': "独身", 'log': [], 'waiting_choice': False})

# --- ヘルパー関数 ---
def add_log(msg):
    st.session_state.log.append(msg)

# --- メインUI ---
st.title("🎲 Life Quest 2026")

# ステータス表示
with st.container():
    st.markdown(f"""
    <div class="status-card">
        <h3>現在のステータス</h3>
        <b>職業:</b> {st.session_state.job} | <b>状況:</b> {st.session_state.partner}<br>
        <b>所持金:</b> {st.session_state.money}万円
    </div>
    """, unsafe_allow_html=True)

# 現在のイベント画像
current_cell = BOARD_DATA.get(st.session_state.pos, BOARD_DATA[0])
st.image(current_cell["img"], width=200)
st.subheader(current_cell["text"])

# --- ゲームロジック ---
if st.session_state.waiting_choice:
    # 選択イベント発生中
    if st.session_state.pos == 5:
        st.write("どの職業を目指しますか？")
        col1, col2 = st.columns(2)
        if col1.button("サラリーマン"):
            st.session_state.job = "サラリーマン"
            st.session_state.waiting_choice = False
            st.rerun()
        if col2.button("起業家"):
            st.session_state.job = "起業家"
            st.session_state.money -= 50
            st.session_state.waiting_choice = False
            st.rerun()
    elif st.session_state.pos == 12:
        st.write("人生のパートナーを選びますか？")
        col1, col2 = st.columns(2)
        if col1.button("結婚する"):
            st.session_state.partner = "既婚"
            st.session_state.money -= 30
            st.session_state.waiting_choice = False
            st.rerun()
        if col2.button("自由な独身"):
            st.session_state.waiting_choice = False
            st.rerun()

else:
    # 通常のサイコロ振り
    if st.button("サイコロを振る！"):
        roll = random.randint(1, 6)
        next_pos = st.session_state.pos + roll
        
        # チェックポイントを跨ぐ場合の処理
        for cp in CHECKPOINTS:
            if st.session_state.pos < cp <= next_pos:
                next_pos = cp
                st.session_state.waiting_choice = True
                break
        
        st.session_state.pos = min(next_pos, 20)
        
        # 資金の更新
        cell = BOARD_DATA.get(st.session_state.pos, {})
        st.session_state.money += cell.get("money", 0)
        add_log(f"🎲 {roll}が出て、{st.session_state.pos}マス目へ：{cell.get('text')}")
        
        if st.session_state.pos >= 20:
            st.balloons()
            st.success("🎉 ゴール！")
        st.rerun()

# 履歴表示
st.write("---")
for m in reversed(st.session_state.log[-5:]):
    st.caption(m)
