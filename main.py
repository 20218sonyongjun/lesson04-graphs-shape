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
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
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
# 구역 2: 개봉일 스크린수와 총 관객수의 관계
# ==========================================
st.subheader("2. 개봉일 스크린수와 총 관객수의 관계")

fig2 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    size="days_in_top10",
    title="개봉일 스크린수 대비 총 관객수 분포 (점 크기: 10위권 유지 일수)",
    labels={
        "first_scrn": "개봉일 스크린수 (개)",
        "total_audi": "총 관객수 (명)",
        "genre": "장르",
        "days_in_top10": "Top 10 유지 일수",
    },
    hover_data={
        "days_in_top10": True,
        "first_scrn": ":,",
        "total_audi": ":,",
    },
)

fig2.update_layout(margin=dict(t=50, b=20, l=20, r=20))

st.plotly_chart(fig2, use_container_width=True)

# 인사이트 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:** 초기 스크린 확보 수가 많을수록 대체로 높은 총 관객수를 기록하지만, Top 10 진입 유지 일수가 긴 영화일수록 최종 흥행 규모가 더욱 커집니다."
)

st.divider()

# ==========================================
# 구역 3: 총 관객수 분포
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

# 인사이트 구역
st.info(
    "💡 **이 그래프로 알 수 있는 것:** 대부분의 영화가 특정 관객수 이하 구간에 밀집해 있으며, 소수의 대형 흥행작만 오른쪽으로 멀리 떨어져 존재하는 오른쪽으로 긴 꼬리를 가진 분포를 보입니다."
)

st.divider()

# 데이터 원본 확인용 확장 영역
with st.expander("🔍 원본 데이터셋 보기"):
    st.dataframe(df, use_container_width=True)
