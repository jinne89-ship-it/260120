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
    "INTJ": {"emoji": "🧠", "desc":
