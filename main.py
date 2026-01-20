import streamlit as st
import time
from urllib.parse import quote

# 1. 페이지 설정
st.set_page_config(
    page_title="My AI Health Coach",
    page_icon="🧬",
    layout="wide"
)

# 2. CSS 스타일링
st.markdown("""
    <style>
    .big-font { font-size: 20px !important; font-weight: bold; }
    .card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        background-color: white;
    }
    .workout-card { border-left: 6px solid #FF4B4B; }
    .diet-card { border-left: 6px solid #00C851; }
    .youtube-btn {
        background-color: #FF0000;
        color: white !important;
        padding: 6px 12px;
        border-radius: 20px;
        text-decoration: none;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-top: 8px;
    }
    .youtube-btn:hover { background-color: #CC0000; }
    </style>
    """, unsafe_allow_html=True)

# 3. 계산 함수 (해리스-베네딕트 공식 수정판)
def calculate_metrics(height, weight, age, gender):
    # BMI 계산
    bmi = weight / ((height / 100) ** 2)
    
    # BMR(기초대사량) 계산
    if gender == "남성":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    return bmi, bmr

# 4. 사이드바: 사용자 정보 입력
with st.sidebar:
    st.header("📋 내 신체 정보 입력")
    name = st.text_input("닉네임", "도전하는나")
    gender = st.radio("성별", ["여성", "남성"])
    age = st.number_input("나이 (만)", 20, 80, 25)
    height = st.number_input("키 (cm)", 140, 200, 163)
    current_weight = st.number_input("현재 몸무게 (kg)", 30, 150, 60)
    target_weight = st.number_input("🎯 목표 몸무게 (kg)", 30, 150, 55)
    
    st.divider()
    
    # 목표 분석
    weight_diff = current_weight - target_weight
    if weight_diff > 0:
        goal_type = "lose" # 감량
        goal_text = f"📉 {weight_diff:.1f}kg 감량 필요"
        color = "red"
    elif weight_diff < 0:
        goal_type = "gain" # 증량
        goal_text = f"📈 {abs(weight_diff):.1f}kg 증량 필요"
        color = "blue"
    else:
        goal_type = "maintain"
        goal_text = "✨ 현재 체중 유지"
        color = "green"
        
    st.markdown(f"### 현재 목표: :{color}[{goal_text}]")
    if st.button("솔루션 생성하기 🧬"):
        st.session_state['analyzed'] = True

# 5. 메인 로직
st.title(f"🧬 {name}님의 맞춤형 목표 달성 플랜")

if 'analyzed' not in st.session_state:
    st.info("👈 왼쪽 사이드바에 정보를 입력하고 '솔루션 생성하기'를 눌러주세요!")
else:
    # (1) 신체 지표 분석 및 칼로리 목표 설정
    bmi, bmr = calculate_metrics(height, current_weight, age, gender)
    tdee = bmr * 1.55 # 활동대사량 (보통 활동 기준)
    
    if goal_type == "lose":
        target_kcal = tdee - 500  # 감량 시 -500kcal
        diet_desc = "체지방 감소를 위한 '저탄수화물 고단백' 식단"
        workout_desc = "지방 연소를 극대화하는 '서킷 트레이닝 & 유산소'"
    elif goal_type == "gain":
        target_kcal = tdee + 300  # 증량 시 +300kcal
        diet_desc = "근성장을 위한 '탄수화물 및 단백질 충분' 식단"
        workout_desc = "근비대를 위한 '고중량 저반복 웨이트'"
    else:
        target_kcal = tdee
        diet_desc = "건강 유지를 위한 '탄단지 밸런스' 식단"
        workout_desc = "체력 유지를 위한 '전신 근력 & 가벼운 유산소'"

    # (2) 대시보드 출력
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("BMI 지수", f"{bmi:.1f}", "정상: 18.5~23")
    c2.metric("기초대사량(BMR)", f"{int(bmr)} kcal")
    c3.metric("하루 권장 칼로리", f"{int(target_kcal)} kcal", f"목표 달성용")
    c4.metric("목표 체중까지", f"{abs(weight_diff):.1f} kg", "남음")
    
    # BMI 상태 바
    st.write("###### 📊 나의 BMI 위치")
    bmi_progress = min(max((bmi - 10) / 30, 0.0), 1.0) # 10~40 범위 정규화
    st.progress(bmi_progress)
    
    # (3) 추천 로직 데이터베이스 (조건부 선택)
    if goal_type == "lose":
        # 다이어트 운동 리스트
        strength_list = [
            ("버피 테스트", "전신 체지방 연소 끝판왕"),
            ("마운틴 클라이머", "복근과 유산소를 동시에"),
            ("스쿼트 & 숄더프레스", "상하체 동시 자극으로 칼로리 태우기")
        ]
        cardio_rec = "인터벌 러닝 (1분 전력질주 / 2분 걷기) x 5세트"
        
        # 다이어트 식단
        meals = {
            "아침": "그릭요거트(100g), 사과 반쪽, 삶은 계란 1개",
            "점심": "현미밥 1/2공기, 닭가슴살 샐러드, 오리엔탈 드레싱",
            "저녁": "단호박 찜, 연어 구이, 아스파라거스",
            "간식": "방울토마토, 아몬드 10알"
        }
        
    elif goal_type == "gain":
        # 벌크업 운동 리스트
        strength_list = [
            ("벤치 프레스", "상체 근육 매스 증가"),
            ("데드리프트", "전신 근력 및 등 근육 발달"),
            ("바벨 스쿼트", "하체 근육 및 남성 호르몬 촉진")
        ]
        cardio_rec = "가벼운 사이클 15분 (워밍업 위주)"
        
        # 벌크업 식단
        meals = {
            "아침": "오트밀 죽, 스크램블 에그 3개, 바나나 1개",
            "점심": "백미밥, 제육볶음(살코기 위주), 쌈채소",
            "저녁": "파스타(면 많이), 부채살 스테이크",
            "간식": "프로틴 쉐이크, 식빵 2장 & 땅콩버터"
        }
        
    else: # 유지
        strength_list = [
            ("플랭크", "코어 안정화"),
            ("런지", "균형 감각 및 하체 라인"),
            ("푸시업", "기초 상체 근력")
        ]
        cardio_rec = "조깅 30분 or 수영"
        
        meals = {
            "아침": "통밀 토스트, 계란후라이, 우유",
            "점심": "한식 일반식 (국물 적게)",
            "저녁": "닭가슴살 카레라이스",
            "간식": "하루견과 1봉"
        }

    # (4) 2단 컬럼 출력 (운동 vs 식단)
    st.markdown("---")
    col_left, col_right = st.columns([1, 1])
    
    # 왼쪽: 운동 추천
    with col_left:
        st.subheader(f"🏋️‍♂️ {workout_desc}")
        
        # 근력 운동 반복 출력
        for ex_name, ex_desc in strength_list:
            search_query = quote(f"{ex_name} 올바른 자세")
            yt_url = f"https://www.youtube.com/results?search_query={search_query}"
            
            st.markdown(f"""
            <div class="card workout-card">
                <div style="font-weight:bold; font-size:1.1em;">{ex_name}</div>
                <div style="color:#666; font-size:0.9em;">{ex_desc}</div>
                <a href="{yt_url}" target="_blank" class="youtube-btn">▶️ 유튜브 운동법 보기</a>
            </div>
            """, unsafe_allow_html=True)
            
        # 유산소 카드
        st.info(f"🏃 **추천 유산소**: {cardio_rec}")

    # 오른쪽: 식단 추천
    with col_right:
        st.subheader(f"🥗 {diet_desc}")
        
        st.markdown(f"""
        <div class="card diet-card">
            <h4 style="margin-top:0;">📋 오늘의 식단 플랜</h4>
            <p><strong>🌅 아침:</strong> {meals['아침']}</p>
            <p><strong>☀️ 점심:</strong> {meals['점심']}</p>
            <p><strong>🌙 저녁:</strong> {meals['저녁']}</p>
            <p><strong>🍪 간식:</strong> {meals['간식']}</p>
            <hr>
            <p style="text-align:right; font-weight:bold; color:#00C851;">
                목표 섭취량: 약 {int(target_kcal)} kcal
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.warning("💡 **Tip**: 물은 하루 2리터 이상 충분히 섭취하세요!")

    # 푸터
    st.divider()
    st.caption("※ 본 결과는 일반적인 공식을 기반으로 한 추정치이며, 전문 의료 상담을 대체할 수 없습니다.")
