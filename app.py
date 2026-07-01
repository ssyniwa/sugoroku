import streamlit as st
import random

# ページ設定
st.set_page_config(page_title="シンプルすごろく", page_icon="🎲")

# イベントリスト（ランダムに選ばれる内容）
events = [
    "宝くじが当たった！資金＋100万！",
    "道で100円を拾った。ちょっと嬉しい。",
    "急な雨に降られた。洗濯物がびしょ濡れ...",
    "新しい趣味を見つけた！人生が豊かになった。",
    "お腹が空いたので寄り道。少し進みが遅れた。",
    "素晴らしい出会いがあった！運気アップ！"
]

# 初期化（セッション状態の管理）
if 'position' not in st.session_state:
    st.session_state.position = 0
if 'log' not in st.session_state:
    st.session_state.log = ["ゲームスタート！サイコロを振ってね"]

# タイトル
st.title("🎲 ミニすごろく")

# 現在地表示
st.subheader(f"現在のマス: {st.session_state.position}")

# サイコロを振るボタン
if st.button("サイコロを振る！", use_container_width=True):
    move = random.randint(1, 6)
    st.session_state.position += move
    
    # イベント発生
    event = random.choice(events)
    log_text = f"🎲 {move} 進んだ！: {event}"
    st.session_state.log.append(log_text)
    
    # ゴール判定
    if st.session_state.position >= 20:
        st.success("🎉 ゴール！おめでとう！")
        if st.button("リセット"):
            st.session_state.position = 0
            st.session_state.log = ["スタート！"]
            st.rerun()

# ログ表示（新しい順に表示）
st.markdown("---")
st.write("**ログ:**")
for msg in reversed(st.session_state.log):
    st.text(msg)
