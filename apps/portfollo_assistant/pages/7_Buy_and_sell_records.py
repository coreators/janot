import datetime

import streamlit as st
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pandas as pd
import requests

usernameSession = 'username'
userSession = st.session_state[usernameSession]

st.markdown("# Buy, Sell Records")
st.sidebar.markdown("# Buy, Sell Records")

buy_or_sell = st.sidebar.selectbox("매수 매도 선택", ["매수", "매도"])

username = "sanghyeok"

korea, usa, dollar= st.tabs(['Korea', 'USA',"Dollar"])
st.sidebar.success("Trading Journal ➕")
st.sidebar.info(" 매수 매도 기록 페이지입니다.")
st.sidebar.title("Trading Journal ➕")
st.sidebar.markdown(
    """
    매수 매도 기록 페이지입니다.
    """
)

# 미리 저장해둔 데이터 읽어오기
kor_list_name = pd.read_csv("resources/kor_ticker_list.csv")['Name']
kor_list_code = pd.read_csv("resources/kor_ticker_list.csv")['Code']
kor_list_sector = pd.read_csv("resources/kor_ticker_list.csv")['Sector']

usa_list_name = pd.read_csv("resources/usa_ticker_list.csv")['Name']
usa_list_code = pd.read_csv("resources/usa_ticker_list.csv")['Code']
usa_list_sector = pd.read_csv("resources/usa_ticker_list.csv")['Sector']


def kor_sync_with_ticker_and_sector():
    st.session_state.ticker = kor_list_code[kor_list_name == st.session_state.ticker_searchbox].values[0]
    st.session_state.sector = kor_list_sector[kor_list_name == st.session_state.ticker_searchbox].values[0]

def usa_sync_with_ticker_and_sector():
    st.session_state.usa_ticker = usa_list_code[usa_list_name == st.session_state.usa_ticker_searchbox].values[0]
    st.session_state.usa_sector = usa_list_sector[usa_list_name == st.session_state.usa_ticker_searchbox].values[0]



def send_buy_journal(ticker, buy_price, buy_amount, buy_date, tax, fee, sector):
    print("buy ",ticker, buy_price, buy_amount, buy_date, tax, fee)
    response = requests.post('http://localhost:9000/api/v1/journal/kor/trade',
                             json={'email':st.session_state[usernameSession],
                                 'ticker': ticker, 'price': buy_price, 'amount': buy_amount, 'date': buy_date.isoformat(), 'tax': tax, 'fee': fee,
                                   'is_buy': True, 'sector': sector,'sold_amount':0,'profit_loss':0})
    return response

def get_buy_record_by_ticker_in_kor(ticker):
    response = requests.get('http://localhost:9000/api/v1/journal/kor/buy/record',
                            json={'email': st.session_state[usernameSession],
                                  'ticker': ticker})
    print("get kor buy record status : ", response)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        return pd.DataFrame()

def get_buy_record_by_ticker_in_usa(ticker):
    response = requests.get('http://localhost:9000/api/v1/journal/usa/buy/record',
                            json={'email': st.session_state[usernameSession],
                                  'ticker': ticker})
    print("get usa buy record status : ", response.json())
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        return pd.DataFrame()

def send_update_buy_journal(df_json):
    response = requests.put('http://localhost:9000/api/v1/journal/kor/buy/update',
                             json=df_json)
    print(response.json())
    return response

def send_sell_journal(ticker, sell_price, sell_amount, sell_date, tax, fee, sector, profit_loss):
    print("sell",ticker, sell_price, sell_amount, sell_date, tax, fee)
    response = requests.post('http://localhost:9000/api/v1/journal/kor/trade',
                             json={'email':st.session_state[usernameSession],
                                   'ticker': ticker, 'price': sell_price, 'amount': sell_amount, 'date': sell_date.isoformat(), 'tax': tax, 'fee': fee,
                                   'is_buy': False, 'sector': sector, 'sold_amount': 0, 'profit_loss': profit_loss})
    return response

def usa_send_buy_journal(ticker, buy_price, buy_amount, buy_date, tax, fee, sector, exchange_rate):
    print("buy ",ticker, buy_price, buy_amount, buy_date, tax, fee)
    response = requests.post('http://localhost:9000/api/v1/journal/usa/trade',
                             json={'email':st.session_state[usernameSession],
                                 'ticker': ticker, 'price': buy_price, 'amount': buy_amount, 'date': buy_date.isoformat(), 'tax': tax, 'fee': fee,
                                   'is_buy': True, 'sector': sector, 'exchange_rate':exchange_rate,
                                   'sold_amount':0,'profit_loss':0.0,'profit_loss_with_exchange':0.0})
    print(response.json())
    return response

def usa_send_update_buy_journal(df_json):
    response = requests.put('http://localhost:9000/api/v1/journal/usa/buy/update',
                            json=df_json)
    print(response.json())
    return response

def usa_send_sell_journal(ticker, sell_price, sell_amount, sell_date, tax, fee, sector ,exchange_rate, profit_loss, profit_loss_with_exchange):
    # 매수 갯수가 있는지 query로 확인해야함.

    print("sell",ticker, sell_price, sell_amount, sell_date, tax, fee, profit_loss)
    response = requests.post('http://localhost:9000/api/v1/journal/usa/trade',
                             json={'email':st.session_state[usernameSession],
                                   'ticker': ticker, 'price': sell_price, 'amount': sell_amount, 'date': sell_date.isoformat(), 'tax': tax, 'fee': fee,
                                   'is_buy': False, 'sector': sector, 'exchange_rate':exchange_rate,
                                   'sold_amount': 0, 'profit_loss': profit_loss, 'profit_loss_with_exchange': profit_loss_with_exchange})
    return response


# 한국 주식 기록 탭
with korea:
    if buy_or_sell == "매수":
        st.empty()
        st.title("한국 주식 매수 일지 작성")
        # pandas나 numpy로 배열 바꿀 수 있음. box를 yahoo finance에서 가져온 data frame으로 바꾸기
        search_box = st.selectbox("회사 이름", kor_list_name, key="ticker_searchbox", on_change=kor_sync_with_ticker_and_sector)
        st.info("회사 이름을 선택하면 회사 코드와 섹터가 자동으로 채워집니다.")
        # schemas.py : ticker price amount date tax fee
        ticker = st.text_input("티커",disabled=True, key="ticker", value=kor_list_code[0])
        sector = st.text_input("섹터", disabled=True, key="sector", value=kor_list_sector[0])
        buy_price = st.number_input("매수 가격", key="buy_price", min_value=0, value=0, step=100, format=None)
        buy_amount = st.number_input("매수 수량", key="buy_amount", min_value=1, value=1, step=1, format=None)
        buy_date = st.date_input("매수 일자", key="buy_date", value=None, min_value=None, max_value=datetime.date.today(), help=None)
        tax = st.number_input("수수료율", key="tax", min_value=0.0, value=0.2, step=0.01, format=None, help="한국 주식 매도 수수료는 0.2% 입니다")
        fee = st.number_input("거래세율", key="fee", min_value=0.0, value=0.00, step=0.01, format=None, help="한국 주식 매수 거레세율은 0% 입니다")
        submit = st.button(label="Submit",key="kor_buy_submit")
        if submit:
            response = send_buy_journal(ticker, buy_price, buy_amount, buy_date, tax, fee, sector)
            print(buy_date)
            if response.status_code == 200:
                st.success("매수 기록 등록이 완료했습니다!")
                request_summary = search_box + "에 대한 매수 기록이 등록되었습니다."
                st.info(request_summary) #좀 더 구체적으로 쓰기
            else:
                st.error("매수 기록 등록이 실패했습니다!")
                st.stop()
            # add error handling
            # print warning whether data is correct or not
    else:
        st.empty()
        st.title("한국 주식 매도 일지 작성")
        st.text("매수 기록이 있는 경우에만 매도 기록을 작성할 수 있습니다.")
        search_box = st.selectbox("회사 이름", kor_list_name, key="ticker_searchbox", on_change=kor_sync_with_ticker_and_sector)
        st.info("회사 이름을 선택하면 회사 코드와 섹터가 자동으로 채워집니다.")
        # schemas.py : ticker price amount date tax fee
        ticker = st.text_input("티커", disabled=True, key="ticker", value=kor_list_code[0]) # 회사이름으로 ticker 검색해서 ticker 부분에 넣기
        sector = st.text_input("섹터", disabled=True, key="sector", value=kor_list_sector[0])
        sell_price = st.number_input("매도 가격", key="buy_price", min_value=0, value=0, step=100, format=None)
        sell_amount = st.number_input("매도 수량", key="buy_amount", min_value=1, value=1, step=1, format=None)
        sell_date = st.date_input("매도 일자", key="buy_date", value=None, min_value=None, max_value=datetime.date.today(), help=None)
        tax = st.number_input("수수료율", key="tax", min_value=0.000, value=0.015, step=0.001, format="%.3f", help="한국 주식 매도 수수료는 0.015% 입니다")
        fee = st.number_input("거래세율", key="fee", min_value=0.0, value=0.2, step=0.01, format=None, help="한국 주식 매도 거래세율은 0.2% 입니다")
        submit = st.button(label="Submit",key="kor_sell_submit")
        if submit:
            # 매도 가능한 기록이 있는지 확인
            # 충분한 양의 매수가 있는지
            buy_record_df = get_buy_record_by_ticker_in_kor(ticker)
            # 매수 기록이 없으면 멈춤
            if buy_record_df.empty:
                st.error("해당 종목에 대한 매수 기록이 없습니다!")
                st.stop()

            buy_record_df['date'] = pd.to_datetime(buy_record_df['date'])
            buy_record_df['remaining_amount'] = buy_record_df['amount'] - buy_record_df['sold_amount']
            # remaining 값이 0이 아닌 row만 남김
            buy_record_df = buy_record_df[buy_record_df['remaining_amount'] != 0]

            # 날짜를 오름차순으로 정렬
            buy_record_df = buy_record_df.sort_values(by=['date'], ascending=True)

            # 매수 기록이 있으면 양이 충분한지 확인
            if buy_record_df['remaining_amount'].sum() < sell_amount:
                msg = "해당 종목에 대한 매수 수량이 충분하지 않습니다! " + " 남아있는 양: "+ str(buy_record_df['remaining_amount'].sum())+", 팔려는 양: " + str(sell_amount)
                st.error(msg)
                st.stop()

            # remaining amount는 필요없으므로 삭제
            buy_record_df = buy_record_df.drop(['remaining_amount'], axis=1)
            print(buy_record_df)

            # df에 저장하고 update 되어야할 값들
            update_buy_record_df = buy_record_df.copy()
            update_buy_record_df = update_buy_record_df.iloc[0:0]
            update_idx = 0
            profit_loss = 0


            tmp_sell_amount = sell_amount
            # 가장 오래된 매수 기록 부터 지우기
            for index, row in buy_record_df.iterrows():
                remaining_amount = buy_record_df.loc[index, 'amount'] - buy_record_df.loc[index, 'sold_amount']
                # sell amount가 레코드의 amount보다 크거나 같으면 sold_amount를 amount로 바꾸고 remaining_amount를 0으로 바꿈
                if tmp_sell_amount > remaining_amount:
                    # sell amount 계산
                    buy_record_df.loc[index, 'sold_amount'] += remaining_amount
                    # print("sold amount result : ",buy_record_df.loc[index, 'sold_amount'])

                    # 매수 기록에 sold amount update
                    update_buy_record_df.loc[update_idx] = buy_record_df.loc[index]
                    update_idx+=1

                    # 매매 손익 (profit_loss) 값 계산, (매도 금액 - 매수금액) * 매도 수량
                    profit_loss += (sell_price - buy_record_df.loc[index, 'price']) * remaining_amount
                    tmp_sell_amount = tmp_sell_amount - remaining_amount
                else:
                    #sell amount가 적혀있는 레코드보다 작으면
                    buy_record_df.loc[index, 'sold_amount'] += tmp_sell_amount
                    # print("sold amount result : ",buy_record_df.loc[index, 'sold_amount'])

                    # 매수 기록에 sold amount update
                    update_buy_record_df.loc[update_idx] = buy_record_df.loc[index]
                    update_idx+=1

                    # 매매 손익 (profit_loss) 값 계산, (매도 금액 - 매수금액) * 매도 수량
                    profit_loss += (sell_price - buy_record_df.loc[index, 'price']) * tmp_sell_amount
                    tmp_sell_amount = 0
                    break

            update_buy_record_df['date'] = update_buy_record_df['date'].dt.strftime('%Y-%m-%d')
            # numpy64를 파이썬 기본 int로 바꿔주어야함.
            profit_loss = int(profit_loss)
            print("profit is ", profit_loss)

            # 해당 price를 어디에 저장해서 보관해두기
            update_response = send_update_buy_journal(update_buy_record_df.to_dict(orient='records'))
            if update_response.status_code == 200:
                response = send_sell_journal(ticker, sell_price, sell_amount, sell_date, tax, fee, sector, profit_loss)
                if response.status_code == 200:
                    st.success("매도 기록 등록이 완료했습니다!")
                    request_summary = search_box + "에 대한 매도 기록이 등록되었습니다."
                    st.info(request_summary)
                else:
                    st.error("매도 기록 등록이 실패했습니다!")
                    st.stop()




# 미국 주식 기록 탭
with usa:
    if buy_or_sell == "매수":
        st.empty()
        st.title("미국 주식 매수 일지 작성")
        # pandas나 numpy로 배열 바꿀 수 있음. box를 yahoo finance에서 가져온 data frame으로 바꾸기
        search_box = st.selectbox("회사 이름", usa_list_name, key="usa_ticker_searchbox", on_change=usa_sync_with_ticker_and_sector)
        st.info("회사 이름을 선택하면 회사 코드와 섹터가 자동으로 채워집니다.")
        # schemas.py : ticker price amount date tax fee
        ticker = st.text_input("티커", disabled=True, key="usa_ticker", value=usa_list_code[0])
        sector = st.text_input("섹터", disabled=True, key="usa_sector", value=usa_list_sector[0])
        buy_price = st.number_input("매수 가격", key="usa_buy_price", min_value=0.0, value=0.0, step=0.01, format=None)
        buy_amount = st.number_input("매수 수량", key="usa_buy_amount", min_value=1, value=1, step=1, format=None)
        buy_date = st.date_input("매수 일자", key="usa_buy_date", value=None, min_value=None, max_value=datetime.date.today(), help=None)
        tax = st.number_input("수수료율", key="usa_tax", min_value=0.0, value=0.07, step=0.01, format=None, help="키움증권 미국 주식 매매 혜택 수수료율은 0.07% 입니다")
        fee = st.number_input("거래세율", key="usa_fee", min_value=0.0, value=0.0, step=0.01, format=None, help="미국 주식 매수 거래세율은 0% 입니다")
        exchange_rate = st.number_input("환율", key="exchange_rate", min_value=0.0, value=1300.00, step=0.01, format=None, help="달러당 원화 환율을 입력해주세요")
        submit = st.button(label="Submit",key="usa_buy_submit")
        if submit:
            response = usa_send_buy_journal(ticker, buy_price, buy_amount, buy_date, tax, fee, sector,exchange_rate)
            print(buy_date)
            if response.status_code == 200:
                st.success("매수 기록 등록이 완료했습니다!")
                request_summary = search_box + "에 대한 매수 기록이 등록되었습니다."
                st.info(request_summary) #좀 더 구체적으로 쓰기
            else:
                st.error("매수 기록 등록이 실패했습니다!")
                st.stop()
            # add error handling
            # print warning whether data is correct or not
    else:
        st.empty()
        st.title("미국 주식 매도 일지 작성")
        search_box = st.selectbox("회사 이름", usa_list_name, key="usa_ticker_searchbox", on_change=usa_sync_with_ticker_and_sector)
        st.info("회사 이름을 선택하면 회사 코드와 섹터가 자동으로 채워집니다.")
        # schemas.py : ticker price amount date tax fee
        ticker = st.text_input("티커",disabled=True, key="usa_ticker", value=usa_list_code[0])
        sector = st.text_input("섹터", disabled=True, key="usa_sector", value=usa_list_sector[0])
        sell_price = st.number_input("매도 가격", key="usa_buy_price", min_value=0.0, value=0.0, step=0.01, format=None)
        sell_amount = st.number_input("매도 수량", key="usa_buy_amount", min_value=1, value=1, step=1, format=None)
        sell_date = st.date_input("매도 일자", key="usa_buy_date", value=None, min_value=None, max_value=datetime.date.today(), help=None)
        tax = st.number_input("수수료율", key="usa_tax", min_value=0.0, value=0.07, step=0.01, format=None, help="키움증권 미국 주식 매매 혜택 수수료율은 0.07% 입니다")
        fee = st.number_input("거래세율", key="usa_fee", min_value=0.0, value=0.0008, step=0.0001, format="%.4f", help="미국 주식 매수 거래세율은 0.0008% 입니다")
        # 매도 환율은 1. 매수 환율과 동일하거나 2. 원화로 특정 환율로 환전했으면 환전 값을 넣거나 둘중에 하나로 하기 (버튼 추가해야할수도)
        exchange_rate = st.number_input("환율", key="exchange_rate", min_value=0.0, value=1300.00, step=0.01, format=None, help="달러당 원화 환율을 입력해주세요")
        submit = st.button(label="Submit",key="usa_sell_submit")
        if submit:
            # 매도 가능한 기록이 있는지 확인
            # 충분한 양의 매수가 있는지
            buy_record_df = get_buy_record_by_ticker_in_usa(ticker)
            # 매수 기록이 없으면 멈춤
            if buy_record_df.empty:
                st.error("해당 종목에 대한 매수 기록이 없습니다!")
                st.stop()

            buy_record_df['date'] = pd.to_datetime(buy_record_df['date'])
            buy_record_df['remaining_amount'] = buy_record_df['amount'] - buy_record_df['sold_amount']
            # remaining 값이 0이 아닌 row만 남김
            buy_record_df = buy_record_df[buy_record_df['remaining_amount'] != 0]

            # 날짜를 오름차순으로 정렬
            buy_record_df = buy_record_df.sort_values(by=['date'], ascending=True)

            # 매수 기록이 있으면 양이 충분한지 확인
            if buy_record_df['remaining_amount'].sum() < sell_amount:
                 msg = "해당 종목에 대한 매수 수량이 충분하지 않습니다! " + " 남아있는 양: "+ str(buy_record_df['remaining_amount'].sum())+", 팔려는 양: " + str(sell_amount)
                 st.error(msg)
                 st.stop()

            # remaining amount는 필요없으므로 삭제
            buy_record_df = buy_record_df.drop(['remaining_amount'], axis=1)

            # df에 저장하고 update 되어야할 값들
            update_buy_record_df = buy_record_df.copy()
            update_buy_record_df = update_buy_record_df.iloc[0:0]
            update_idx = 0
            profit_loss = 0.0
            profit_loss_with_exchange = 0.0


            tmp_sell_amount = sell_amount
            print(tmp_sell_amount)
            print(buy_record_df)
            # 가장 오래된 매수 기록 부터 지우기
            for index, row in buy_record_df.iterrows():
                 remaining_amount = buy_record_df.loc[index, 'amount'] - buy_record_df.loc[index, 'sold_amount']
                 # sell amount가 레코드의 amount보다 크거나 같으면 sold_amount를 amount로 바꾸고 remaining_amount를 0으로 바꿈
                 if tmp_sell_amount > remaining_amount:
                     # sell amount 계산
                     buy_record_df.loc[index, 'sold_amount'] += remaining_amount
                     print("if sold amount result : ",buy_record_df.loc[index, 'sold_amount'])

                     # 매수 기록에 sold amount update
                     update_buy_record_df.loc[update_idx] = buy_record_df.loc[index]
                     update_idx+=1

                     # 매매 손익 (profit_loss) 값 계산, (매도 금액 - 매수금액) * 매도 수량
                     profit_loss += (sell_price - buy_record_df.loc[index, 'price']) * remaining_amount
                     profit_loss_with_exchange += (sell_price * exchange_rate  - buy_record_df.loc[index, 'price'] * buy_record_df.loc[index, 'exchange_rate']) * remaining_amount
                     tmp_sell_amount = tmp_sell_amount - remaining_amount
                 else:
                     #sell amount가 적혀있는 레코드보다 작으면
                     buy_record_df.loc[index, 'sold_amount'] += tmp_sell_amount
                     print("else sold amount result : ",buy_record_df.loc[index, 'sold_amount'])

                     # 매수 기록에 sold amount update
                     update_buy_record_df.loc[update_idx] = buy_record_df.loc[index]
                     update_idx+=1

                     # 매매 손익 (profit_loss) 값 계산, (매도 금액 - 매수금액) * 매도 수량
                     profit_loss += (sell_price - buy_record_df.loc[index, 'price']) * tmp_sell_amount
                     profit_loss_with_exchange += (sell_price * exchange_rate  - buy_record_df.loc[index, 'price'] * buy_record_df.loc[index, 'exchange_rate']) * tmp_sell_amount
                     tmp_sell_amount = 0
                     break

            # 정렬을 위해 계산가능하게 바꿔놓은 date를 원래 연-월-일 포맷으로 변환
            update_buy_record_df['date'] = update_buy_record_df['date'].dt.strftime('%Y-%m-%d')

            # numpy64를 파이썬 기본 float으로 바꿔주어야함.
            profit_loss = float(profit_loss)
            profit_loss_with_exchange = float(profit_loss_with_exchange)
            print(update_buy_record_df)
            print("profit is ", profit_loss, "profit with exchange is ", profit_loss_with_exchange)

            # 해당 price를 어디에 저장해서 보관해두기
            update_response = usa_send_update_buy_journal(update_buy_record_df.to_dict(orient='records'))
            if update_response.status_code == 200:
                 response = usa_send_sell_journal(ticker, sell_price, sell_amount, sell_date, tax, fee, sector, exchange_rate, profit_loss, profit_loss_with_exchange)
                 if response.status_code == 200:
                    st.success("매도 기록 등록이 완료했습니다!")
                    request_summary = search_box + "에 대한 매도 기록이 등록되었습니다."
                    st.info(request_summary)
                 else:
                    st.error("매도 기록 등록이 실패했습니다!")
                    st.stop()
