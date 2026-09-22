import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_layout="wide",
)


# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
  url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
  df = pd.read_csv(url)

  # 장르 열 전처리: 세로막대(|)가 있는 경우 첫 번째 장르만 추출
  if "genre" in df.columns:
    df["genre"] = (
        df["genre"].astype(str).apply(lambda x: x.split("|")[0].strip())
    )

  return df


try:
  df = load_data()
except Exception as e:
  st.error(f"데이터를 불러오는 데 실패했습니다: {e}")
  st.stop()

# 앱 제목 및 소개
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    "KOBIS 박스오피스 상위 10위권에 든 영화 216편의 데이터를 바탕으로 영화의"
    " 장르별 분포와 흥행 지표 간의 관계를 시각화한 도감입니다."
)
st.markdown("---")

# ==========================================
# [그래프 1] 장르별 영화 편수 도넛 그래프
# ==========================================
st.subheader("1. 장르별 영화 편수 분포")

genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "count"]

fig_genre = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.4,  # 도넛 차트 형태
    title="장르별 영화 편수 비율",
)
fig_genre.update_traces(textposition="inside", textinfo="percent+label")
st.plotly_chart(fig_genre, use_container_width=True)

# 그래프 설명 구역
st.markdown("> **💡 이 그래프로 알 수 있는 것**")
st.info(
    "전체 박스오피스 상위 영화 중 어떤 장르가 가장 많이 제작되고 흥행"
    " 상위권에 진입했는지 장르별 편수와 비중을 한눈에 파악할 수 있습니다."
)

st.markdown("---")

# ==========================================
# [그래프 2] 개봉 첫 주 관객수와 총 관객수의 관계 산점도
# ==========================================
st.subheader("2. 개봉 첫 주 관객수와 총 관객수의 관계")

if "first_week_audi" in df.columns and "total_audi" in df.columns:
  fig_rel = px.scatter(
      df,
      x="first_week_audi",
      y="total_audi",
      hover_data=["movieNm", "genre"],
      labels={
          "first_week_audi": "개봉 첫 주 관객수",
          "total_audi": "총 관객수",
      },
      title="개봉 첫 주 성적이 총 관객수에 미치는 영향",
  )
  st.plotly_chart(fig_rel, use_container_width=True)

  # 그래프 설명 구역
  st.markdown("> **💡 이 그래프로 알 수 있는 것**")
  st.info(
      "영화의 초기 흥행 성적(개봉 첫 주 관객수)이 최종 흥행 규모(총"
      " 관객수)와 어느 정도의 비례 관계를 가지는지 확인할 수 있습니다."
  )
else:
  st.warning("필요한 데이터 열이 존재하지 않습니다.")
