import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="2026 오늘의 뉴스 브리핑",
    page_icon="📰",
    layout="wide"
)

# 2. 커스텀 CSS로 스타일링 (색감 및 폰트)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .news-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border-left: 5px solid #FF4B4B;
    }
    .section-title {
        color: #1f77b4;
        font-size: 24px;
        font-weight: bold;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 헤더 섹션
st.markdown("<h1 style='text-align: center; color: #2E3192;'>🗞️ 2026년 1월 20일 주요 뉴스 Briefing</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>실시간 정치, 사회, 문화 이슈를 한눈에 확인하세요! ✨</p>", unsafe_allow_html=True)
st.divider()

# 4. 오늘의 주요 지표 (화려함 추가)
col_a, col_b, col_c = st.columns(3)
col_a.metric(label="🌡️ 서울 기온", value="-4.2°C", delta="-2.1°C (한파)")
col_b.metric(label="📈 대통령 지지율", value="61%", delta="3.2% (상승)")
col_c.metric(label="🇰🇷 K-컬처 지수", value="98.5", delta="0.5 (안정)")

# 5. 뉴스 데이터 정의 (2026.01.20 실제 이슈 반영)
news_data = {
    "🏛️ 정치 (Politics)": [
        {"title": "김민석 국무총리 주재 '제22차 국가테러대책위원회' 개최", "desc": "가덕도 피습 사건 10년을 맞아 테러 예방 체계 전반을 보완하고 K-민주주의 안전 강화 선언."},
        {"title": "이혜훈 인사청문회 파행... 여야 '절차적 문제' 공방", "desc": "중수청·공소청 논란과 맞물려 야당 간사 간 합의 불발로 청문회 일정 연기 가능성 대두."},
        {"title": "장동혁 국민의힘 대표 '단식 6일차' 돌입", "desc": "한동훈 전 대표 사과 반응 및 당무위 감찰 요구 등을 둘러싸고 보수 진영 내 긴장 고조."}
    ],
    "⚖️ 사회 (Society)": [
        {"title": "한국노총 '근로자 추정제도' 입법 보완 강력 요구", "desc": "플랫폼 노동자와 프리랜서 보호를 위해 실효성 있는 노동법 보호 체계 마련 촉구 성명 발표."},
        {"title": "전국적 빙판길 사고 비상... 강추위 속 낙상 주의보", "desc": "영하권 날씨가 이어지며 출근길 빙판사고 급증, 지자체 제설 작업 인력 풀가동 중."},
        {"title": "남양주 묵현리 도시계획도로 미집행 논란 심화", "desc": "20년째 방치된 도로 문제로 주민 불만 고조, 보궐선거 앞두고 평택 등 지역 정가 하마평 무성."}
    ],
    "🎨 문화/경제 (Culture)": [
        {"title": "이재명 대통령 '2026년은 대도약의 원년' 선언", "desc": "지방·분배·안전·문화·평화 5대 전략 제시하며 K-컬처 해외 진출 적극 지원 약속."},
        {"title": "다보스 포럼 '트럼프 대통령 특별연설'에 세계 이목 집중", "desc": "국가원수 자격으로 참석하는 트럼프 대통령의 외교 담판이 글로벌 문화·경제 지형에 미칠 영향 분석."},
        {"title": "한반도 정세 변화와 'K-민주주의' 문화 확산", "desc": "남북 관계 회복을 위한 사회적 대화 확대와 9·19 군사합의 복원 가능성에 대한 문화계 담론 형성."}
    ]
}

# 6. 뉴스 본문 출력 (3단 컬럼 구성)
cols = st.columns(3)

for i, (category, news_list) in enumerate(news_data.items()):
    with cols[i]:
        st.markdown(f"<div class='section-title'>{category}</div>", unsafe_allow_html=True)
        for item in news_list:
            with st.container():
                st.markdown(f"""
                    <div class="news-card">
                        <h4 style='margin-bottom: 5px;'>📍 {item['title']}</h4>
                        <p style='font-size: 0.9em; color: #444;'>{item['desc']}</p>
                    </div>
                """, unsafe_allow_html=True)

# 7. 푸터 및 인터랙션
st.divider()
if st.button("🎉 오늘 하루도 파이팅! (클릭)"):
    st.balloons()
    st.confetti() # 설치 환경에 따라 작동 (최신 버전 지원)

st.caption("Produced by Gemini News Bot | 2026 Duksung Educational Innovation Center Support")
