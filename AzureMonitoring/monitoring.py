from azure.storage.blob import BlobServiceClient
import io
import time
import binance as bnb
import pandas as pd
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

def get_exchange_info():
    """Get exchange information from Binance API"""
    info = requests.get('https://api.binance.com/api/v3/exchangeInfo')
    return info.json()

def create_overview_df(info):
    """Create overview DataFrame from exchange info"""
    symbols_df = pd.DataFrame(info['symbols'])
    overview_df = symbols_df[[
        'symbol',
        'baseAsset', 
        'quoteAsset',
        'status',
        'baseAssetPrecision',
        'quotePrecision'
    ]]
    return overview_df[overview_df.status == 'TRADING']

def setup_binance_client():
    """Setup Binance API client"""
    load_dotenv()
    apiKey = os.getenv('BinanceAPIKey')
    secret = os.getenv('BinanceAPISecret')
    client = bnb.Client(api_key=apiKey, api_secret=secret)
    return client


def get_tickers_df(client, overview_df):
    """Get tickers data and convert to DataFrame"""
    all_tickers = client.get_all_tickers()
    tickers_df = pd.DataFrame(all_tickers)
    trading_symbols = overview_df['symbol']
    tickers_df = tickers_df[tickers_df['symbol'].isin(trading_symbols)]
    tickers_df['price'] = pd.to_numeric(tickers_df['price'], errors='coerce')
    
    return tickers_df

def split_pair(pair):
    """Split trading pair into base and quote currencies"""
    quote_currencies = ['USDT', 'USDC', 'BTC', 'ETH']
    for quote in quote_currencies:
        if pair.endswith(quote):
            return pair[:-len(quote)], quote
    return pair, None

def create_arbitrage_matrix(tickers_df):
    """Create arbitrage matrix from tickers data"""
    # Create base and quote columns
    tickers_df[['Base', 'Quote']] = tickers_df['symbol'].apply(lambda x: pd.Series(split_pair(x)))
    
    # Filter quotes and create pivot table
    tickers_df = tickers_df[tickers_df['Quote'].isin(['USDT', 'USDC', 'BTC', 'ETH'])]
    arbitrage_matrix = tickers_df.pivot(index='Base', columns='Quote', values='price')
    
    # Format matrix
    arbitrage_matrix.reset_index(inplace=True)
    arbitrage_matrix.columns.name = None
    arbitrage_matrix = arbitrage_matrix.rename(columns={'Base': 'COIN'})
    
    # Ensure column order
    cols = ['COIN', 'BTC', 'ETH', 'USDC', 'USDT']
    return arbitrage_matrix.reindex(columns=cols)

def get_arbitrage_matrix():
    """Main function to run the analysis"""
    # Get exchange info and create overview DataFrame
    info = get_exchange_info()
    overview_df = create_overview_df(info)
    
    # Setup client and get tickers data
    client = setup_binance_client()
    tickers_df = get_tickers_df(client,overview_df)
    
    # Create and return arbitrage matrix
    arbitrage_matrix = create_arbitrage_matrix(tickers_df)
    return arbitrage_matrix

def create_base_conversion_matrix(arbitrage_matrix):
    """Create initial conversion matrix with base currencies"""
    base_currencies = ['BTC', 'ETH', 'USDC', 'USDT']
    conversion_matrix = arbitrage_matrix[arbitrage_matrix['COIN'].isin(base_currencies)]
    
    # Set diagonal values to 1
    for currency in base_currencies:
        conversion_matrix.loc[conversion_matrix['COIN'] == currency, currency] = 1
        
    return conversion_matrix

def calculate_cross_rates(conversion_matrix):
    """Calculate cross-rates between currencies"""
    # Calculate BTC/ETH rate
    btc_eth = 1/float(conversion_matrix.loc[conversion_matrix['COIN'] == 'ETH', 'BTC'].iloc[0])
    conversion_matrix.loc[conversion_matrix['COIN'] == 'BTC', 'ETH'] = btc_eth
    
    # Calculate USDC/BTC rate
    usdc_btc = 1/float(conversion_matrix.loc[conversion_matrix['COIN'] == 'BTC', 'USDC'].iloc[0])
    conversion_matrix.loc[conversion_matrix['COIN'] == 'USDC', 'BTC'] = usdc_btc
    
    # Calculate USDC/ETH rate
    usdc_eth = 1/float(conversion_matrix.loc[conversion_matrix['COIN'] == 'ETH', 'USDT'].iloc[0])
    conversion_matrix.loc[conversion_matrix['COIN'] == 'USDC', 'ETH'] = usdc_eth
    
    return conversion_matrix

def convert(source='BTC', destination='ETH', amount=1, conversion_matrix=None):
    """Convert amount from one currency to another"""
    conversion_rate = conversion_matrix.loc[conversion_matrix['COIN'] == source, destination].values[0]
    return amount * conversion_rate

def get_coin_price_USDT(coin, df):
    coin_usdt = df[df['COIN'] == coin]['USDT_actual'].values[0]
    return coin_usdt

def get_coin_price_BTC(coin, df):
    coin_btc = df[df['COIN'] == coin]['BTC_actual'].values[0]
    return coin_btc

def get_coin_price_ETH(coin, df):
    coin_eth = df[df['COIN'] == coin]['ETH_actual'].values[0]
    return coin_eth

def get_coin_price_USDC(coin, df):
    coin_usdc = df[df['COIN'] == coin]['USDC_actual'].values[0]
    return coin_usdc

def collect_arbitrage_snapshot():
    # Get fresh data from Binance
    arbitrage_matrix = get_arbitrage_matrix()
    conversion_matrix = create_base_conversion_matrix(arbitrage_matrix)
    conversion_matrix = calculate_cross_rates(conversion_matrix)
    df = arbitrage_matrix.dropna()
    df.columns = ['COIN', 'BTC_actual', 'ETH_actual', 'USDC_actual', 'USDT_actual']
    
    # Calculate arbitrage opportunities
    results = []
    for i in range(len(df)):
        coin = df.iloc[i]['COIN']
        
        try:
            # Calculate paths for each coin
            starting_quantity = 100/get_coin_price_USDT(coin, df)
            
            # COIN -> USDT
            path1 = get_coin_price_USDT(coin, df) * starting_quantity
            
            # COIN -> BTC -> USDT
            path2 = get_coin_price_BTC(coin, df) * starting_quantity
            path2 = convert(source='BTC', destination='USDT', amount=path2, conversion_matrix=conversion_matrix)
            
            # COIN -> ETH -> USDT
            path3 = get_coin_price_ETH(coin, df) * starting_quantity
            path3 = convert(source='ETH', destination='USDT', amount=path3, conversion_matrix=conversion_matrix)
            
            # COIN -> USDC -> USDT
            path4 = get_coin_price_USDC(coin, df) * starting_quantity
            path4 = convert(source='USDC', destination='USDT', amount=path4, conversion_matrix=conversion_matrix)
            
            # Find best path and calculate profit
            paths = [path1, path2, path3, path4]
            path_names = ["Direct", "Via BTC", "Via ETH", "Via USDC"]
            best_path_index = paths.index(max(paths))
            profit_percentage = ((paths[best_path_index] - path1) / path1) * 100
            
            results.append({
                'coin': coin,
                'profit_percentage': profit_percentage,
                'best_path': path_names[best_path_index],
                'direct_value': path1,
                'btc_path_value': path2,
                'eth_path_value': path3,
                'usdc_path_value': path4,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            # Skip coins with missing data
            print(f"Error processing {coin}: {str(e)}")
            continue
    
    # Return top opportunities sorted by profit percentage
    print(results)
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('profit_percentage', ascending=False)
    return results_df

if __name__ == "__main__":
    while True:
        try:
        # Get arbitrage data
            arbitrage_matrix = get_arbitrage_matrix()
            conversion_matrix = create_base_conversion_matrix(arbitrage_matrix)
            conversion_matrix = calculate_cross_rates(conversion_matrix)
            resulting_df = collect_arbitrage_snapshot()
            # Download existing arbitrage data from Azure Blob Storage
            # Azure Blob Storage connection details
            connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
            container_name = "arbitrage-data"
            blob_name = "arbitrage_history.csv"
            
            try:
                # Initialize the BlobServiceClient
                blob_service_client = BlobServiceClient.from_connection_string(connection_string)
                container_client = blob_service_client.get_container_client(container_name)
                
                # Create container if it doesn't exist
                try:
                    container_client.create_container()
                    print(f"Container '{container_name}' created")
                except Exception:
                    # Container already exists
                    pass
                
                blob_client = container_client.get_blob_client(blob_name)
                
                # Check if the blob exists
                try:
                    # Download the existing CSV
                    download_stream = blob_client.download_blob()
                    existing_data = pd.read_csv(io.StringIO(download_stream.content_as_text()))
                    
                    # Append new data
                    combined_df = pd.concat([existing_data, resulting_df], ignore_index=True)
                except Exception:
                    # If blob doesn't exist, use only the new data
                    combined_df = resulting_df
                    
                # Upload the combined data back to Azure Blob Storage
                csv_content = combined_df.to_csv(index=False)
                blob_client.upload_blob(csv_content, overwrite=True)
                print(f"Successfully uploaded arbitrage data to {blob_name}")
                
            except Exception as e:
                print(f"Error handling blob storage: {str(e)}")
            time.sleep(5)
        except Exception as e:
            print(e)
            pass