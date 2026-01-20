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
            {"name": "점핑잭 (팔벌려뛰기)", "set
