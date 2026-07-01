import streamlit as st
import random

# ページ設定
st.set_page_config(page_title="人生すごろく改", page_icon="🚗")

# ゲーム設定
TOTAL_CELLS = 20
# 特殊マスの定義 {マス番号: (タイプ, 内容, 数値)}
board_map = {
    5: ("lose", "贅沢しすぎた！資金-50万", 50),
    10: ("warp", "近道発見！15マス目にジャンプ！", 15),
    12: ("gain", "臨時ボーナス！資金+100万", 100),
    18: ("lose", "トラブル発生！資金-80万", 80),
}

# 初期化
if 'position' not in st.session_state:
    st.session_state.position = 0
    st.session_state.money = 100 # 初期資金
    st.session_state.log = ["スタート！人生の旅へ出発！"]

# UI表示
st.title("🚗 人生すごろく 2026")
col1, col2 = st.columns(2)
col1.metric("現在地", f"{st.session_state.position} / {TOTAL_CELLS}")
col2.metric("所持金", f"{st.session_state.money}万円")

# 状況に応じたアイコン表示
if st.session_state.position < 10:
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062634.png", width=100) # 若い頃のイメージ
else:
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062678.png", width=100) # 熟成のイメージ

# ゲームロジック
if st.button("サイコロを振る！", use_container_width=True):
    move = random.randint(1, 6)
    st.session_state.position += move
    
    # 特殊マス判定
    if st.session_state.position in board_map:
        m_type, msg, val = board_map[st.session_state.position]
        st.session_state.log.append(f"📍 マス{st.session_state.position}: {msg}")
        if m_type == "lose": st.session_state.money -= val
        elif m_type == "gain": st.session_state.money += val
        elif m_type == "warp": st.session_state.position = val
    else:
        st.session_state.log.append(f"🎲 {move}進んだ。何事もない平和な日。")

    # ゴール判定
    if st.session_state.position >= TOTAL_CELLS:
        st.balloons()
        st.success(f"🎉 ゴール！最終資産: {st.session_state.money}万円")
        if st.button("もう一度遊ぶ"):
            st.session_state.position = 0
            st.session_state.money = 100
            st.session_state.log = ["リスタート！"]
            st.rerun()

# ログ表示
st.write("---")
st.write("**これまでの人生:**")
for msg in reversed(st.session_state.log[-5:]): # 最新5件を表示
    st.caption(msg)
