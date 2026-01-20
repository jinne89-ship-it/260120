import streamlit as st
import pandas as pd
import time

# 1. 페이지 설정 (가장 상단)
st.set_page_config(
    page_title="오늘의 운동 루틴 추천",
    page_icon="💪",
    layout="wide"
)

# 2. 커스텀 CSS (카드 디자인 및 버튼 스타일)
st.markdown("""
    <style>
    .workout-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-top: 5px solid #FF4B4B;
        transition: transform 0.3s;
    }
    .workout-card:hover {
        transform: scale(1.02);
    }
    .card-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    .card-desc {
        color: #666;
        font-size: 0.9em;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 운동 데이터베이스 (딕셔너리 구조)
# 부위별: [근력 운동 리스트], [추천 유산소]
workout_db = {
    "상체 (가슴/등/어깨)": {
        "strength": [
            {"name": "푸시업 (Push Up)", "set": "3세트 x 12회", "desc": "가슴과 삼두근 발달에 기초가 되는 운동"},
            {"name": "덤벨 숄더 프레스", "set": "3세트 x 10회", "desc": "어깨의 볼륨감을 키워주는 필수 운동"},
            {"name": "벤트오버 로우", "set": "3세트 x 12회", "desc": "등 근육의 선명도를 높여주는 당기기 운동"}
        ],
        "cardio": "로잉 머신 (15분) 또는 배틀 로프 (10분)"
    },
    "하체 (허벅지/엉덩이)": {
        "strength": [
            {"name": "맨몸 스쿼트", "set": "4세트 x 15회", "desc": "하체 운동의 꽃, 엉덩이와 허벅지 전체 자극"},
            {"name": "런지 (Lunge)", "set": "3세트 x 12회(양발)", "desc": "균형 감각과 허벅지 앞쪽 자극"},
            {"name": "카프 레이즈", "set": "3세트 x 20회", "desc": "탄탄한 종아리 라인을 만드는 운동"}
        ],
        "cardio": "실내 자전거 (20분) 또는 계단 오르기 (15분)"
    },
    "코어 (복근/허리)": {
        "strength": [
            {"name": "플랭크 (Plank)", "set": "3세트 x 1분 버티기", "desc": "전신 코어 안정성을 높이는 최고의 운동"},
            {"name": "크런치", "set": "3세트 x 15회", "desc": "상복부를 쥐어짜는 듯한 자극 집중"},
            {"name": "슈퍼맨 자세", "set": "3세트 x 15회", "desc": "허리(기립근)를 강화하여 통증 예방"}
        ],
        "cardio": "마운틴 클라이머 (3세트 x 30초) 또는 버피 테스트"
    },
    "전신 (Full Body)": {
        "strength": [
            {"name": "데드리프트", "set": "3세트 x 10회", "desc": "전신의 근력을 사용하는 고강도 운동"},
            {"name": "케틀벨 스윙", "set": "3세트 x 15회", "desc": "유산소와 근력을 동시에 잡는 운동"},
            {"name": "쓰러스터", "set": "3세트 x 10회", "desc": "스쿼트와 프레스를 결합한 전신 운동"}
        ],
        "cardio": "인터벌 러닝 (20분) 또는 수영"
    }
}

# 4. 사이드바 (사용자 입력)
with st.sidebar:
    st.header("⚙️ 운동 설정")
    name = st.text_input("닉네임을 입력하세요", "헬린이")
    target_part = st.selectbox("오늘 자극할 부위는?", list(workout_db.keys()))
    intensity = st.select_slider("오늘의 컨디션은?", options=["피곤함", "보통", "최고조🔥"])
    
    st.write("---")
    st.info("💡 팁: 꾸준함이 득근의 지름길입니다!")

# 5. 메인 콘텐츠
st.title(f"🔥 {name}님의 오늘의 운동 처방")
st.write(f"선택하신 **'{target_part}'** 강화를 위한 최적의 루틴입니다.")
st.divider()

# 데이터 로드
selected_routine = workout_db[target_part]

# 2단 컬럼 레이아웃
col1, col2 = st.columns([1.5, 1])

# 왼쪽 컬럼: 근력 운동 (Card UI 적용)
with col1:
    st.subheader("🏋️‍♀️ 근력 운동 (Strength)")
    for exercise in selected_routine["strength"]:
        # 유튜브 검색 링크 생성
        search_url = f"https://www.youtube.com/results?search_query={exercise['name']} 운동법"
        
        st.markdown(f"""
        <div class="workout-card">
            <div class="card-title">📌 {exercise['name']}</div>
            <div class="card-desc">{exercise['desc']}</div>
            <div style="margin-top: 10px; font-weight: bold; color: #444;">🎯 목표: {exercise['set']}</div>
            <div style="margin-top: 10px;">
                <a href="{search_url}" target="_blank" style="text-decoration: none; color: #FF4B4B; font-size: 0.9em;">
                    ▶️ 유튜브에서 자세세 확인하기
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 오른쪽 컬럼: 유산소 & 완료 체크
with col2:
    st.subheader("🏃 유산소 (Cardio)")
    st.markdown(f"""
    <div class="workout-card" style="border-top: 5px solid #1E90FF;">
        <div class="card-title">🔥 지방 태우기</div>
        <div class="card-desc">근력 운동 후 아래 유산소를 진행하세요.</div>
        <h3 style="color: #1E90FF; margin-top:15px;">{selected_routine['cardio']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("") # 여백
    st.write("---")
    
    # 운동 완료 기능
    st.write("### ✅ 운동 완료 체크")
    if st.button("오늘 운동 끝내기! (클릭)"):
        with st.spinner("기록 저장 중..."):
            time.sleep(1)
        st.balloons()
        st.success(f"수고하셨습니다, {name}님! 오늘 루틴을 완벽하게 소화하셨네요! 🎉")

# 6. 푸터
st.markdown("---")
st.caption("© 2026 Smart Health Care System | Developed with Streamlit")
