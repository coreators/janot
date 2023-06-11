import streamlit as st
import pandas as pd
import requests
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode , ColumnsAutoSizeMode

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
# @st.cache_data()
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
    monthly_df['총 매수액'] = monthly_df['총 매수액'].apply(lambda x: str(int(x)) + '원')
    monthly_df['총 매도액'] = monthly_df['총 매도액'].apply(lambda x: str(int(x)) + '원')
    monthly_df['매매 비용'] = monthly_df['매매 비용'].apply(lambda x: str(int(x)) + '원')
    monthly_df['실현 손익'] = monthly_df['실현 손익'].apply(lambda x: str(int(x)) + '원')

    # 출력이 이상하게 되는데 string 그대로 출력을 위함.
    monthly_df['월'] = monthly_df['월'].astype(str)

    monthly_df.set_index('월', inplace=True)
    print(monthly_df)
    if response.status_code == 200:
        return monthly_df
    else:
        return pd.DataFrame()

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
        "profit_loss": "실현 손익"})
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

    monthly_fee_df = df.groupby('월')['매매 비용'].sum().reset_index()
    monthly_fee_df = monthly_fee_df.rename(columns={"수수료": "총 매매 비용"})

    # 월이라는 컬럼이 중복인데 이를 하나로 합쳤음
    monthly_df = pd.merge(monthly_buy_df, monthly_sell_df, on='월', how='outer')
    monthly_df = pd.merge(monthly_df, monthly_fee_df, on='월', how='outer')
    monthly_df = pd.merge(monthly_df, monthly_profit_df, on='월', how='outer')

    # 값이 nan인걸 0으로 대체
    monthly_df = monthly_df.fillna(0)

    # 단위 붙이기 ($)
    monthly_df['총 매수액'] = monthly_df['총 매수액'].apply(lambda x: str(round(x,2)) + '$')
    monthly_df['총 매도액'] = monthly_df['총 매도액'].apply(lambda x: str(round(x,2)) + '$')
    monthly_df['매매 비용'] = monthly_df['매매 비용'].apply(lambda x: str(round(x,2)) + '$')
    monthly_df['실현 손익'] = monthly_df['실현 손익'].apply(lambda x: str(round(x,2)) + '$')



    # 값이 nan인걸 0으로 대체
    monthly_df = monthly_df.fillna(0)

    # 출력이 이상하게 되는데 string 그대로 출력을 위함.
    monthly_df['월'] = monthly_df['월'].astype(str)

    monthly_df.set_index('월', inplace=True)
    print(monthly_df)
    if response.status_code == 200:
        return monthly_df
    else:
        return pd.DataFrame()

def create_table(df):
    st.dataframe(df, use_container_width=True)


with total:
    st.markdown("## Total")
    col1, col2, col3 = st.columns(3)
    # 비중을 이런걸로 표시해도 UI가 괜찮을듯
    col1.metric("총 실현 손익", "70 °F", "1.2 °F")
    col2.metric("한국 실현 손익", "9 mph", "-8%")
    col3.metric("미국 실현 손익", "86%", "4%")

with korea:
    st.markdown("## Korea")
    df = fetch_data()
    create_table(df)

with usa:
    st.markdown("## USA")
    df = fetch_data_usa()
    create_table(df)


with dollar:
    st.markdown("## Dollar")

