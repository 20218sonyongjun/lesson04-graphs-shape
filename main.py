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
    hole=0.4,
)

fig1.update_traces(
    textinfo='percent+label', 
    hovertemplate='<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>'
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** 드라마와 액션 장르가 전체 영화 편수의 과반수 이상을 차지하고 있습니다.")
st.divider()

# =========================================
# 2. 장르 및 영화별 총 관객수 (트리맵)
# =========================================
st.subheader("2. 장르 및 영화별 총 관객수")

fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), 'genre', 'movieNm'],
    values='total_audi',
    color='genre',
)

fig2.update_traces(
    hovertemplate='<b>%{label}</b><br>총 관객수: %{value:,}명<extra></extra>'
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:** 영화 편수가 많은 장르일수록 총 관객수 지분도 대체로 크게 나타납니다.")
st.divider()

# =========================================
# 3. 총 관객수 분포 (히스토그램)
# =========================================
st.subheader("3. 총 관객수 분포")

# 히스토그램 생성
fig3 = px.histogram(
    df, 
    x='total_audi',
    nbins=30,
    labels={'total_audi': '총 관객수'}
)

fig3.update_traces(
    hovertemplate='관객수 구간: %{x}명<br>영화 수: %{y}편<extra></extra>'
)

fig3.update_layout(
    xaxis_title="총 관객수 (명)",
    yaxis_title="영화 수 (편)",
    bargap=0.1
)

st.plotly_chart(fig3, use_container_width=True)

# 최고 관객수 영화 정보 데이터프레임에서 동적 추출
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

# 그래프 아래 해석 문구 출력
st.markdown(
    f"**이 그래프로 알 수 있는 것:** 대다수의 영화가 **100만~200만 명 이하의 낮은 관객수 구간**에 모여 있으며, "
    f"가장 많은 관객을 동원한 영화는 **'{top_movie_name}'**({top_movie_audi:,}명)입니다."
)
st.divider()
