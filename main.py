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

genre_df = df["genre"].value_counts().reset_index()
genre_df.columns = ["genre", "count"]

fig1 = px.pie(
    genre_df,
    names="genre",
    values="count",
    hole=0.4,
    title="장르별 영화 편수 비중",
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

fig1.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>장르: %{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>",
)

fig1.update_layout(margin=dict(t=50, b=20, l=20, r=20))

st.plotly_chart(fig1, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 특정 상위 장르(드라마, 액션 등)가 전체 개봉작의 과반 이상을 차지하며 시장을 주도하고 있음을 확인할 수 있습니다."
)

st.divider()

# ==========================================
# 구역 2: 장르 및 영화별 총 관객수 (트리맵 그래프)
# ==========================================
st.subheader("2. 장르 및 영화별 총 관객수 분포")

fig2 = px.treemap(
    df,
    path=[px.Constant("전체 영화"), "genre", "movieNm"],
    values="total_audi",
    color="genre",
    title="장르 및 영화별 총 관객수 트리맵 (칸 크기: 총 관객수)",
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,.0f}명<extra></extra>"
)

fig2.update_layout(margin=dict(t=50, b=20, l=20, r=20))

st.plotly_chart(fig2, use_container_width=True)

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

# 최다 관객 동원작 및 주요 구간 계산
top_movie = df.loc[df["total_audi"].idxmax()]
top_movie_name = top_movie["movieNm"]
top_movie_audi = top_movie["total_audi"]

under_2m_cnt = len(df[df["total_audi"] <= 2000000])
under_2m_pct = (under_2m_cnt / len(df)) * 100

st.info(
    f"💡 **이 그래프로 알 수 있는 것:**\n\n"
    f"- **밀집 구간:** 전체 영화 216편 중 대부분인 **{under_2m_pct:.1f}%({under_2m_cnt}편)**가 **200만 명 이하 구간**에 밀집되어 있습니다.\n"
    f"- **최다 관객 동원작:** 데이터셋에서 가장 관객 수가 많은 영화는 **'{top_movie_name}'** (약 **{top_movie_audi:,.0f}명**)입니다."
)

st.divider()

# ==========================================
# 구역 4: 개봉일 스크린수와 총 관객수 (산점도)
# ==========================================
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수 대비 총 관객수 산점도",
    labels={
        "first_scrn": "개봉일 스크린수 (개)",
        "total_audi": "총 관객수 (명)",
        "genre": "장르",
    },
    hover_data={
        "first_scrn": ":,",
        "total_audi": ":,",
        "genre": True,
    },
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

fig4.update_layout(margin=dict(t=50, b=20, l=20, r=20))

st.plotly_chart(fig4, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수를 많이 확보한 영화일수록 대체로 더 많은 총 관객수를 기록하는 양의 상관관계를 보이지만, 스크린수가 적음에도 높은 관객수를 기록한 입소문 흥행작도 존재함을 알 수 있습니다."
)

st.divider()

# ==========================================
# 구역 5: 주요 장르별 총 관객수 분포 (박스플롯)
# ==========================================
st.subheader("5. 주요 장르별 총 관객수 분포")

# 영화 수가 10편 이상인 장르 필터링
genre_counts = df["genre"].value_counts()
top_genres = genre_counts[genre_counts >= 10].index
box_df = df[df["genre"].isin(top_genres)]

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    points="outliers",
    title="영화 10편 이상 주요 장르별 총 관객수 상자 그림 (점: 이상치 영화)",
    labels={
        "genre": "장르",
        "total_audi": "총 관객수 (명)",
    },
    hover_data={
        "total_audi": ":,",
        "genre": False,
    },
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

fig5.update_layout(margin=dict(t=50, b=20, l=20, r=20), showlegend=False)

st.plotly_chart(fig5, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 장르별 중앙값(중위수)을 통해 평균적인 흥행 규모를 비교할 수 있으며, 상자 밖으로 높게 솟은 이상치(outlier) 점들에 마우스를 올리면 해당 장르의 기록적인 텐트폴(대형 흥행) 영화명을 바로 확인할 수 있습니다."
)

st.divider()

# ==========================================
# 구역 6: 개봉일 스크린수, 첫 주 관객수, 총 관객수 (버블 차트)
# ==========================================
st.subheader("6. 개봉일 스크린수, 첫 주 관객수, 총 관객수의 관계")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수 대비 총 관객수 버블 차트 (버블 크기: 개봉 첫 주 관객수)",
    labels={
        "first_scrn": "개봉일 스크린수 (개)",
        "total_audi": "총 관객수 (명)",
        "first_week_audi": "첫 주 관객수 (명)",
        "genre": "장르",
    },
    hover_data={
        "first_scrn": ":,",
        "total_audi": ":,",
        "first_week_audi": ":,",
        "genre": True,
    },
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

fig6.update_layout(margin=dict(t=50, b=20, l=20, r=20))

st.plotly_chart(fig6, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수가 많고 개봉 첫 주 관객수(버블 크기)가 클수록 최종 총 관객수도 높아지는 경향을 보이며, 버블의 크기를 통해 초반 흥행 기세가 최종 흥행 성적에 미친 영향력을 입체적으로 확인할 수 있습니다."
)

st.divider()

# ==========================================
# 구역 7: 제작 국가 및 장르별 영화 편수 (선버스트 차트)
# ==========================================
st.subheader("7. 제작 국가 및 장르별 영화 편수 분포")

fig7 = px.sunburst(
    df,
    path=["nation", "genre"],
    title="제작 국가 및 장르별 영화 편수 선버스트 차트 (칸 크기: 영화 편수)",
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<extra></extra>"
)

fig7.update_layout(margin=dict(t=50, b=20, l=20, r=20))

st.plotly_chart(fig7, use_container_width=True)

st.info(
    "💡 **이 그래프로 알 수 있는 것:** 주요 제작 국가별로 어떤 장르의 영화가 주로 제작/개봉되는지 국가별 장르 다양성과 편수 비중을 계층적으로 파악할 수 있습니다."
)

st.divider()

# ==========================================
# 구역 8: 질문 해결 구역 (추세선 포함 산점도)
# ==========================================
st.subheader("8. 개봉일 스크린수가 많으면 총 관객도 많을까?")

# 그래프 선택 이유 설명 (한 줄)
st.markdown(
    "📌 **그래프 선택 이유:** 두 연속형 수치 변수(스크린수와 관객수) 간의 상관관계와 전체적인 비례 경향성을 추세선과 함께 직관적으로 확인하기에 **회귀 추세선 산점도**가 가장 적합합니다."
)

# 스크린수와 총 관객수의 상관계수 계산
corr_val = df["first_scrn"].corr(df["total_audi"])

# 추세선(OLS)을 포함한 산점도 생성
fig8 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    trendline="ols",
    title="개봉일 스크린수가 많으면 총 관객도 많을까?",
    labels={
        "first_scrn": "개봉일 스크린수 (개)",
        "total_audi": "총 관객수 (명)",
        "genre": "장르",
    },
    hover_data={
        "first_scrn": ":,",
        "total_audi": ":,",
        "genre": True,
    },
    color_discrete_sequence=px.colors.qualitative.Pastel,
)

fig8.update_layout(margin=dict(t=50, b=20, l=20, r=20))

st.plotly_chart(fig8, use_container_width=True)

st.info(
    f"💡 **이 그래프로 알 수 있는 것:** 개봉일 스크린수와 총 관객수는 상관계수 약 **{corr_val:.2f}**로 우상향하는 뚜렷한 **양의 상관관계**를 보입니다. 즉, 개봉일 스크린수가 많을수록 대체로 총 관객수도 많아진다는 경향성을 확인할 수 있습니다."
)

st.divider()

# 데이터 원본 확인용 확장 영역
with st.expander("🔍 원본 데이터셋 보기"):
    st.dataframe(df, use_container_width=True)
