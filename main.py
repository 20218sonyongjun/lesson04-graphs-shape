import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption("KOBIS 박스오피스 상위 영화 216편 데이터 분석")


# 데이터 불러오기 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/happykth/data/main/kobis_movies.csv"
    df = pd.read_csv(url)

    # 장르 열: 세로막대 기호(|) 기준으로 첫 번째 장르만 추출
    df["genre"] = df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())

    return df


df = load_data()

# ==========================================
# 구역 1: 장르별 영화 편수 (도넛 그래프)
# ==========================================
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_df = df["genre"].value_counts().reset_index()
genre_df.columns = ["genre", "count"]

# 플롯리 도넛 그래프 작성
fig1 = px.pie(
    genre_df,
    names="genre",
    values="count",
    hole=0.4,
    title="장르별 영화 편수 비중",
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

# 마우스 오버 시 편수와 비율 표시 설정
fig1.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>장르: %{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>",
)

fig1.update_layout(margin=dict(t=50, b=20, l=20, r=20))

st.plotly_chart(fig1, use_container_width=True)

# 인사이트 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:** 특정 상위 장르(드라마, 액션 등)가 전체 개봉작의 과반 이상을 차지하며 시장을 주도하고 있음을 확인할 수 있습니다."
)

st.divider()

# ==========================================
# 구역 2: 장르 및 영화별 총 관객수 (트리맵 그래프)
# ==========================================
st.subheader("2. 장르 및 영화별 총 관객수 분포")

# 트리맵 그래프 작성 (장르 > 영화 구조, 칸 크기: total_audi)
fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), "genre", "movieNm"],
    values="total_audi",
    color="genre",
    title="장르 및 영화별 총 관객수 트리맵 (칸 크기: 총 관객수)",
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

# 마우스 오버 시 영화명(label)과 총 관객수(value) 표시
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,.0f}명<extra></extra>"
)

fig2.update_layout(margin=dict(t=50, b=20, l=20, r=20))

st.plotly_chart(fig2, use_container_width=True)

# 인사이트 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:** 각 장르 내부에서 어떤 영화가 시장 관객수의 대부분을 차지하고 있는지 한눈에 비중을 비교할 수 있습니다."
)

st.divider()

# ==========================================
# 구역 3: 총 관객수 분포 (히스토그램)
# ==========================================
st.subheader("3. 총 관객수 구간별 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=30,
    title="총 관객수 구간별 영화 편수 히스토그램",
    labels={"total_audi": "총 관객수 (명)", "count": "영화 수"},
    color_discrete_sequence=["#636EFA"],
)

fig3.update_layout(
    yaxis_title="영화 수 (편)", margin=dict(t=50, b=20, l=20, r=20)
)

st.plotly_chart(fig3, use_container_width=True)

# 가장 관객이 많은 영화 정보 추출 및 주요 구간 분석
top_movie = df.loc[df["total_audi"].idxmax()]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

# 관객수 200만 명 이하 영화의 비중 계산
under_2m_cnt = len(df[df["total_audi"] <= 2000000])
under_2m_pct = (under_2m_cnt / len(df)) * 100

# 인사이트 구역 (요청사항 반영 문구)
st.info(
    f"💡 **이 그래프로 알 수 있는 것:**\n\n"
    f"- **밀집 구간:** 전체 영화 216편 중 대부분인 **{under_2m_pct:.1f}%({under_2m_cnt}편)**가 **200만 명 이하 구간**에 밀집되어 있습니다.\n"
    f"- **최다 관객 동원작:** 데이터셋에서 가장 관객 수가 많은 영화는 **'{top_movie_name}'** (약 **{top_movie_audi:,.0f}명**)입니다."
)

st.divider()

# 데이터 원본 확인용 확장 영역
with st.expander("🔍 원본 데이터셋 보기"):
    st.dataframe(df, use_container_width=True)
