from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup

bp = Blueprint('btc_usd_investing', __name__)
import cloudscraper
from bs4 import BeautifulSoup

def scrape_btc_usd_price():
    url = 'https://br.investing.com/crypto/bitcoin/btc-usd'
    scraper = cloudscraper.create_scraper()  # cloudscraper é compatível com Cloudflare
    
    try:
        # Fazendo a requisição para a página do Bitcoin
        page = scraper.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Procurando o elemento que contém o preço de BTC/USD
        price_div = soup.find('div', {'data-test': 'instrument-price-last'})
        if price_div:
            price = price_div.text.strip()
            return price
        else:
            return None
    except Exception as e:
        print(f"Erro ao capturar o preço: {e}")
        return None

@bp.route('/market/btcusd/currentprice', methods=['GET'])
def current_btc_usd_price():
    price = scrape_btc_usd_price()
    
    if price:
        return jsonify({'price': price})
    else:
        return jsonify({'error': 'Price not found'}), 404
