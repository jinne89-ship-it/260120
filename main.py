import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="AI 퍼스널 헬스 케어",
    page_icon="🥗",
    layout="wide"
)

# 2. 스타일링 (CSS) - 운동(Red)과 식단(Green) 테마 분리
st.markdown("""
    <style>
    /* 공통 카드 스타일 */
    .card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        background-color: white;
    }
    /* 운동 카드 (Red) */
    .workout-card {
        border-top: 5px solid #FF4B4B;
    }
    /* 식단 카드 (Green) */
    .food-card {
        border-top: 5px solid #28a745;
    }
    .card-title {
        font-size: 1.1em;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    .kcal-tag {
        font-size: 0.9em;
        font-weight: bold;
        color: #666;
        background-color: #f1f3f5;
        padding: 2px 8px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터베이스 정의

# [운동 DB] 부위별 루틴 + 소모 칼로리(추정치)
workout_db = {
    "상체 (가슴/등)": {
        "exercises": [
            {"name": "벤치 프레스", "set": "4세트", "kcal": 100},
            {"name": "랫 풀 다운", "set": "4세트", "kcal": 90},
            {"name": "팔굽혀펴기", "set": "3세트", "kcal": 60}
        ],
        "cardio": {"name": "로잉 머신 20분", "kcal": 220},
        "total_burn": 470
    },
    "하체 (허벅지/힙)": {
        "exercises": [
            {"name": "스쿼트", "set": "5세트", "kcal": 150},
            {"name": "런지", "set": "3세트", "kcal": 100},
            {"name": "레그 익스텐션", "set": "3세트", "kcal": 80}
        ],
        "cardio": {"name": "계단 오르기 20분", "kcal": 250},
        "total_burn": 580
    },
    "전신 (다이어트)": {
        "exercises": [
            {"name": "버피 테스트", "set": "3세트", "kcal": 180},
            {"name": "케틀벨 스윙", "set": "4세트", "kcal": 140},
            {"name": "마운틴 클라이머", "set": "3세트", "kcal": 100}
        ],
        "cardio": {"name": "인터벌 러닝 20분", "kcal": 280},
        "total_burn": 700
    }
}

# [식단 DB] 목표별 식단 + 섭취 칼로리
diet_db = {
    "체중 감량 (Diet)": {
        "breakfast": {"menu": "그릭요거트 & 블루베리", "kcal": 250},
        "lunch": {"menu": "닭가슴살 샐러드 & 고구마", "kcal": 450},
        "dinner": {"menu": "연어 스테이크 & 야채 구이", "kcal": 400},
        "snack": {"menu": "아몬드 10알", "kcal": 70},
        "total_intake": 1170
    },
    "근육 증가 (Bulking)": {
        "breakfast": {"menu": "오트밀 & 프로틴 쉐이크", "kcal": 450},
        "lunch": {"menu": "현미밥 & 소불고기", "kcal": 700},
        "dinner": {"menu": "파스타 & 닭다리살", "kcal": 650},
        "snack": {"menu": "바나나 2개 & 삶은 계란", "kcal": 250},
        "total_intake": 2050
    },
    "건강 유지 (Balance)": {
        "breakfast": {"menu": "사과 & 통밀 토스트", "kcal": 350},
        "lunch": {"menu": "일반식 (한식 백반)", "kcal": 600},
        "dinner": {"menu": "두부 샐러드 & 닭가슴살", "kcal": 400},
        "snack": {"menu": "하루견과 1봉", "kcal": 150},
        "total_intake": 1500
    }
}

# 4. 사이드바 설정
with st.sidebar:
    st.header("⚙️ 내 몸 상태 설정")
    name = st.text_input("닉네임", "건강지킴이")
    target_part = st.selectbox("오늘의 운동 부위", list(workout_db.keys()))
    diet_goal = st.radio("식단 목표", list(diet_db.keys()))
    
    st.write("---")
    st.caption("※ 칼로리는 성인 남성 75kg 기준 추정치입니다.")

# 5. 메인 로직
# 데이터 로드
w_data = workout_db[target_part]
d_data = diet_db[diet_goal]

st.title(f"📊 {name}님의 데일리 헬스 리포트")
st.markdown("운동 루틴과 영양 섭취 계획을 한눈에 확인하세요!")
st.divider()

# [섹션 1] 칼로리 대시보드 (Metrics)
col1, col2, col3 = st.columns(3)
col1.metric("🔥 운동 소모 칼로리", f"-{w_data['total_burn']} kcal", "지방 연소 중")
col2.metric("🥗 식단 섭취 칼로리", f"+{d_data['total_intake']} kcal", "에너지 보충")
net_kcal = d_data['total_intake'] - w_data['total_burn']
col3.metric("⚖️ 오늘의 밸런스", f"{net_kcal} kcal", "잉여/부족 에너지")

st.write("") # 여백

# [섹션 2] 화면 분할 (좌: 운동 / 우: 식단)
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("🏋️‍♂️ 오늘의 운동 루틴")
    
    # 근력 운동 카드
    for ex in w_data['exercises']:
        st.markdown(f"""
        <div class="card workout-card">
            <div class="card-title">💪 {ex['name']}</div>
            <p>{ex['set']} 진행</p>
            <span class="kcal-tag">🔥 {ex['kcal']} kcal 소모</span>
        </div>
        """, unsafe_allow_html=True)
        
    # 유산소 운동 카드
    cardio = w_data['cardio']
    st.markdown(f"""
    <div class="card workout-card" style="background-color: #fff5f5;">
        <div class="card-title">🏃 마무리 유산소</div>
        <p>{cardio['name']}</p>
        <span class="kcal-tag">🔥 {cardio['kcal']} kcal 소모</span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.subheader("🥦 추천 식단 가이드")
    
    # 식단 카드 (아침/점심/저녁/간식)
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
            <p>{info['menu']}</p>
            <span class="kcal-tag" style="color: #155724; background-color: #d4edda;">
                🥗 {info['kcal']} kcal 섭취
            </span>
        </div>
        """, unsafe_allow_html=True)

# 6. 하단 인터랙션
st.divider()
if st.button("✅ 오늘 하루 기록 저장하기"):
    with st.spinner("데이터 동기화 중..."):
        time.sleep(1)
    st.success(f"{name}님, 오늘 하루 {w_data['total_burn']}kcal를 태우고 건강한 식단을 계획하셨네요! 멋집니다! 🎉")
    st.balloons()
