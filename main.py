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

top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

st.markdown(
    f"**이 그래프로 알 수 있는 것:** 대다수의 영화가 **100만~200만 명 이하의 낮은 관객수 구간**에 모여 있으며, "
    f"가장 많은 관객을 동원한 영화는 **'{top_movie_name}'**({top_movie_audi:,}명)입니다."
)
st.divider()

# =========================================
# 4. 개봉일 스크린수와 총 관객수의 관계 (산점도)
# =========================================
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계")

fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    labels={
        'first_scrn': '개봉일 스크린수',
        'total_audi': '총 관객수',
        'genre': '장르'
    }
)

fig4.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>개봉일 스크린수: %{x:,}개<br>총 관객수: %{y:,}명<extra></extra>'
)

fig4.update_layout(
    xaxis_title="개봉일 스크린수 (개)",
    yaxis_title="총 관객수 (명)"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown(
    "**이 그래프로 알 수 있는 것:** 대체로 **개봉일 스크린수가 많을수록 총 관객수도 증가하는 양의 상관관계**를 보이지만, "
    "스크린수가 적어도 높은 관객수를 기록하거나 스크린수가 많아도 관객수가 적은 흥행 예외 사례도 관찰됩니다."
)
st.divider()
```eof

네 번째 그래프인 **개봉일 스크린수와 총 관객수의 산점도**가 정상적으로 추가되었습니다. 

* 점에 마우스를 올리면 **영화명**과 함께 스크린수, 총 관객수가 천 단위 쉼표 포맷으로 나타납니다.
* **장르별로 색상**이 다르게 구분되며 범례(Legend)를 통해 특정 장르만 필터링하여 확인하실 수도 있습니다.

추가로 수정하고 싶은 부분이나 새로운 그래프 요청이 있으시면 말씀해 주세요!
