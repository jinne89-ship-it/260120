import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="홍길동의 포트폴리오",
    page_icon="👋",
    layout="wide"
)

# 2. 프로필 이미지 불러오기 (URL 사용 예시)
# 실제 사용 시에는 본인의 로컬 이미지 경로(예: "my_photo.jpg")를 사용하거나
# 아래처럼 웹상의 이미지 주소를 사용할 수 있습니다.
def load_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# 예시용 이미지 (실제 앱에서는 본인 사진 경로로 변경하세요: st.image("profile.jpg"))
image_url = "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80"

# --- 사이드바 (연락처 및 간략 정보) ---
with st.sidebar:
    try:
        # 로컬 파일 사용 시: image = Image.open("profile.jpg")
        st.image(image_url, caption="홍길동", use_column_width=True)
    except:
        st.warning("이미지를 불러올 수 없습니다.")
    
    st.markdown("### Contact Info")
    st.info("📧 email@example.com")
    st.info("📞 010-1234-5678")
    st.success("🔗 [GitHub](https://github.com)")
    st.success("🔗 [LinkedIn](https://linkedin.com)")
    
    st.markdown("---")
    st.write("📍 Seoul, South Korea")

# --- 메인 화면 구성 ---

# 헤더 섹션 (인사말)
col1, col2 = st.columns([2, 1]) # 텍스트 영역을 좀 더 넓게 배분

with col1:
    st.title("안녕하세요! 👋")
    st.header("데이터를 사랑하는 개발자, 홍길동입니다.")
    st.write("""
    저는 **Python**과 **데이터 분석**에 열정을 가지고 있는 개발자입니다.
    복잡한 문제를 기술로 해결하는 것을 좋아하며, 항상 새로운 것을 배우기 위해 노력합니다.
    """)

# 탭을 사용하여 내용 분리 (깔끔한 UI)
tab1, tab2, tab3 = st.tabs(["📚 자기소개", "🛠 기술 스택", "🚀 프로젝트"])

with tab1:
    st.subheader("About Me")
    st.write("""
    - **성격:** 긍정적이고 협업을 중시합니다.
    - **취미:** 코딩, 등산, 기술 블로그 운영
    - **목표:** 사람들에게 도움이 되는 서비스를 만드는 풀스택 데이터 사이언티스트
    """)
    st.markdown("### 🎓 학력")
    st.write("- OO대학교 컴퓨터공학과 졸업 (2018 - 2022)")

with tab2:
    st.subheader("Skills")
    # 컬럼을 나누어 스킬 나열
    skill_col1, skill_col2, skill_col3 = st.columns(3)
    with skill_col1:
        st.markdown("**Languages**")
        st.write("- Python, Java, SQL")
    with skill_col2:
        st.markdown("**Frameworks**")
        st.write("- Streamlit, Django, Flask")
    with skill_col3:
        st.markdown("**Tools**")
        st.write("- Git, Docker, AWS")

with tab3:
    st.subheader("My Projects")
    
    # 프로젝트 1
    st.markdown("#### 1. 영화 추천 시스템 웹 앱")
    st.write("사용자의 취향을 분석하여 영화를 추천해주는 머신러닝 프로젝트입니다.")
    st.caption("사용 기술: Python, Scikit-learn, Streamlit")
    
    st.divider() # 구분선
    
    # 프로젝트 2
    st.markdown("#### 2. 주식 가격 예측 대시보드")
    st.write("LSTM 모델을 활용하여 주가 변동을 예측하고 시각화했습니다.")
    st.caption("사용 기술: TensorFlow, Pandas, Plotly")

# --- 푸터 ---
st.write("---")
st.write("© 2024 Hong Gil Dong. All rights reserved.")
