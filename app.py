import streamlit as st
import random

# ページ設定
st.set_page_config(page_title="人生すごろく改", page_icon="🚗")

# イベント画像の設定（イベントタイプ: 画像URL）
EVENT_IMAGES = {
    "start": "https://cdn-icons-png.flaticon.com/512/3062/3062634.png",
    "lose": "https://cdn-icons-png.flaticon.com/512/2919/2919736.png",  # 困り顔
    "gain": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",  # 笑顔
    "warp": "https://cdn-icons-png.flaticon.com/512/3757/3757962.png",  # ロケット
    "normal": "https://cdn-icons-png.flaticon.com/512/3062/3062678.png"  # 通常
}

# マスの定義
board_map = {
    5: ("lose", "贅沢しすぎた！資金-50万", 50),
    10: ("warp", "近道発見！15マス目にジャンプ！", 15),
    12: ("gain", "臨時ボーナス！資金+100万", 100),
    18: ("lose", "トラブル発生！資金-80万", 80),
}

# 初期化
if 'position' not in st.session_state:
    st.session_state.position = 0
    st.session_state.money = 100
    st.session_state.log = ["スタート！人生の旅へ出発！"]
    st.session_state.current_image = EVENT_IMAGES["start"]

# タイトルとステータス
st.title("🚗 人生すごろく 2026")
col1, col2 = st.columns(2)
col1.metric("現在地", f"{st.session_state.position}")
col2.metric("所持金", f"{st.session_state.money}万円")

# ★画像表示エリア
st.image(st.session_state.current_image, width=150)

# ゲームロジック
if st.button("サイコロを振る！", use_container_width=True):
    move = random.randint(1, 6)
    st.session_state.position += move
    
    # イベント判定と画像切り替え
    if st.session_state.position in board_map:
        m_type, msg, val = board_map[st.session_state.position]
        st.session_state.current_image = EVENT_IMAGES[m_type]
        st.session_state.log.append(f"📍 マス{st.session_state.position}: {msg}")
        
        if m_type == "lose": st.session_state.money -= val
        elif m_type == "gain": st.session_state.money += val
        elif m_type == "warp": 
            st.session_state.position = val
            st.warning("ワープ発動！")
    else:
        st.session_state.current_image = EVENT_IMAGES["normal"]
        st.session_state.log.append(f"🎲 {move}進んだ。平和な日常。")

    # ゴール判定
    if st.session_state.position >= 20:
        st.balloons()
        st.success(f"🎉 ゴール！最終資産: {st.session_state.money}万円")
        if st.button("もう一度遊ぶ"):
            st.session_state.position = 0
            st.session_state.money = 100
            st.session_state.current_image = EVENT_IMAGES["start"]
            st.session_state.log = ["リスタート！"]
            st.rerun()

# ログ表示
st.write("---")
for msg in reversed(st.session_state.log[-5:]):
    st.caption(msg)
