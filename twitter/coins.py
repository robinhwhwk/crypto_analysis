import requests
import json
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import io
import base64
import urllib.parse
from io import StringIO


def getPriceChart(query):
    try:
        coin_df = getPrice(query)
        coin_df = pd.DataFrame(coin_df['prices'])
        index = coin_df.index
        time = []
        now = datetime.now()
        for i in index:
            time.append(now - timedelta(minutes=i*5))
        coin_df['Time'] = [t for t in time]
        plt.cla()
        fig, ax = plt.subplots()
        plt.plot(coin_df['Time'], coin_df[1])
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        plt.title("Price change in the past day (UTC)")
        plt.tight_layout()
        fig = plt.gcf()
        fig.set_size_inches(5, 3, forward=True)
        image = io.BytesIO()
        plt.savefig(image, format='png')
        image.seek(0)
        string = base64.b64encode(image.read())
        image64 = "data:image/png;base64," + urllib.parse.quote_plus(string)
        return image64
    except ValueError:
        print(ValueError)
        return None


def getPrice(coin):
    # Edit this to return the plot of coin price in the last day
    query = "https://api.coingecko.com/api/v3/coins/" + \
        coin + "/market_chart?vs_currency=usd&days=1"
    response_api = requests.get(query)
    data = response_api.text
    parse_json = json.loads(data)
    return parse_json
