import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="Woman's Health Care AI",
    page_icon="🧘‍♀️",
    layout="wide"
)

# 2. 스타일링 (여성 타겟에 맞춰 조금 더 부드러운 톤으로 변경 가능하나, 가독성을 위해 기존 유지)
st.markdown("""
    <style>
    .card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        background-color: white;
    }
    .workout-card { border-top: 5px solid #FF6B6B; } /* 조금 더 부드러운 레드 */
    .food-card { border-top: 5px solid #51CF66; }   /* 조금 더 부드러운 그린 */
    
    .card-title {
        font-size: 1.1em;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    .kcal-tag {
        font-size: 0.85em;
        font-weight: bold;
        color: #555;
        background-color: #f8f9fa;
        padding: 4px 8px;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터베이스 정의 (성인 여성 60kg 기준 수정)

# [운동 DB] 체중 감소에 따라 소모 칼로리 약 20% 하향 조정
workout_db = {
    "상체 (라인/탄력)": {
        "exercises": [
            {"name": "니 푸시업 (무릎대고)", "set": "3세트 x 12회", "kcal": 45},
            {"name": "덤벨 킥백 (팔뚝)", "set": "3세트 x 15회", "kcal": 35},
            {"name": "랫 풀 다운", "set": "4세트 x 12회", "kcal": 60}
        ],
        "cardio": {"name": "가벼운 조깅 20분", "kcal": 160},
        "total_burn": 300
    },
    "하체 (힙업/슬림)": {
        "exercises": [
            {"name": "와이드 스쿼트", "set": "4세트 x 15회", "kcal": 90},
            {"name": "덩키 킥 (힙업)", "set": "3세트 x 20회", "kcal": 50},
            {"name": "런지", "set": "3세트 x 15회", "kcal": 70}
        ],
        "cardio": {"name": "실내 자전거 20분", "kcal": 180},
        "total_burn": 390
    },
    "전신 (지방 연소)": {
        "exercises": [
            {"name": "슬로우 버피", "set": "3세트 x 10회", "kcal": 100},
            {"name": "마운틴 클라이머", "set": "3세트 x 30초", "kcal": 80},
            {"name": "점핑잭 (팔벌려뛰기)", "set": "3세트 x 30회", "kcal": 60}
        ],
        "cardio": {"name": "인터벌 러닝 20분", "kcal": 210},
        "total_burn": 450
    }
}

# [식단 DB] 기초대사량 고려하여 섭취 칼로리 재조정
# 다이어트: ~1200kcal, 유지: ~1600kcal, 증량: ~1900kcal
diet_db = {
    "체중 감량 (Diet)": {
        "breakfast": {"menu": "그릭요거트 & 베리류", "kcal": 200},
        "lunch": {"menu": "닭가슴살 샐러드 & 단호박", "kcal": 350},
        "dinner": {"menu": "연어 포케 (밥 적게)", "kcal": 400},
        "snack": {"menu": "방울토마토 & 아몬드 5알", "kcal": 100},
        "total_intake": 1050
    },
    "근육 증가 (Toning)": {
        "breakfast": {"menu": "베이글 1/2 & 스크램블 에그", "kcal": 350},
        "lunch": {"menu": "일반식 (잡곡밥 1/2공기)", "kcal": 550},
        "dinner": {"menu": "소고기 안심 & 구운 야채", "kcal": 450},
        "snack": {"menu": "프로틴 쉐이크 & 바나나", "kcal": 250},
        "total_intake": 1600
    },
    "건강 유지 (Balance)": {
        "breakfast": {"menu": "사과 1개 & 삶은 계란 2개", "kcal": 250},
        "lunch": {"menu": "비빔밥 (고추장 적게)", "kcal": 500},
        "dinner": {"menu": "두부면 파스타 & 닭가슴살", "kcal": 350},
        "snack": {"menu": "두유 & 견과류", "kcal": 150},
        "total_intake": 1250
    }
}

# 4. 사이드바 설정
with st.sidebar:
    st.header("⚙️ 퍼스널 설정")
    name = st.text_input("닉네임", "건강한습관")
    target_part = st.selectbox("오늘의 운동 목표", list(workout_db.keys()))
    diet_goal = st.radio("식단 목표", list(diet_db.keys()))
    
    st.write("---")
    # 기준 변경 안내
    st.caption("※ 칼로리는 성인 여성 60kg 기준 추정치입니다.")
    st.caption("(기초대사량 및 활동량에 따라 개인차가 있을 수 있습니다.)")

# 5. 메인 로직
w_data = workout_db[target_part]
d_data = diet_db[diet_goal]

st.title(f"🧘‍♀️ {name}님의 웰니스 리포트")
st.markdown("여성 평균 신체 데이터를 기반으로 분석된 오늘의 루틴입니다.")
st.divider()

# [섹션 1] 칼로리 대시보드
col1, col2, col3 = st.columns(3)
col1.metric("🔥 운동 소모", f"-{w_data['total_burn']} kcal", "Target Burn")
col2.metric("🥗 식단 섭취", f"+{d_data['total_intake']} kcal", "Clean Food")
net_kcal = d_data['total_intake'] - w_data['total_burn']
col3.metric("⚖️ 에너지 밸런스", f"{net_kcal} kcal", "Today's Total")

st.write("") 

# [섹션 2] 운동 & 식단 카드
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("💪 오늘의 운동 (Workout)")
    for ex in w_data['exercises']:
        st.markdown(f"""
        <div class="card workout-card">
            <div class="card-title">📌 {ex['name']}</div>
            <p style="color:#666; margin-bottom:5px;">{ex['set']}</p>
            <span class="kcal-tag">🔥 약 {ex['kcal']} kcal 소모</span>
        </div>
        """, unsafe_allow_html=True)
        
    cardio = w_data['cardio']
    st.markdown(f"""
    <div class="card workout-card" style="background-color: #FFF5F5;">
        <div class="card-title">🏃 유산소 마무리</div>
        <p style="color:#666; margin-bottom:5px;">{cardio['name']}</p>
        <span class="kcal-tag">🔥 약 {cardio['kcal']} kcal 소모</span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.subheader("🥑 오늘의 식단 (Diet)")
    meals = [
        ("🌅 아침", d_data['breakfast']),
        ("☀️ 점심", d_data['lunch']),
        ("🌙 저녁", d_data['dinner']),
        ("🍪 간식", d_data['snack'])
    ]
    
    for title, info in meals:
        st.markdown(f"""
        <div class="card food-card">
            <div class="card-title">{title}</div>
            <p style="color:#666; margin-bottom:5px;">{info['menu']}</p>
            <span class="kcal-tag" style="color: #2b8a3e; background-color: #ebfbee;">
                🥗 {info['kcal']} kcal
            </span>
        </div>
        """, unsafe_allow_html=True)

# 6. 하단 인터랙션
st.divider()
if st.button("✨ 오늘 하루 완료! (기록하기)"):
    with st.spinner("데이터 저장 중..."):
        time.sleep(1)
    st.balloons()
    st.success(f"{name}님, 오늘도 건강한 하루를 보내셨네요! 내일도 함께해요! 💖")
