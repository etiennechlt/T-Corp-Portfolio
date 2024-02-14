import pandas as pd
import requests
import json
import logging
import yfinance as yf


# Fonction pour charger et préparer les données (exemple basique)
def get_data(sheet_id=None, sheet_names=None):
    data = pd.DataFrame()
    for sheet_name in sheet_names:
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        try:
            df = pd.read_csv(csv_url)
            df["Name"] = sheet_name
            data = pd.concat([data, df], axis=0, ignore_index=True)
        except:
            logging.log(0, f"Error loading sheet: {sheet_name}")
            print(f"Error loading sheet: {sheet_name}")
    return data


# Renvoie le ticker à partir du nom de la compagnie
def get_ticker(company_name):
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    try:
        res = requests.get(url=yfinance, params=params, headers={'User-Agent': user_agent})
        data = res.json()

        company_code = data['quotes'][0]['symbol']
    except:
        logging.log(0, f"Error getting ticker: {company_name}")
        print(f"Error getting ticker: {company_name}")
        company_code = ""
    return company_code


def update_tickers(data_assets):
    with open("ticker_configs.json", "r") as f1:
        data_tickers = pd.DataFrame(json.load(f1)).dropna(how='any').drop_duplicates().reset_index()
    if (data_tickers.empty):
        data_tickers = pd.DataFrame(columns=['Titre', 'Ticker'])
    stock_to_update = data_assets.loc[~data_assets['Titre'].isin(data_tickers['Titre']), ['Titre', 'Ticker']]
    if len(stock_to_update):
        stock_to_update['Ticker'] = stock_to_update['Titre'].apply(lambda x: get_ticker(x))
        data_tickers = pd.concat([data_tickers, stock_to_update], axis=0, ignore_index=True)
        data_tickers.drop_duplicates(inplace=True)
        with open("ticker_configs.json", "w") as f2:
            json.dump(data_tickers[['Titre', 'Ticker']].to_dict(orient='records'), f2)
    data_assets['Ticker'] = data_assets['Titre'].apply(lambda x: data_tickers.loc[data_tickers['Titre']==x, 'Ticker'].values[0])


# Get price history from ticker
# https://pypi.org/project/yfinance/
def get_symbol_prices(symbol, period='1mo', interval='1h'):
    try:
        symbol_prices = yf.download(tickers=symbol, period=period, interval=interval)
    except:
        logging.log(0, f"Error getting prices: {symbol}")
        print(f"Error getting prices: {symbol}")
        symbol_prices = pd.DataFrame([])
    return symbol_prices

def get_symbol_info(symbol):
    try:
        info = yf.Ticker(symbol).info
    except:
        logging.log(0, f"Error getting info: {symbol}")
        print(f"Error getting info: {symbol}")
        info = {}
    return info

def get_symbol_sector(symbol):
    try:
        sector = yf.Ticker(symbol).info['sector']
    except:
        logging.log(0, f"Error getting sector: {symbol}")
        print(f"Error getting sector: {symbol}")
        sector = ""
    return sector

def get_symbol_country(symbol):
    try:
        country = yf.Ticker(symbol).info['country']
    except:
        logging.log(0, f"Error getting country: {symbol}")
        print(f"Error getting country: {symbol}")
        country = ""
    return country

def get_symbol_currency(symbol):
    try:
        currency = yf.Ticker(symbol).info['currency']
    except:
        logging.log(0, f"Error getting currency: {symbol}")
        print(f"Error getting currency: {symbol}")
        currency = ""
    return currency



def get_prices(data):
    data_prices = pd.DataFrame()
    for ticker in data['Ticker']:
        prices_month = get_symbol_prices(ticker, period='1mo', interval='1d').reset_index().rename(columns={"Date": "Datetime"})
        prices_week = get_symbol_prices(ticker, period='1w', interval='1h').reset_index()
        prices_day = get_symbol_prices(ticker, period='1d', interval='1m').reset_index()
        currency = get_symbol_currency(ticker)
        country = get_symbol_country(ticker)
        sector = get_symbol_sector(ticker)

        prices_month['Ticker'] = ticker
        prices_month['Currency'] = currency
        prices_month['Country'] = country
        prices_month['Sector'] = sector

        prices_week['Ticker'] = ticker
        prices_week['Currency'] = currency
        prices_week['Country'] = country
        prices_week['Sector'] = sector

        prices_day['Ticker'] = ticker
        prices_day['Currency'] = currency
        prices_day['Country'] = country
        prices_day['Sector'] = sector

        data_prices = pd.concat([data_prices, prices_month, prices_week, prices_day], axis=0, ignore_index=True)
    return data_prices


def compute_timedelta_variation(data, timedelta='24h'):
    data_sorted = data.sort_values("Datetime")
    data_shifted = data_sorted.loc[data_sorted['Datetime'] == data_sorted.iloc[-1]['Datetime'] - pd.to_timedelta(timedelta)]
    variation = (data_sorted.iloc[-1]['Close'] - data_shifted['Close']) * 100
    return variation