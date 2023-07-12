import streamlit as st
import requests
import pandas as pd
import FinanceDataReader as fdr
import plotly.express as px
import datetime

usernameSession = 'username'
userSession = st.session_state[usernameSession]

st.set_page_config(
    page_title="My Portfolio",
    page_icon="👋",
)

kor_list = pd.read_csv("resources/kor_ticker_list.csv")
usa_list = pd.read_csv("resources/usa_ticker_list.csv")

# Get user portfolio data from korea data
@st.cache_data()
def fetch_kor_data():
    response = requests.get('http://localhost:9000/api/v1/journal/kor/read',
                            json={'email': userSession})
    print("fetch data : ", response , "user name : ",userSession)

    # 0. email에 해당하는 매수/매도 데이터들 다 긁어오기
    df = pd.DataFrame(response.json())


    # 1. 날짜를 내림차순으로 정렬
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df = df.sort_values(by=['date'], ascending=True)
    print(df)
    df = df.rename(columns={
        "ticker": "티커",
        "price": "매수 가격",
        "amount": "매수 수량",
        "date": "매수/매도 일자",
        "fee": "수수료",
        "tax": "세금",
        "sector": "섹터",
        "is_buy": "매수/매도",
        "sold_amount": "매도 수량",
        "profit_loss": "매도 손익"})
    name_dict = kor_list.set_index('Code').to_dict()['Name']

    # TODO: 매도 자료는 총 손익등에 사용하긴해야함

    # 2. Ticker로 저장된 DB값을 통해서 종목명 컬럼을 생성
    df['종목명'] = df['티커'].map(name_dict).fillna(df['티커'])

    # 3. 매수 자료만 남기기
    df = df[df['매수/매도'] == True]

    # 보유수량, 총 투자액, 보유 투자액
    df['보유 수량'] = df['매수 수량'] - df['매도 수량']
    # 수량이 없으면 제외
    df = df[df['보유 수량'] > 0]
    df['총 투자액'] = df['보유 수량'] * df['매수 가격']

    # 3. 기존 인덱스를 삭제하고 종목명으로 인덱스 설정

    # 4. 출력 필요없는 항목들 제거 (나중에 변경가능)
    del df['transaction_id']
    del df['세금']
    del df['수수료']
    del df['매도 손익']

    # 5. 보유수량, 평균단가, 총투자금, 현재주가, 평가수익률, 평가손익, 평가금액, 비중, 섹터 (매매 시작일)
    df = df.groupby('종목명').agg({
        '티커': 'first',
        '보유 수량': 'sum',
        '매수/매도 일자': 'first',
        '섹터': 'first',
        '총 투자액':'sum',}).reset_index()

    # 포트폴리오 종목들을 기준으로 현재가격을 가져오기
    for idx, row in df.iterrows():
        df.loc[idx, '현재 주가'] = fdr.DataReader(row['티커'])['Close'][-1]
    df['현재 주가'] = df['현재 주가'].astype(int)
    print(df)

    # 보유 투자액 / 보유 수량 == df['평균 단가']
    df['평균 단가'] = df['총 투자액'] / df['보유 수량']
    df['평균 단가'] = df['평균 단가'].astype(int)

    # 평가손익, 평가수익률, 평가금액, 비중 계산
    df['평가 손익'] = (df['현재 주가'] - df['평균 단가']) * df['보유 수량']
    df['평가 수익률'] = (df['현재 주가'] - df['평균 단가']) / df['평균 단가'] * 100
    df['평가 금액'] = df['현재 주가'] * df['보유 수량']
    # 비중 =  해당 종목 평가 금액 / 총 평가금액 *100
    df['비중'] = df['평가 금액'] / df['평가 금액'].sum() * 100

    # 새로운 칼럼 순서 정리
    columns = ['종목명','평균 단가','보유 수량','총 투자액','평가 금액','현재 주가','평가 손익','평가 수익률','매수/매도 일자','섹터','비중']
    df = df[columns]
    df.set_index('종목명',inplace=True)
    # df['평균 단가'] = df['평균 단가'].apply(lambda x: str(x) + '원')
    # df['총 투자액'] = df['총 투자액'].apply(lambda x: str(x) + '원')
    # df['평가 금액'] = df['평가 금액'].apply(lambda x: str(x) + '원')
    # df['현재 주가'] = df['현재 주가'].apply(lambda x: str(x) + '원')
    # df['평가 손익'] = df['평가 손익'].apply(lambda x: str(x) + '원')
    # df['평가 수익률'] = df['평가 수익률'].apply(lambda x: str(round(x,2)) + '%')
    if response.status_code == 200:
        return df
    else:
        return pd.DataFrame()


@st.cache_data()
def fetch_usa_data():
    response = requests.get('http://localhost:9000/api/v1/journal/usa/read',
                            json={'email': userSession})
    print("fetch data : ", response , "user name : ",userSession)

    # 0. email에 해당하는 매수/매도 데이터들 다 긁어오기
    df = pd.DataFrame(response.json())
    print(df)

    # 1. 날짜를 내림차순으로 정렬
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df = df.sort_values(by=['date'], ascending=True)
    print(df)
    df = df.rename(columns={
        "ticker": "티커",
        "price": "매수 가격",
        "amount": "매수 수량",
        "date": "매수/매도 일자",
        "fee": "수수료",
        "tax": "세금",
        "exchange_rate": "환율",
        "sector": "섹터",
        "is_buy": "매수/매도",
        "sold_amount": "매도 수량",
        "profit_loss": "매도 손익",
        "profit_loss_with_exchange": "환전 매도 손익"})
    name_dict = usa_list.set_index('Code').to_dict()['Name']

    # TODO: 매도 자료는 총 손익등에 사용하긴해야함

    # 2. Ticker로 저장된 DB값을 통해서 종목명 컬럼을 생성
    df['종목명'] = df['티커'].map(name_dict).fillna(df['티커'])

    # 3. 매수 자료만 남기기
    df = df[df['매수/매도'] == True]

    # 보유수량, 총 투자액, 보유 투자액
    df['보유 수량'] = df['매수 수량'] - df['매도 수량']
    # 수량이 없으면 제외
    df = df[df['보유 수량'] > 0]
    df['총 투자액'] = df['보유 수량'] * df['매수 가격']

    # 3. 기존 인덱스를 삭제하고 종목명으로 인덱스 설정

    # 4. 출력 필요없는 항목들 제거 (나중에 변경가능)
    del df['transaction_id']
    del df['세금']
    del df['수수료']
    del df['매도 손익']
    del df['환전 매도 손익']

    # 5. 보유수량, 평균단가, 총투자금, 현재주가, 평가수익률, 평가손익, 평가금액, 비중, 섹터 (매매 시작일)
    df = df.groupby('종목명').agg({
        '티커': 'first',
        '보유 수량': 'sum',
        '매수/매도 일자': 'first',
        '섹터': 'first',
        '총 투자액':'sum',}).reset_index()

    # 포트폴리오 종목들을 기준으로 현재가격을 가져오기
    for idx, row in df.iterrows():
        df.loc[idx, '현재 주가'] = fdr.DataReader(row['티커'])['Close'][-1]
    df['현재 주가'] = df['현재 주가'].astype(int)
    print(df)

    # 보유 투자액 / 보유 수량 == df['평균 단가']
    df['평균 단가'] = df['총 투자액'] / df['보유 수량']
    df['평균 단가'] = df['평균 단가'].astype(int)

    # 평가손익, 평가수익률, 평가금액, 비중, 환율평균 계산
    df['평가 손익'] = (df['현재 주가'] - df['평균 단가']) * df['보유 수량']
    df['평가 수익률'] = (df['현재 주가'] - df['평균 단가']) / df['평균 단가'] * 100
    df['평가 금액'] = df['현재 주가'] * df['보유 수량']
    # df['환율 평균'] = df['환율'] * df['보유 수량']/df['보유 수량'].sum()
    # 비중 =  해당 종목 평가 금액 / 총 평가금액 *100
    df['비중'] = df['평가 금액'] / df['평가 금액'].sum() * 100

    # 새로운 칼럼 순서 정리
    columns = ['종목명','평균 단가','보유 수량','총 투자액','평가 금액','현재 주가','평가 손익','평가 수익률','매수/매도 일자','섹터','비중']
    
    # 환율 평균을 계산하기가 힘듬
    df = df[columns]
    df.set_index('종목명',inplace=True)

    if response.status_code == 200:
        return df
    else:
        return pd.DataFrame()


def create_portfolio_table(df):
    st.dataframe(df, use_container_width=True)

def create_pie_chart_by_stockname(df):
    fig1 = px.pie(df, values='평가 금액', names=df.index, title='종목별 비중 (평가금액)')
    st.plotly_chart(fig1, use_container_width=True)

def create_pie_chart_by_section(df):
    fig2 = px.pie(df, values='평가 금액', names='섹터', title='섹터별 비중 (평가금액)')
    st.plotly_chart(fig2, use_container_width=True)

def create_bar_chart_by_nation(df):
    fig3 = px.pie(df, values='평가 금액', names='국가', title='국가별 평가금액')
    st.plotly_chart(fig3, use_container_width=True)


total, korea, usa, dollar= st.tabs(['Total', 'Korea', 'USA','Dollar'])


df_kor = fetch_kor_data()
df_usa = fetch_usa_data()

today = datetime.date.today()
yesterday = today - datetime.timedelta(1)

# 어제와 오늘의 USD/KRW 환율을 가져옵니다.
df_today = fdr.DataReader('USD/KRW', today)
df_yesterday = fdr.DataReader('USD/KRW', yesterday)

# 오늘의 USD/KRW 환율을 가져옵니다.
try:
    exchange_today = df_today['Close'].iloc[-1] # 여기서 버그생김 밤이라 그런가?
except:
    exchange_today = df_yesterday['Close'].iloc[-1]
exchange_today = round(exchange_today, 2)

# 어제 오늘의 변화량을 기록합니다.
change = exchange_today - df_yesterday['Close'].iloc[-1]
change = round(change, 2)
if change >= 0:
    change_diff = str("+") + str(change)+ str("%")
else:
    change_diff = str(change)+ str("%")
change_percent = change / df_yesterday['Close'].iloc[-1] * 100

@st.cache_data()
def fecth_both_data():
    #columns = ['종목명','평균 단가','보유 수량','총 투자액','평가 금액','현재 주가','평가 손익','평가 수익률','매수/매도 일자','섹터','비중']
    df_kor_cpy = df_kor.copy()
    df_usa_cpy = df_usa.copy()
    df_usa_cpy['평균 단가'] = df_usa_cpy['평균 단가'] * exchange_today
    df_usa_cpy['현재 주가'] = df_usa_cpy['현재 주가'] * exchange_today
    df_usa_cpy['총 투자액'] = df_usa_cpy['총 투자액'] * exchange_today
    df_usa_cpy['평가 금액'] = df_usa_cpy['평가 금액'] * exchange_today
    df_usa_cpy['평가 손익'] = df_usa_cpy['평가 손익'] * exchange_today

    del df_usa_cpy['비중']
    del df_kor_cpy['비중']

    df = pd.concat([df_kor_cpy, df_usa_cpy])

    #전체에서 비중을 새로 계산
    df['비중'] = df['평가 금액'] / df['평가 금액'].sum() * 100
    return df

@st.cache_data()
def fetch_nation_data():
    df_kor_cpy = df_kor.copy()
    df_usa_cpy = df_usa.copy()
    df_usa_cpy['총 투자액'] = df_usa_cpy['총 투자액'] * exchange_today
    total_usa = int(df_usa_cpy['총 투자액'].sum())
    total_kor = int(df_kor_cpy['총 투자액'].sum())
    df = pd.DataFrame({'국가':['한국','미국'],'평가 금액':[total_kor,total_usa]})
    return df

with total:
    df = fecth_both_data()
    both_total = int(df['평가 금액'].sum())
    kor_total = int(df_kor['평가 금액'].sum())
    usa_total = int(df_usa['평가 금액'].sum() * exchange_today)

    both_total_diff = int(df['평가 손익'].sum())
    kor_total_diff = int(df_kor['평가 손익'].sum())
    usa_total_diff = int(df_usa['평가 손익'].sum()*exchange_today)

    both_total = "{:,}".format(both_total)
    kor_total = "{:,}".format(kor_total)
    usa_total = "{:,}".format(usa_total)

    # both_total_diff = "{:,}".format(both_total_diff)
    # kor_total_diff = "{:,}".format(kor_total_diff)
    # usa_total_diff = "{:,}".format(usa_total_diff)

    if both_total_diff >= 0:
        both_total_diff = str("+") + str(both_total_diff) + "원"
    else:
        both_total_diff = str(both_total_diff) + "원"

    if kor_total_diff >= 0:
        kor_total_diff = str("+") + str(kor_total_diff) + "원"
    else:
        kor_total_diff = str(kor_total_diff) + "원"

    if usa_total_diff >= 0:
        usa_total_diff = str("+") + str(usa_total_diff) + "원"
    else:
        usa_total_diff = str(usa_total_diff) + "원"

    both_total = str(both_total) + "원"
    kor_total = str(kor_total) + "원"
    usa_total = str(usa_total) + "원"

    st.title("All Accounts")
    col1, col2, col3, col4 = st.columns(4)
    # 비중을 이런걸로 표시해도 UI가 괜찮을듯
    col1.metric("총 자산(원)", both_total, both_total_diff)
    col2.metric("한국 주식(원)",kor_total, kor_total_diff)
    col3.metric("미국 주식(원)", usa_total, usa_total_diff)
    col4.metric("원/달러 환율",round(exchange_today,2), change_diff)

    create_portfolio_table(df)
    create_pie_chart_by_stockname(df)
    create_pie_chart_by_section(df)

    df_nation = fetch_nation_data()
    create_bar_chart_by_nation(df_nation)


with korea:
    st.title("Korea Accounts")
    # 1. 주식 별로 매수 기록 다 불러와서 오름차순으로 정렬하기
    # 2. 매도기록에 대한 실현 손익 column을 생성해준다. 매수기록과 매도기록 매칭은 어떻게해? -> 찾아서 지우기? -> 지우면 월별 매매기록이 안보여
    # 3. 개수나눠서 어떻게 처리하지 매도량 update하기? -> 매도 입력시에 매수 기록의 매도량 update 필요
    # 4. 매도가격 측정은? -> 매도 기록 옆에 매수 가격 컬럼 추가해서 관리 -> 매도 입력시에 추가 처리 필요
    # 5. 그것의 합을 구하면 해당 월의 실현손익일듯.
    create_portfolio_table(df_kor)
    create_pie_chart_by_stockname(df_kor)
    create_pie_chart_by_section(df_kor)


with usa:
    st.title("USA Accounts")
    create_portfolio_table(df_usa)
    create_pie_chart_by_stockname(df_usa)
    create_pie_chart_by_section(df_usa)

st.write(st.session_state["username"],"님 환영합니다.")

st.markdown("# Portfolio page 💸")
st.sidebar.success("Portfolio Page 💸")
st.sidebar.info("여기는 메인 페이지입니다.포트폴리오를 여기다가 구현할 예정입니다.")
st.sidebar.title("Portfolio Page 💸")
st.sidebar.button("포트폴리오 그래프")
st.sidebar.checkbox("현재 포트폴리오의 종목별 비중")
st.sidebar.checkbox("현재 포트폴리오의 국가별 비중")
st.sidebar.checkbox("현재 포트폴리오의 자산별 비중")
st.sidebar.button("포트폴리오 수익률")



st.sidebar.markdown(
    """
    여기는 메인페이지입니다. 포트폴리오를 여기다가 구현할 예정입니다.
    환율정보를 가져오는 API를 사용하였습니다.
    본 페이지는 매매일지를 기반으로 결과를 출력만합니다.
    
    아래는 Optional한 기능들입니다.
    - 질문 요구페이지 추가
    - 모듈화 가능하게
    - 예금 포함
    - 주가 위치별 메모
    - 실제 계좌정보 가져올 수도 있는 가능성 부여
    - Gpt검색서비스 추가
    - 연수익률 그래프
    - 연 투자금액에 따른 해당 수익률 (의미가있나?)
    - 배당금 그래프
    """
)
st.markdown(
    """
    포트폴리오 그래프 
    
    - 현재 포트폴리오의 종목별 비중 (etc는 너무 작을때 그냥 무시)
    - 현재 포트폴리오의 분야별 비중
    - 현재 포트폴리오의 국가별 비중
    - 현재 포트폴리오의 자산별 비중
    - 증권사 별 수수료 
    
    예외 처리
    - 주식 분할 처리를 어떻게 할 것인가?
        - 주식 분할이 되면 모든 데이터를 분할후의 데이터로 교체
        - 분할되어 바뀌었다는것을 사용자에게 알리기
    - 주식 병합 처리도 해야 할 듯.
    - 상장 폐지 처리
    - 배당금 처리
    - 정렬해서 볼수있어야함. 
    보유수량, 단가, 투자금, 현재주가, 평가수익률, 섹터, 비중, 수수료, 고점 대비 하락율, 매매 시작 시점, 메모 (는 어떻게 저장할지는 모르겠네)

    (Optional) 월당 수익률 (기간당 수익률)
    
     주식 섹터별 비중 그래프 및 표
    
     주식 종목별 비중 그래프 및 표
    
     실현 손익
    
     평가 손익
	
	자산비중							
    현금	100%		평가 손익합			달러당 환율	
    주식	0%		
    채권	0%
    한국주식
    미국주식
    
    검색을 위한 DB가 필요하거나 검색 내용을 즉각적으로 보여주는 기능이 필요할듯.
    포트폴리오 추가하는 UI 추가
    """
)