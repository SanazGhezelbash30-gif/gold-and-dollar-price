from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import json
import re

app = Flask(__name__)

def get_gold_price():
    url = "https://www.tgju.org/profile/geram18"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers= headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_elem = soup.find(string=re.compile(r'\d{3},\d{3},?\d*'))
    
    if price_elem:
        price = re.sub(r'[^\d]', '', price_elem)  
        return int(price)
    return None


def get_dollar_price():
    url = "https://www.tgju.org/profile/price_dollar_rl"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    price_elem = soup.find(string=re.compile(r'\d{1},\d{3},?\d*'))
    if price_elem:
        price = re.sub(r'[^\d]', '', price_elem)
        return int(price)
    return None

def main():
    gold = get_gold_price()
    dollar = get_dollar_price()
    
    data = {
        'gold_18k_per_gram': gold,
        'dollar_free': dollar,
        'timestamp': '2026-02-21'
    }
    
    print(f"price of God(18): {gold:,} rials [gram]")
    print(f"price of dollar {dollar:,} rials")
    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\nداده‌ها در prices.json ذخیره شد.")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/prices')
def api_prices():
    gold = get_gold_price()
    dollar = get_dollar_price()
    data = {
        'gold_18k': f"{gold:,}" if gold else "نامشخص",
        'dollar_free': f"{dollar:,}" if dollar else "نامشخص",
        'timestamp': 'به‌روزرسانی لحظه‌ای'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

