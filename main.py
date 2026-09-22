import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 2 - 분포와 관계", layout="wide")

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 및 전처리 함수 (캐싱을 통해 속도 향상)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 장르 전처리: 여러 장르가 '|'로 묶여있을 경우 첫 번째 장르만 추출
    df['genre'] = df['genre'].apply(lambda x: str(x).split('|')[0] if pd.notnull(x) else x)
    return df

df = load_data()

# =========================================
# 1. 장르별 영화 편수 (도넛 그래프)
# =========================================
st.subheader("1. 장르별 영화 편수")

# 장르별 빈도수 계산
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '편수']

# Plotly 도넛 그래프 생성
fig1 = px.pie(
    genre_counts, 
    names='장르', 
    values='편수', 
    hole=0.4, # 이 값을 주면 가운데가 뚫린 도넛 그래프가 됩니다.
)

# 마우스를 올렸을 때(hover) 편수와 비율이 깔끔하게 보이도록 텍스트 포맷 설정
fig1.update_traces(
    textinfo='percent+label', 
    hovertemplate='<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>'
)

# 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 그래프 해석 및 구역 나누기
st.markdown("**이 그래프로 알 수 있는 것:** (이곳에 장르별 분포에 대한 해석을 한 문장으로 적어주세요.)")
st.divider()

# 이후 추가할 그래프들을 위해 아래에 템플릿을 만들어 둘 수 있습니다.
# st.subheader("2. 다음 그래프 제목")
# ... (그래프 코드)
# st.markdown("**이 그래프로 알 수 있는 것:** (해석)")
# st.divider()
