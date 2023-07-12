import streamlit as st
import pandas as pd
import requests
import datetime
import FinanceDataReader as fdr

usernameSession = 'username'
userSession = st.session_state[usernameSession]

kor_list = pd.read_csv("resources/kor_ticker_list.csv")
usa_list = pd.read_csv("resources/usa_ticker_list.csv")

st.markdown("# Monthly Trade 📈")
st.sidebar.markdown("# Monthly Trade 📈")

st.sidebar.success("Monthly Trade 📈️")
st.sidebar.info("월별 매매일지 정리 페이지입니다.")
st.sidebar.title("Monthly Trade 📈️")
st.sidebar.markdown(
    """
    다음은 본 페이지의 요구사항입니다.    

    - 월별 매수 횟수
    - 월별 매수 금액
    - 월별 매도 횟수
    - 월별 매도 금액
    - 월별 총 실현 손익
    - 환율 반영한 실현손익
    """
)

total, korea, usa, dollar= st.tabs(['Total', 'Korea', 'USA',"Dollar"])


# 유저의 데이터를 다 긁어와서 읽어서 월별로 표시해주기
# 매수 매도는 계산하는 방법이 다름.
@st.cache_data()
def fetch_data():
    response = requests.get('http://localhost:9000/api/v1/journal/kor/read',
                            json={'email': userSession})
    print("fecth data : ", response , "user name : ",userSession)
    df = pd.DataFrame(response.json())
    df = df.rename(columns={
        "ticker": "종목명",
        "price": "매수/매도 가격",
        "amount": "수량",
        "date": "매수/매도 일자",
        "fee": "수수료",
        "tax": "세금",
        "sector": "섹터",
        "is_buy": "매수/매도",
        "profit_loss": "실현 손익"})
    name_dict = kor_list.set_index('Code').to_dict()['Name']

    # Ticker로 저장된 DB값을 종목명으로 치환해주기
    df['종목명'] = df['종목명'].map(name_dict).fillna(df['종목명'])
    df['매수/매도'] = df['매수/매도'].map({True: "매수", False: "매도"})


    #월별 매도/매수 총 가격 정리
    df['매수/매도 일자'] = pd.to_datetime(df['매수/매도 일자'])  # '매수/매도 일자' 컬럼을 datetime 객체로 변환
    df['월'] = df['매수/매도 일자'].dt.to_period('M')  # 새로운 '월' 컬럼을 만들고 월별로 그룹화

    #매매비용 합치기용
    df['매매 비용'] = df['수수료'] + df['세금']
    df_buy = df[df['매수/매도'] == '매수']
    df_buy['총 매수액'] = df_buy['매수/매도 가격'] * df_buy['수량']
    df_sell = df[df['매수/매도'] == '매도']
    df_sell['총 매도액'] = df_sell['매수/매도 가격'] * df_sell['수량']

    # 예를 들어, 월별로 '매수/매도 가격'의 합계를 구하려면 아래와 같이 할 수 있습니다.
    monthly_buy_df = df_buy.groupby('월')['총 매수액'].sum().reset_index()
    monthly_sell_df = df_sell.groupby('월')['총 매도액'].sum().reset_index()
    monthly_profit_df = df_sell.groupby('월')['실현 손익'].sum().reset_index()
    monthly_profit_df = monthly_profit_df.fillna(0)

    monthly_fee_df = df.groupby('월')['매매 비용'].sum().reset_index()
    monthly_fee_df = monthly_fee_df.rename(columns={"수수료": "총 매매 비용"})

    # 월이라는 컬럼이 중복인데 이를 하나로 합쳤음
    monthly_df = pd.merge(monthly_buy_df, monthly_sell_df, on='월', how='outer')
    monthly_df = pd.merge(monthly_df, monthly_fee_df, on='월', how='outer')
    monthly_df = pd.merge(monthly_df, monthly_profit_df, on='월', how='outer')


    # 값이 nan인걸 0으로 대체
    monthly_df = monthly_df.fillna(0)

    # 단위 붙이기 (원)
    # monthly_df['총 매수액'] = monthly_df['총 매수액'].apply(lambda x: str(int(x)) + '원')
    # monthly_df['총 매도액'] = monthly_df['총 매도액'].apply(lambda x: str(int(x)) + '원')
    # monthly_df['매매 비용'] = monthly_df['매매 비용'].apply(lambda x: str(int(x)) + '원')
    # monthly_df['실현 손익'] = monthly_df['실현 손익'].apply(lambda x: str(int(x)) + '원')

    # 출력이 이상하게 되는데 string 그대로 출력을 위함.
    monthly_df['월'] = monthly_df['월'].astype(str)

    monthly_df.set_index('월', inplace=True)
    # print(monthly_df)
    if response.status_code == 200:
        return monthly_df
    else:
        return pd.DataFrame()

@st.cache_data()
def fetch_data_usa():
    response = requests.get('http://localhost:9000/api/v1/journal/usa/read',
                            json={'email': userSession})
    print("fecth data : ", response , "user name : ",userSession)
    df = pd.DataFrame(response.json())
    df = df.rename(columns={
        "ticker": "종목명",
        "price": "매수/매도 가격",
        "amount": "수량",
        "date": "매수/매도 일자",
        "fee": "수수료",
        "tax": "세금",
        "sector": "섹터",
        "is_buy": "매수/매도",
        "profit_loss": "실현 손익",
        "profit_loss_with_exchange": "환전 포함 손익"})
    name_dict = usa_list.set_index('Code').to_dict()['Name']

    # Ticker로 저장된 DB값을 종목명으로 치환해주기
    df['종목명'] = df['종목명'].map(name_dict).fillna(df['종목명'])
    df['매수/매도'] = df['매수/매도'].map({True: "매수", False: "매도"})


    #월별 매도/매수 총 가격 정리
    df['매수/매도 일자'] = pd.to_datetime(df['매수/매도 일자'])  # '매수/매도 일자' 컬럼을 datetime 객체로 변환
    df['월'] = df['매수/매도 일자'].dt.to_period('M')  # 새로운 '월' 컬럼을 만들고 월별로 그룹화

    #매매비용 합치기용
    df['매매 비용'] = df['수수료'] + df['세금']
    df_buy = df[df['매수/매도'] == '매수']
    df_buy['총 매수액'] = df_buy['매수/매도 가격'] * df_buy['수량']
    df_sell = df[df['매수/매도'] == '매도']
    df_sell['총 매도액'] = df_sell['매수/매도 가격'] * df_sell['수량']

    # 예를 들어, 월별로 '매수/매도 가격'의 합계를 구하려면 아래와 같이 할 수 있습니다.
    monthly_buy_df = df_buy.groupby('월')['총 매수액'].sum().reset_index()
    monthly_sell_df = df_sell.groupby('월')['총 매도액'].sum().reset_index()
    monthly_profit_df = df_sell.groupby('월')['실현 손익'].sum().reset_index()
    monthly_profit_krw_df = df_sell.groupby('월')['환전 포함 손익'].sum().reset_index()

    monthly_fee_df = df.groupby('월')['매매 비용'].sum().reset_index()
    monthly_fee_df = monthly_fee_df.rename(columns={"수수료": "총 매매 비용"})

    # 월이라는 컬럼이 중복인데 이를 하나로 합쳤음
    monthly_df = pd.merge(monthly_buy_df, monthly_sell_df, on='월', how='outer')
    monthly_df = pd.merge(monthly_df, monthly_fee_df, on='월', how='outer')
    monthly_df = pd.merge(monthly_df, monthly_profit_df, on='월', how='outer')
    monthly_df = pd.merge(monthly_df, monthly_profit_krw_df, on='월', how='outer')

    # 값이 nan인걸 0으로 대체
    monthly_df = monthly_df.fillna(0)

    # 단위 붙이기 ($)
    # monthly_df['총 매수액'] = monthly_df['총 매수액'].apply(lambda x: str(round(x,2)) + '$')
    # monthly_df['총 매도액'] = monthly_df['총 매도액'].apply(lambda x: str(round(x,2)) + '$')
    # monthly_df['매매 비용'] = monthly_df['매매 비용'].apply(lambda x: str(round(x,2)) + '$')
    # monthly_df['실현 손익'] = monthly_df['실현 손익'].apply(lambda x: str(round(x,2)) + '$')
    # monthly_df['환전 포함 손익'] = monthly_df['환전 포함 손익'].apply(lambda x: str(int(x)) + '원')


    # 값이 nan인걸 0으로 대체
    monthly_df = monthly_df.fillna(0)

    # 출력이 이상하게 되는데 string 그대로 출력을 위함.
    monthly_df['월'] = monthly_df['월'].astype(str)

    monthly_df.set_index('월', inplace=True)
    # print(monthly_df)
    if response.status_code == 200:
        return monthly_df
    else:
        return pd.DataFrame()


@st.cache_data()
def fetch_mixed_data():
    df_kor_copy = df_kor.copy()
    df_usa_copy = df_usa.copy()

    print(df_usa_copy)
    print(exchange_today)
    df_usa_copy['실현 손익'] = df_usa_copy['환전 포함 손익']
    del df_usa_copy['환전 포함 손익']

    df_usa_copy['총 매수액'] = df_usa_copy['총 매수액'] * int(exchange_today)
    df_usa_copy['총 매도액'] = df_usa_copy['총 매도액'] * int(exchange_today)
    df_usa_copy['매매 비용'] = df_usa_copy['매매 비용'] * int(exchange_today)
    print(df_usa_copy)

    merged_df = pd.concat([df_kor_copy, df_usa_copy])

    # 동일한 월에 대해서 값을 합치기
    merged_df = merged_df.groupby('월').agg({
        '총 매수액': 'sum',
        '총 매도액': 'sum',
        '매매 비용': 'sum',
        '실현 손익': 'sum',}).reset_index()
    merged_df.set_index('월', inplace=True)
    print(merged_df)
    return merged_df


def create_table(df):
    st.dataframe(df, use_container_width=True)


# cache kor and usa data
df_kor = fetch_data()
df_usa = fetch_data_usa()

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

# 어제와 오늘의 USD/KRW 환율을 가져옵니다.
df_today = fdr.DataReader('USD/KRW', today)
df_yesterday = fdr.DataReader('USD/KRW', yesterday)

# 오늘의 USD/KRW 환율을 가져옵니다.
try:
    exchange_today = df_today['Close'].iloc[-1] # 여기서 버그생김 밤이라 그런가?
except:
    exchange_today = df_yesterday['Close'].iloc[-1]
exchange_today = round(exchange_today, 2)
change = exchange_today - df_yesterday['Close'].iloc[-1]
change = round(change, 2)
if change >= 0:
    change_diff = str("+") + str(change)+ str("%")
else:
    change_diff = str(change)+ str("%")

with total:
    exchange, col2 = st.columns(2)
    st.markdown("## 원화 기준 월별 매매 일지")
     # 비중을 이런걸로 표시해도 UI가 괜찮을듯
    exchange.metric("원/달러 환율",round(exchange_today,2), change_diff)

# 환전 포함 원화 페이지 구성
    df = fetch_mixed_data()
    create_table(df)

    # print(df)

with korea:
    st.markdown("## Korea")
    create_table(df_kor)

with usa:
    st.markdown("## USA")
    create_table(df_usa)


with dollar:
    st.markdown("## Dollar")

