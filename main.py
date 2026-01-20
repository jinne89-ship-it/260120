import streamlit as st
import time
from urllib.parse import quote

# 1. 페이지 설정
st.set_page_config(
    page_title="My AI Health Coach Pro",
    page_icon="🧬",
    layout="wide"
)

# 2. CSS 스타일링
st.markdown("""
    <style>
    .card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        background-color: white;
    }
    .workout-card { border-left: 5px solid #FF4B4B; }
    .diet-card { border-left: 5px solid #00C851; }
    
    .youtube-btn {
        background-color: #FF0000;
        color: white !important;
        padding: 5px 10px;
        border-radius: 15px;
        text-decoration: none;
        font-size: 0.8rem;
        display: inline-block;
        margin-top: 5px;
    }
    .youtube-btn:hover { background-color: #CC0000; }
    
    /* 탭 폰트 크기 조절 */
    button[data-baseweb="tab"] {
        font-size: 1.2rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 함수 정의
def calculate_metrics(height, weight, age, gender):
    bmi = weight / ((height / 100) ** 2)
    if gender == "남성":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmi, bmr

# 카드 렌더링 함수 (코드 중복 방지)
def render_solution(plan_name, workout_list, meal_plan, cardio_txt, kcal_target):
    st.markdown(f"### {plan_name}")
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("💪 운동 루틴")
        for ex_name, ex_desc in workout_list:
            search_query = quote(f"{ex_name} 자세 운동법")
            yt_url = f"https://www.youtube.com/results?search_query={search_query}"
            st.markdown(f"""
            <div class="card workout-card">
                <strong>📌 {ex_name}</strong><br>
                <span style="font-size:0.9em; color:#666;">{ex_desc}</span><br>
                <a href="{yt_url}" target="_blank" class="youtube-btn">▶️ 영상 보기</a>
            </div>
            """, unsafe_allow_html=True)
        st.info(f"🏃 **유산소**: {cardio_txt}")

    with c2:
        st.subheader("🥗 식단 플랜")
        st.markdown(f"""
        <div class="card diet-card">
            <p><strong>🌅 아침:</strong> {meal_plan['아침']}</p>
            <p><strong>☀️ 점심:</strong> {meal_plan['점심']}</p>
            <p><strong>🌙 저녁:</strong> {meal_plan['저녁']}</p>
            <p><strong>🍪 간식:</strong> {meal_plan['간식']}</p>
            <hr>
            <strong style="color:#00C851;">🎯 목표: 하루 {int(kcal_target)} kcal</strong>
        </div>
        """, unsafe_allow_html=True)

# 4. 사이드바 입력
with st.sidebar:
    st.header("📋 내 정보 입력")
    name = st.text_input("닉네임", "건강한나")
    gender = st.radio("성별", ["여성", "남성"])
    age = st.number_input("나이", 20, 80, 26)
    height = st.number_input("키 (cm)", 140, 200, 163)
    curr_w = st.number_input("현재 체중 (kg)", 30, 150, 60)
    target_w = st.number_input("목표 체중 (kg)", 30, 150, 52)
    
    st.divider()
    
    diff = curr_w - target_w
    if diff > 0:
        goal_type = "lose"
        goal_msg = f"📉 {diff:.1f}kg 감량"
    elif diff < 0:
        goal_type = "gain"
        goal_msg = f"📈 {abs(diff):.1f}kg 증량"
    else:
        goal_type = "maintain"
        goal_msg = "✨ 유지"
        
    st.markdown(f"### 목표: :{('red' if diff>0 else 'blue')}[{goal_msg}]")
    
    if st.button("AI 솔루션 받기 🧬"):
        st.session_state['run'] = True

# 5. 메인 화면
st.title(f"🧬 {name}님을 위한 3가지 맞춤 전략")

if 'run' not in st.session_state:
    st.info("👈 사이드바에서 정보를 입력하고 버튼을 눌러주세요.")
else:
    # 지표 계산
    bmi, bmr = calculate_metrics(height, curr_w, age, gender)
    tdee = bmr * 1.55 # 활동대사량
    
    # 목표 칼로리 설정
    if goal_type == "lose":
        target_kcal = tdee - 500
    elif goal_type == "gain":
        target_kcal = tdee + 300
    else:
        target_kcal = tdee

    # 상단 지표 표시
    c1, c2, c3 = st.columns(3)
    c1.metric("BMI", f"{bmi:.1f}")
    c2.metric("기초대사량", f"{int(bmr)} kcal")
    c3.metric("권장 섭취", f"{int(target_kcal)} kcal")
    st.divider()
    
    # 탭 생성 (솔루션 3가지)
    tab1, tab2, tab3 = st.tabs(["🏠 옵션 A: 홈트레이닝", "🏋️ 옵션 B: 헬스장(Gym)", "🧘 옵션 C: 라이프스타일"])

    # --- 데이터 정의 (목표에 따라 분기) ---
    
    # [공통] 감량 식단 vs 증량 식단
    if goal_type == "lose":
        diet_A = {"아침":"사과, 계란2", "점심":"일반식(밥1/2)", "저녁":"닭가슴살 샐러드", "간식":"아몬드"} # 간편
        diet_B = {"아침":"오트밀, 프로틴", "점심":"현미밥, 소고기", "저녁":"고구마, 닭가슴살", "간식":"방울토마토"} # 정석
        diet_C = {"아침":"그릭요거트", "점심":"포케 샐러드", "저녁":"두부면 파스타", "간식":"두유"} # 트렌디
    elif goal_type == "gain":
        diet_A = {"아침":"토스트, 우유", "점심":"제육덮밥", "저녁":"삼겹살 구이", "간식":"바나나"}
        diet_B = {"아침":"닭가슴살, 고구마", "점심":"소고기, 밥200g", "저녁":"파스타, 생선", "간식":"프로틴쉐이크"}
        diet_C = {"아침":"베이글, 계란", "점심":"부채살 스테이크", "저녁":"리조또", "간식":"단백질바"}
    else: # 유지
        diet_A = diet_B = diet_C = {"아침":"토스트", "점심":"한식", "저녁":"생선구이", "간식":"과일"}

    # --- 탭 1: 홈트레이닝 (집에서 맨몸으로) ---
    with tab1:
        if goal_type == "lose":
            w_list = [("버피 테스트", "전신 유산소성 근력"), ("스쿼트", "하체 기본"), ("플랭크", "코어 강화")]
            cardio = "제자리 뛰기 20분"
        else:
            w_list = [("푸시업", "상체 발달"), ("런지", "하체 밸런스"), ("체어 딥스", "팔 근육")]
            cardio = "동네 산책 30분"
        
        render_solution("🏠 집에서 간편하게 (No Equipment)", w_list, diet_A, cardio, target_kcal)

    # --- 탭 2: 헬스장 (기구 사용 정석) ---
    with tab2:
        if goal_type == "lose":
            w_list = [("레그 프레스", "하체 고립"), ("랫 풀 다운", "등 라인"), ("체스트 프레스", "가슴 탄력")]
            cardio = "러닝머신 인터벌 30분"
        else:
            w_list = [("벤치 프레스", "3대 운동(가슴)"), ("데드리프트", "3대 운동(전신)"), ("바벨 스쿼트", "3대 운동(하체)")]
            cardio = "사이클 15분 (웜업)"
            
        render_solution("🏋️ 헬스장에서 확실하게 (FM Style)", w_list, diet_B, cardio, target_kcal)

    # --- 탭 3: 라이프스타일/필라테스 (유연성 및 라인) ---
    with tab3:
        w_list = [("폼롤러 스트레칭", "혈액순환 및 붓기제거"), ("필라테스 헌드레드", "복부 코어"), ("브릿지 자세", "힙업 효과")]
        cardio = "수영 또는 빠르게 걷기"
        
        render_solution("🧘 예쁜 라인 만들기 (Balance)", w_list, diet_C, cardio, target_kcal)

    # 하단 마무리
    st.divider()
    if st.button("✨ 이 솔루션으로 시작하기"):
        st.balloons()
        st.success("훌륭한 선택입니다! 오늘부터 1일입니다! 🎉")
