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

CHECKPOINTS = [20, 60,100]
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
    {"text": "図書カードをもらった", "img": "images/book.png", "money": 5},
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
    {"text": "チーム目標達成で報奨金", "img": "images/job118.png", "money": 20},
    {"text": "慣れない事務処理でミス連発", "img": "images/job119.png", "money": -10},
]
ENTREPRENEUR_EVENTS = [
    {"text": "投資家から出資獲得！", "img": "images/job21.png", "money": 100},
    {"text": "自社サービスがSNSでバズる", "img": "images/job22.png", "money": 80},
    {"text": "特許取得でライセンス料収入", "img": "images/job23.png", "money": 50},
    {"text": "大手企業との提携が決定", "img": "images/job24.png", "money": 60},
    {"text": "新規事業が異例のヒット", "img": "images/job25.png", "money": 70},
    {"text": "補助金審査に見事通過", "img": "images/job26.png", "money": 40},
    {"text": "クラウドファンディング大成功", "img": "images/job27.png", "money": 50},
    {"text": "取引先が突然の倒産…売掛金回収不能", "img": "images/job28.png", "money": -80},
    {"text": "サーバーがダウンし補償問題に", "img": "images/job29.png", "money": -50},
    {"text": "競合他社に顧客をごっそり奪われる", "img": "images/job210.png", "money": -40},
    {"text": "法改正により事業モデルの変更を余儀なくされる", "img": "images/job211.png", "money": -30},
    {"text": "優秀なエンジニアが引き抜きで退職", "img": "images/job212.png", "money": -30},
    {"text": "オフィス賃料の値上げに直面", "img": "images/job213.png", "money": -20},
    {"text": "宣伝費を使いすぎた…", "img": "images/job214.png", "money": -25},
    {"text": "メンターに出会い経営のアドバイスを受ける", "img": "images/job215.png", "money": 20},
    {"text": "海外展開で市場を拡大", "img": "images/job216.png", "money": 60},
    {"text": "訴訟リスク発生、弁護士費用で痛い出費", "img": "images/job217.png", "money": -40},
    {"text": "徹夜の連続でついにダウン（治療費）", "img": "images/job218.png", "money": -30},
    {"text": "運命のビジネスパートナーとの出会い", "img": "images/job219.png", "money": 30},
    {"text": "自分の会社を売却（M&A）！", "img": "images/job220.png", "money": 200},
]
DOCTOR_EVENTS = [
    {"text": "緊急手術成功！謝礼金と評価を得る", "img": "images/job41.png", "money": 60},
    {"text": "学会で論文が優秀賞を受賞", "img": "images/job42.png", "money": 40},
     {"text": "難易度の高い症例を完治させる", "img": "images/job43.png", "money": 50},
    {"text": "後輩の指導が実を結ぶ", "img": "images/job44.png", "money": 20},
    {"text": "高額な医療機器の導入が決定", "img": "images/job45.png", "money": -40},
    {"text": "医療ミスを回避するための最新研修受講", "img": "images/job46.png", "money": -20},
    {"text": "激務の末、仮眠室で束の間の休息", "img": "images/job47.png", "money": 5},
    {"text": "訴訟リスクに備える保険料の支払い", "img": "images/job48.png", "money": -30},
    {"text": "専門医資格を取得して給与ランクアップ", "img": "images/job49.png", "money": 50},
    {"text": "病院の経営難による一時的な減給", "img": "images/job410.png", "money": -30},
    {"text": "難病治療のプロジェクトリーダーに就任", "img": "images/job411.png", "money": 40},
    {"text": "海外の最新医療視察へ出発", "img": "images/job412.png", "money": -20},
    {"text": "患者さんから温かい手紙を貰う", "img": "images/job413.png", "money": 10},
    {"text": "オンコール待機中に呼び出される", "img": "images/job414.jpg", "money": -10},
    {"text": "医局の飲み会でネットワークを拡大", "img": "images/job415.png", "money": -10},
    {"text": "研究費の獲得競争に勝利", "img": "images/job416.png", "money": 30},
    {"text": "診断に迷い、専門書を大量購入", "img": "images/job417.png", "money": -15},
    {"text": "激務による慢性疲労で精密検査を受ける", "img": "images/job418.png", "money": -20},
    {"text": "講演の依頼を受けて謝礼を受け取る", "img": "images/job419.png", "money": 20},
    {"text": "病院長から次期候補として指名される", "img": "images/job420.png", "money": 50},
]
CIVIL_SERVANT_EVENTS = [
    {"text": "地域住民から感謝の言葉を頂く", "img": "images/job31.png", "money": 10},
    {"text": "長期勤続による表彰金", "img": "images/job32.png", "money": 30},
    {"text": "予算策定業務が完璧に完了", "img": "images/job33.png", "money": 20},
    {"text": "福利厚生で格安温泉旅行へ", "img": "images/job34.png", "money": 5},
    {"text": "定期昇給で少しだけ手取りUP", "img": "images/job35.png", "money": 15},
    {"text": "災害対策本部の設置で特別手当", "img": "images/job36.png", "money": 25},
    {"text": "公共施設のリニューアル計画に貢献", "img": "images/job37.png", "money": 20},
    {"text": "住民説明会で予期せぬ厳しい意見", "img": "images/job38.png", "money": -10},
    {"text": "システム入替に伴う休日出勤", "img": "images/job39.png", "money": -5},
    {"text": "部署異動で慣れない業務に四苦八苦", "img": "images/job310.png", "money": -15},
    {"text": "経費削減のあおりで備品購入制限", "img": "images/job311.png", "money": -5},
    {"text": "住民からの理不尽な苦情対応で疲弊", "img": "images/job312.png", "money": -10},
    {"text": "忘年会で公務員仲間との絆が深まる", "img": "images/job313.png", "money": 5},
    {"text": "資格取得支援制度を活用してスキルアップ", "img": "images/job314.png", "money": 10},
    {"text": "庁内のスポーツ大会で景品をゲット", "img": "images/job315.png", "money": 5},
    {"text": "激務による体調不良で休暇を取る", "img": "images/job316.png", "money": -10},
    {"text": "新庁舎の建設で心機一転", "img": "images/job317.png", "money": 5},
    {"text": "議会対応の資料作成で深夜作業", "img": "images/job318.png", "money": -5},
    {"text": "地域イベントの運営サポートで出費", "img": "images/job319.png", "money": -10},
    {"text": "早期退職優遇制度の案内が届く…", "img": "images/job320.png", "money": 30},
]
ARTIST_EVENTS = [
    {"text": "個展が大盛況！作品が完売", "img": "images/job51.png", "money": 100},
    {"text": "海外のコンクールで入賞", "img": "images/job52.png", "money": 80},
    {"text": "大企業とのコラボデザインが採用", "img": "images/job53.png", "money": 60},
    {"text": "SNSで作品が拡散、フォロワー激増", "img": "images/job54.png", "money": 40},
    {"text": "公募展でグランプリ受賞", "img": "images/job55.png", "money": 70},
    {"text": "自分の作品が映画の劇中に登場", "img": "images/job56.png", "money": 50},
    {"text": "インスピレーションを求めて極貧旅行", "img": "images/job57.png", "money": -30},
    {"text": "高価な画材・機材の衝動買い", "img": "images/job58.png", "money": -40},
    {"text": "依頼主の無茶ぶりに対応して消耗", "img": "images/job59.png", "money": -10},
    {"text": "制作に行き詰まり、気分転換に散財", "img": "images/job510.png", "money": -20},
    {"text": "自分の作風が時代を先取りしすぎて理解されない", "img": "images/job511.png", "money": -30},
    {"text": "ギャラリーの利用料が高騰", "img": "images/job512.png", "money": -20},
    {"text": "尊敬する師匠からのアドバイスで開眼", "img": "images/job513.png", "money": 20},
    {"text": "地方自治体の壁画制作を受託", "img": "images/job514.png", "money": 30},
    {"text": "作品保管場所の確保でスタジオ借り入れ", "img": "images/job515.png", "money": -20},
    {"text": "表現の幅を広げるためのワークショップ受講", "img": "images/job516.png", "money": -15},
    {"text": "著作権侵害のトラブル対応で弁護士へ相談", "img": "images/job517.png", "money": -40},
    {"text": "徹夜で制作し、体調を崩す（医療費）", "img": "images/job518.png", "money": -20},
    {"text": "偶然の出会いから表現の幅が広がる", "img": "images/job519.png", "money": 10},
    {"text": "美術館に作品が永久収蔵される！", "img": "images/job520.png", "money": 150},
]
ATHLETE_EVENTS = [
    {"text": "全国大会で優勝、スポンサー獲得！", "img": "images/job61.png", "money": 100},
    {"text": "リーグ戦でMVP受賞", "img": "images/job62.png", "money": 70},
    {"text": "海外トップチームからのオファー", "img": "images/job63.png", "money": 90},
    {"text": "メディアの注目を集めCM出演料獲得", "img": "images/job64.png", "money": 60},
    {"text": "シーズン自己ベスト更新で報奨金", "img": "images/job65.png", "money": 40},
    {"text": "若手の台頭でレギュラー争いが激化", "img": "images/job66.png", "money": -10},
    {"text": "練習中の怪我で一時戦線離脱", "img": "images/job67.png", "money": -40},
    {"text": "高額なパーソナルトレーナーを雇う", "img": "images/job68.png", "money": -30},
    {"text": "競技用具の最新モデルへの買い替え", "img": "images/job69.png", "money": -20},
    {"text": "栄養管理のための専属シェフ契約", "img": "images/job610.png", "money": -25},
    {"text": "大会直前の極度の緊張で調子を崩す", "img": "images/job611.png", "money": -10},
    {"text": "ファンクラブ設立で安定収入増", "img": "images/job612.png", "money": 30},
    {"text": "自身の名前を冠したグッズがヒット", "img": "images/job613.png", "money": 40},
    {"text": "地方のスポーツ教室で講師を務める", "img": "images/job614.png", "money": 15},
    {"text": "遠征先での移動費・宿泊費が嵩む", "img": "images/job615.png", "money": -15},
    {"text": "ドーピング検査の準備と対応で疲弊", "img": "images/job616.png", "money": -5},
    {"text": "チームメイトとの遠征での食事会", "img": "images/job617.png", "money": -10},
    {"text": "激しい練習で疲労骨折（治療と休養）", "img": "images/job618.png", "money": -50},
    {"text": "競技団体からの強化指定選手に選出", "img": "images/job619.png", "money": 20},
    {"text": "突然の引退表明！", "img": "images/job620.png", "money": 50},
]
INFLUENCER_EVENTS = [
    {"text": "動画が世界中で大バズり！", "img": "images/job71.png", "money": 150},
    {"text": "大手企業から専属アンバサダー依頼", "img": "images/job72.png", "money": 80},
    {"text": "ライブ配信で投げ銭が止まらない", "img": "images/job73.png", "money": 60},
    {"text": "ファン感謝イベントでグッズが即完売", "img": "images/job74.png", "money": 50},
    {"text": "アフィリエイト広告が爆発的に売れる", "img": "images/job75.png", "money": 40},
    {"text": "ネット記事で特集され認知度UP", "img": "images/job76.png", "money": 30},
    {"text": "過去の失言が掘り返されて炎上…", "img": "images/job77.png", "money": -100},
    {"text": "誤情報の拡散により謝罪動画の投稿", "img": "images/job78.png", "money": -40},
    {"text": "悪質なアンチコメント対応で精神疲弊", "img": "images/job79.png", "money": -20},
    {"text": "撮影機材を最新の高級品に一新", "img": "images/job710.png", "money": -40},
    {"text": "動画編集を外注して効率化", "img": "images/job711.png", "money": -30},
    {"text": "流行りの撮影スポットへ弾丸海外遠征", "img": "images/job712.png", "money": -50},
    {"text": "著作権違反の指摘で動画削除・収益没収", "img": "images/job713.png", "money": -60},
    {"text": "映えスポットでの撮影中に私物を破損", "img": "images/job714.png", "money": -15},
    {"text": "フォロワーとの交流で新たな企画のヒントを得る", "img": "images/job715.png", "money": 20},
    {"text": "ネットミーム化して知名度が急上昇", "img": "images/job716.png", "money": 50},
    {"text": "プライベート流出！住所変更で引っ越し", "img": "images/job717.png", "money": -40},
    {"text": "企画倒れで動画の再生数が伸び悩み", "img": "images/job718.png", "money": -10},
    {"text": "コラボ企画で人気配信者と共演", "img": "images/job719.png", "money": 40},
    {"text": "アカウントが突如凍結…再起への道", "img": "images/job720.png", "money": -80},
]
INVEST_EVENTS = [
    {"text": "急成長株を発掘！配当金が跳ね上がる", "img": "images/job81.png", "money": 150},
    {"text": "市場トレンドを完璧に読み切り大勝ち", "img": "images/job82.png", "money": 120},
    {"text": "不動産投資物件の値上がり益確定", "img": "images/job83.png", "money": 100},
    {"text": "仮想通貨の爆上げに乗り遅れず利確", "img": "images/job84.png", "money": 90},
    {"text": "インサイダー情報を疑われ調査が入るが潔白証明", "img": "images/job85.png", "money": 50},
    {"text": "投資家コミュニティで有力な未公開株情報を入手", "img": "images/job86.png", "money": 40},
    {"text": "市場暴落に直撃", "img": "images/job87.png", "money": -150},
    {"text": "信用取引の追証が発生、現金をかき集める", "img": "images/job88.png", "money": -120},
    {"text": "投資詐欺に巻き込まれそうになるが回避", "img": "images/job89.png", "money": -20},
    {"text": "損切りが遅れ、資産価値が半減", "img": "images/job810.png", "money": -80},
    {"text": "高額な有料投資セミナーで情報商材を買わされる", "img": "images/job811.png", "money": -30},
    {"text": "経済ニュースの読み間違えで誤った注文を出す", "img": "images/job812.png", "money": -40},
    {"text": "運用するファンドの管理手数料支払い", "img": "images/job813.png", "money": -20},
    {"text": "経済情勢調査のために世界を飛び回る旅費", "img": "images/job814.png", "money": -30},
    {"text": "投資の神様と呼ばれる人物と奇跡の対面", "img": "images/job815.png", "money": 30},
    {"text": "分散投資が功を奏し、リスクを最小限に抑える", "img": "images/job816.png", "money": 20},
    {"text": "新しい投資手法を学ぶためのシステム構築費用", "img": "images/job817.png", "money": -40},
    {"text": "政治的な不透明感から株価が乱高下", "img": "images/job818.png", "money": -50},
    {"text": "運良くIPO銘柄の抽選に当選", "img": "images/job819.png", "money": 70},
    {"text": "自分の資産が10倍に！ファンドを設立", "img": "images/job820.png", "money": 200},
] # 10種
ADVENTURE_EVENTS = [
    {"text": "未知の古代遺跡を発見！世界中で話題に", "img": "images/job91.png", "money": 150},
    {"text": "新種の生物を発見し、学術界から報奨金", "img": "images/job92.png", "money": 80},
    {"text": "秘境の絶景を撮影し、大手メディアに売却", "img": "images/job93.png", "money": 60},
    {"text": "伝説の財宝の片鱗を見つける", "img": "images/job94.png", "money": 50},
    {"text": "地元のガイドと信頼を築き、穴場へ案内される", "img": "images/job95.png", "money": 40},
    {"text": "冒険譚を執筆し、ベストセラーになる", "img": "images/job96.png", "money": 30},
    {"text": "過酷な自然の中で遭難し、救助費用が発生", "img": "images/job97.png", "money": -100},
    {"text": "探検用機材が崖から落下し全損", "img": "images/job98.png", "money": -40},
    {"text": "現地で食中毒にかかり療養", "img": "images/job99.png", "money": -20},
    {"text": "許可証の取得不備で入域を拒否され、手配し直し", "img": "images/job910.png", "money": -40},
    {"text": "猛獣に追いかけられ、持ち物を捨てて逃走", "img": "images/job911.png", "money": -30},
    {"text": "異常気象により遠征が長期化", "img": "images/job912.png", "money": -50},
    {"text": "冒険中の怪我で現地病院に緊急入院", "img": "images/job913.png", "money": -60},
    {"text": "盗賊に装備の一部を奪われる", "img": "images/job914.png", "money": -15},
    {"text": "運よく現地のお祭りに招待され、歓迎を受ける", "img": "images/job915.png", "money": 20},
    {"text": "薬草を発見し、製薬会社へ提供", "img": "images/job916.png", "money": 50},
    {"text": "装備のメンテナンス不足で登山中にピンチ", "img": "images/job917.png", "money": -40},
    {"text": "新たなルートを開拓し、後世の冒険家の指標に", "img": "images/job918.png", "money": -10},
    {"text": "悪天候でヘリコプターのチャーターが必要に", "img": "images/job919.png", "money": 40},
    {"text": "世界最高峰の登頂に成功！記念すべき旅の終わり", "img": "images/job920.png", "money": -80},
]
LIFE_STAGES = [
    {"text": "家族との団らん", "img": "images/work_hard.png", "money": -10},
    {"text": "一人旅を満喫", "img": "images/raise.png", "money": 30},
    {"text": "趣味の時間", "img": "images/success.png", "money": 20},
] # 10種
ELDER_EVENTS = [
    {"text": "健康診断で異常なし", "img": "images/work_hard.png", "money": -10},
    {"text": "昔の友人と再会", "img": "images/raise.png", "money": 30},
    {"text": "のんびりした休日", "img": "images/success.png", "money": 20},
]

# マスごとの生成関数（100マスを網羅する）
def get_cell_data(pos):
    if pos == 0: return {"text": "スタート！", "img": "images/akari1.png"}
    elif pos == 20: return {"text": "職業選択マス",  "img": "images/akari2.png","type": "checkpoint"}
    elif pos == 60: return {"text": "結婚選択マス", "img": "images/akari3.png", "type": "checkpoint"}
    elif pos == 100: return {"text": "ゴール！", "img": "images/akari4.png"}
    
    # 範囲指定でイベントを割り当て
    elif 1 <= pos <= 19:
        return random.choice(STUDENT_EVENTS)
    elif 21 <= pos <= 59:
        if st.session_state.job == "サラリーマン":
            return random.choice(SALARYMAN_EVENTS)
        elif st.session_state.job == "起業家":
            return random.choice(ENTREPRENEUR_EVENTS)
        elif st.session_state.job == "公務員":
            return random.choice(CIVIL_SERVANT_EVENTS)
        elif st.session_state.job == "医者":
            return random.choice(DOCTOR_EVENTS)
        elif st.session_state.job == "芸術家":
            return random.choice(ARTIST_EVENTS)
        elif st.session_state.job == "スポーツ選手":
            return random.choice(ATHLETE_EVENTS)
        elif st.session_state.job == "インフルエンサー":
            return random.choice(INFLUENCER_EVENTS)
        elif st.session_state.job == "投資家":
            return random.choice(INVEST_EVENTS)
        elif st.session_state.job == "冒険家":
            return random.choice(ADVENTURE_EVENTS)
    elif 61 <= pos <= 79:
        if st.session_state.partner == "既婚":
            return random.choice(LIFE_STAGES)
        elif st.session_state.job == "サラリーマン":
            return random.choice(SALARYMAN_EVENTS)
        elif st.session_state.job == "起業家":
            return random.choice(ENTREPRENEUR_EVENTS)
        elif st.session_state.job == "公務員":
            return random.choice(CIVIL_SERVANT_EVENTS)
        elif st.session_state.job == "医者":
            return random.choice(DOCTOR_EVENTS)
        elif st.session_state.job == "芸術家":
            return random.choice(ARTIST_EVENTS)
        elif st.session_state.job == "スポーツ選手":
            return random.choice(ATHLETE_EVENTS)
        elif st.session_state.job == "インフルエンサー":
            return random.choice(INFLUENCER_EVENTS)
        elif st.session_state.job == "投資家":
            return random.choice(INVEST_EVENTS)
        elif st.session_state.job == "冒険家":
            return random.choice(ADVENTURE_EVENTS)
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
st.session_state.money += current_cell.get("money", 0)
if current_cell.get("money", 0) != 0:
    st.session_state.log.append(f"資金(+{current_cell.get("money", 0)}万円)")
# 職業補正の適用（収入イベント）
    stats = JOB_STATS[st.session_state.job]
    if -5 < stats["luck_bonus"]:
        salary = stats["salary"] + random.randint(-5, stats["luck_bonus"])
    else :
        salary = stats["salary"] + random.randint(stats["luck_bonus"],-5)
    st.session_state.money += salary
    st.session_state.log.append(f"進んだ！(+{salary}万円)")
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
    elif st.session_state.pos == 60:
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
        next_pos = min(st.session_state.pos + roll, 100)
        
        
        
        
        # チェックポイント判定
        for cp in CHECKPOINTS:
            if st.session_state.pos < cp <= next_pos:
                next_pos = cp
                st.session_state.waiting_choice = True
                break
        
        st.session_state.pos = next_pos
        
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
