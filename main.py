import streamlit as st
import pandas as pd

# 🎨 페이지 설정 (가장 상단에 위치해야 함)
st.set_page_config(
    page_title="내 꿈을 찾는 MBTI 진로 탐색",
    page_icon="🚀",
    layout="wide"
)

# ✨ 커스텀 스타일 적용 (CSS)
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .title-text {
        text-align: center;
        color: #1E1E1E;
        font-family: 'Nanum Gothic', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 🏆 제목 및 헤더
st.markdown("<h1 class='title-text'>🌈 MBTI 맞춤형 진로 탐색 센터 🚀</h1>", unsafe_allow_html=True)
st.write("---")

# 📊 데이터 정의 (MBTI별 특징 및 직업)
mbti_data = {
    "ISTJ": {"emoji": "🧐", "desc": "청렴결백한 논리주의자", "jobs": ["회계사", "공무원", "군인", "데이터 분석가"]},
    "ISFJ": {"emoji": "🛡️", "desc": "용감한 수호자", "jobs": ["간호사", "초등교사", "사회복지사", "도서관장"]},
    "INFJ": {"emoji": "🧙", "desc": "선의의 옹호자", "jobs": ["상담사", "작가", "교육혁신가", "인사전문가"]},
    "INTJ": {"emoji": "🧠", "desc": "용의주도한 전략가", "jobs": ["전략 기획가", "대학교수", "IT 아키텍트", "연구원"]},
    "ISTP": {"emoji": "🛠️", "desc": "만능 재주꾼", "jobs": ["엔지니어", "파일럿", "소방관", "시스템 개발자"]},
    "ISFP": {"emoji": "🎨", "desc": "호기심 많은 예술가", "jobs": ["디자이너", "작곡가", "수의사", "조경가"]},
    "INFP": {"emoji": "🌻", "desc": "열정적인 중재자", "jobs": ["심리치료사", "에디터", "일러스트레이터", "인권활동가"]},
    "INTP": {"emoji": "🔬", "desc": "논리적인 사색가", "jobs": ["프로그래머", "수학자", "철학자", "경제학자"]},
    "ESTP": {"emoji": "⚡", "desc": "모험을 즐기는 사업가", "jobs": ["사업가", "스포츠 매니저", "경찰관", "부동산 중개인"]},
    "ESFP": {"emoji": "🥳", "desc": "자유로운 영혼의 연예인", "jobs": ["배우", "이벤트 기획자", "홍보 전문가", "승무원"]},
    "ENFP": {"emoji": "🎈", "desc": "재기발랄한 활동가", "jobs": ["마케터", "방송 PD", "카운슬러", "여행가"]},
    "ENTP": {"emoji": "💡", "desc": "뜨거운 논쟁을 즐기는 변론가", "jobs": ["변호사", "카피라이터", "정치인", "창업가"]},
    "ESTJ": {"emoji": "📊", "desc": "엄격한 관리자", "jobs": ["경영자", "은행원", "프로젝트 매니저", "법률가"]},
    "ESFJ": {"emoji": "🤝", "desc": "사교적인 외교관", "jobs": ["인사과 직원", "호텔리어", "초등교사", "홍보 담당자"]},
    "ENFJ": {"emoji": "🎤", "desc": "정의로운 사회운동가", "jobs": ["코치", "정치인", "커뮤니케이션 전문가", "교사"]},
    "ENTJ": {"emoji": "🏢", "desc": "대담한 통솔자", "jobs": ["CEO", "경제 분석가", "경영 컨설턴트", "판사"]},
}

# 🛠️ 사이드바 레이아웃
with st.sidebar:
    st.header("⚙️ 설정 및 입력")
    name = st.text_input("당신의 성함은?", placeholder="이름을 입력하세요 😊")
    selected_mbti = st.selectbox("자신의 MBTI를 선택하세요 👇", list(mbti_data.keys()))
    
    st.info("💡 MBTI는 진로 탐색의 참고용으로 활용하세요!")

# 🎬 메인 콘텐츠
if name:
    st.balloons() # 화려한 효과 추가!
    st.subheader(f"✨ {name}님께 꼭 맞는 보석 같은 직업들을 찾아봤어요!")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"### {mbti_data[selected_mbti]['emoji']} {selected_mbti}")
        st.write(f"**{mbti_data[selected_mbti]['desc']}**")
        
    with col2:
        st.success(f"📌 {selected_mbti} 추천 직업군")
        for job in mbti_data[selected_mbti]['jobs']:
            st.write(f"✅ {job}")

    # 상세 설명 섹션 (Expander 사용으로 깔끔하게)
    with st.expander("📚 진로 교육 가이드 보기"):
        st.write(f"""
        {selected_mbti} 유형인 {name}님은 평소 논리적이고 체계적인 업무를 선호하실 가능성이 높아요.
        위 추천 직업들은 {name}님의 성향을 가장 잘 발휘할 수 있는 분야들이지만, 
        가장 중요한 것은 본인의 '관심'과 '열정'이라는 점을 잊지 마세요! 🌟
        """)

    # 📊 관련성 차트 (가상 데이터)
    st.write("---")
    st.markdown("### 📈 유형별 직무 적합도")
    chart_data = pd.DataFrame({
        "역량": ["논리력", "창의성", "공감능력", "실행력"],
        "점수": [85, 92, 78, 88] # 실제 구현 시 MBTI별로 수치 조정 가능
    })
    st.bar_chart(chart_data, x="역량", y="점수", color="#FF4B4B")

else:
    st.warning("👈 왼쪽 사이드바에서 이름을 먼저 입력해 주세요!")

# 🦶 푸터
st.markdown("---")
st.caption("© 2026 교육혁신센터 진로 교육 지원 플랫폼 | 모든 꿈을 응원합니다! 🕯️")
