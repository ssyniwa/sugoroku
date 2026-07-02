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

CHECKPOINTS = [5, 12]
# --- 職業別・ライフステージ別イベントデータ ---
# マス範囲ごとのイベントをリスト化（簡易実装例）
# イベントリストを辞書型に拡張
STUDENT_EVENTS = [
    {"text": "部活で優勝！", "img": "images/win.png", "money": 10},
    {"text": "テストで100点！", "img": "images/test_win.png", "money": 10},
    {"text": "アルバイトで初給料", "img": "images/part_time.png", "money": 20},
    {"text": "落とし物を届けて謝礼金", "img": "images/reward.png", "money": 5},
    {"text": "不用品を売って小遣い稼ぎ", "img": "images/sell.png", "money": 10},
    {"text": "部活の遠征で出費", "img": "images/trip.png", "money": -10},
    {"text": "スマホを壊して修理代", "img": "images/broken.png", "money": -15},
    {"text": "テストで赤点、補習費", "img": "images/fail.png", "money": -5},
    {"text": "友達と食べ歩きしすぎた", "img": "images/eat.png", "money": -5},
    {"text": "図書カードをもらった", "img": "images/book.png", "money": 5}
]
SALARYMAN_EVENTS = [
    {"text": "プロジェクトリーダーに抜擢！", "img": "images/job11.png", "money": 30},
    {"text": "夏のボーナス支給！", "img": "images/job12.png", "money": 50},
    {"text": "クライアントから感謝のメール", "img": "images/job13.png", "money": 10},
    {"text": "効率化を提案し、部署表彰される", "img": "images/job14.png", "money": 20},
    {"text": "定時退社！自分へのご褒美", "img": "images/job15.png", "money": -5},
    {"text": "資格取得手当で収入アップ", "img": "images/job16.png", "money": 15},
    {"text": "会社からの独立を夢見て自己啓発本購入", "img": "images/job120.png", "money": -5},
    {"text": "同僚の結婚式でご祝儀", "img": "images/job17.png", "money": -30},
    {"text": "飲み会で羽目を外してタクシー帰宅", "img": "images/job18.png", "money": -10},
    {"text": "突然のPC故障で買い替え", "img": "images/job19.png", "money": -20},
    {"text": "重要な会議で大成功！", "img": "images/job110.png", "money": 25},
    {"text": "社員旅行でリフレッシュ", "img": "images/job111.png", "money": -5},
    {"text": "納期に追われて深夜残業（振替休日あり）", "img": "images/job112.png", "money": -5},
    {"text": "昇進して基本給アップ", "img": "images/job113.png", "money": 40},
    {"text": "誤送信メールのフォローで冷や汗", "img": "images/job114.png", "money": -10},
    {"text": "営業先で美味しいランチをご馳走になる", "img": "images/job115.png", "money": 5},
    {"text": "健康診断で再検査の診断", "img": "images/job116.png", "money": -15},
    {"text": "新しいスーツを新調", "img": "images/job117.png", "money": -20},
    {"text": "プチーム目標達成で報奨金", "img": "images/job118.png", "money": 20},
    {"text": "慣れない事務処理でミス連発", "img": "images/job119.png", "money": -10} ... 他の18種をここに追加
]
JOB_EVENTS = [
    {"text": "残業続きで疲弊", "img": "images/work_hard.png", "money": -10},
    {"text": "昇給のチャンス！", "img": "images/raise.png", "money": 30},
    {"text": "プロジェクト成功", "img": "images/success.png", "money": 20}
]
LIFE_STAGES = [
    {"text": "家族との団らん", "img": "images/work_hard.png", "money": -10},
    {"text": "一人旅を満喫", "img": "images/raise.png", "money": 30},
    {"text": "趣味の時間", "img": "images/success.png", "money": 20}
] # 10種
ELDER_EVENTS = [
    {"text": "健康診断で異常なし", "img": "images/work_hard.png", "money": -10},
    {"text": "昔の友人と再会", "img": "images/raise.png", "money": 30},
    {"text": "のんびりした休日", "img": "images/success.png", "money": 20}
]

# マスごとの生成関数（100マスを網羅する）
def get_cell_data(pos):
    if pos == 0: return {"text": "スタート！", "img": "images/akari1.png"}
    elif pos == 20: return {"text": "職業選択マス",  "img": "images/akari2.png","type": "checkpoint"}
    elif pos == 50: return {"text": "結婚選択マス", "img": "images/akari3.png", "type": "checkpoint"}
    elif pos == 100: return {"text": "ゴール！", "img": "images/akari4.png"}
    
    # 範囲指定でイベントを割り当て
    elif 1 <= pos <= 19:
        return random.choice(STUDENT_EVENTS)
    elif 21 <= pos <= 49:
        if st.session_state.job == "サラリーマン":
            return random.choice(SALARYMAN_EVENTS)
        return random.choice(JOB_EVENTS)
    elif 51 <= pos <= 79:
        if st.session_state.partner == "既婚":
            return random.choice(LIFE_STAGES)
        else:
            return random.choice(JOB_EVENTS)# これも辞書型にしておくこと
    elif 80 <= pos <= 99:
        return random.choice(ELDER_EVENTS)
    return {"text": "平凡な日常",  "img": "images/akari5.png","money": 0}
# --- 初期化 ---
if 'pos' not in st.session_state:
    st.session_state.update({'pos': 0, 'money': 100, 'job': "学生", 'partner': "独身", 'log': [], 'waiting_choice': False})

# --- メインUI ---
st.title("🎲 Life Quest 2026")

# 現在のイベント情報を取得
current_cell = get_cell_data(st.session_state.pos)

# 画像とステータスを一つのまとまりとして表示
with st.container():
    col1, col2 = st.columns([1, 1])  # 画面を半分ずつに分ける
    
    with col1:
        st.image(current_cell["img"], use_container_width=True)
    
    with col2:
        # カードのスタイルを調整して中央に配置
        st.markdown(f"""
        <div style="padding: 20px; border-radius: 15px; background-color: #262730; border: 1px solid #4F46E5; height: 100%;">
            <b style="color:white;">職業:</b> <span style="color:#A5B4FC;">{st.session_state.job}</span><br>
            <b style="color:white;">状況:</b> <span style="color:#A5B4FC;">{st.session_state.partner}</span><br>
            <b style="color:white;">資産:</b> <span style="color:#34D399;">{st.session_state.money}万円</span>
        </div>
        """, unsafe_allow_html=True)

# テキストとボタン
st.subheader(current_cell["text"])

# --- ロジック ---
if st.session_state.waiting_choice:
    if st.session_state.pos == 20:
        st.write("職業を選択してください")
        # 3列にボタンを配置してスマホでも選びやすく
        cols = st.columns(3)
        jobs = list(JOB_STATS.keys())[1:] # 学生以外を表示
        for i, job in enumerate(jobs):
            if cols[i % 3].button(job):
                st.session_state.job = job
                st.session_state.waiting_choice = False
                st.rerun()
    elif st.session_state.pos == 50:
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
        st.session_state.money += current_cell["money"]
        # チェックポイント判定
        for cp in CHECKPOINTS:
            if st.session_state.pos < cp <= next_pos:
                next_pos = cp
                st.session_state.waiting_choice = True
                break
        
        st.session_state.pos = next_pos
        st.session_state.log.append(f"進んだ！(+{salary}万円)")
        # ゴール判定（ロジック内の既存のゴール判定をこれに置き換えてください）
        if st.session_state.pos >= 100:
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
