import streamlit as st
import feedparser
from urllib.parse import quote

# 1. 페이지 설정
st.set_page_config(page_title="실시간 뉴스 돋보기", page_icon="🔍", layout="wide")

# 2. 스타일링
st.markdown("""
    <style>
    .news-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4285F4;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .source-tag {
        color: #34A853;
        font-weight: bold;
        font-size: 0.85em;
    }
    .date-tag {
        color: #888;
        font-size: 0.8em;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 뉴스 가져오기 함수 (구글 RSS 활용)
def get_google_news(query):
    # 한글 검색어 인코딩 및 RSS URL 생성 (hl=ko: 한국어, gl=KR: 한국 지역)
    encoded_query = quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(rss_url)
    return feed.entries

# 4. 사이드바 및 검색창
st.sidebar.title("🚀 News Search")
search_query = st.sidebar.text_input("검색어를 입력하세요", value="인공지능 교육")
news_count = st.sidebar.slider("가져올 기사 개수", 5, 30, 10)

# 5. 메인 화면 구성
st.title(f"🔍 '{search_query}' 최신 뉴스 리포트")
st.write(f"구글 뉴스에서 검색된 최신 기사 {news_count}개를 보여드립니다.")
st.divider()

if search_query:
    with st.spinner('뉴스를 불러오는 중입니다...'):
        articles = get_google_news(search_query)
        
        if not articles:
            st.error("검색 결과가 없습니다. 다른 검색어를 입력해 보세요.")
        else:
            # 지정된 개수만큼 기사 출력
            for entry in articles[:news_count]:
                with st.container():
                    st.markdown(f"""
                        <div class="news-card">
                            <span class="source-tag">📰 {entry.source.get('title', '뉴스')}</span>
                            <span class="date-tag"> | 📅 {entry.published}</span>
                            <h3 style="margin-top: 10px;"><a href="{entry.link}" target="_blank" style="text-decoration: none; color: #1A73E8;">{entry.title}</a></h3>
                        </div>
                    """, unsafe_allow_html=True)
    
    # 성공 시 풍선 효과 (선택 사항)
    st.balloons()
else:
    st.info("왼쪽 사이드바에서 검색어를 입력해 주세요!")

# 6. 푸터
st.markdown("---")
st.caption("© 2026 실시간 뉴스 분석기 | Powered by Google News RSS")
