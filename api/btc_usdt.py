from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import cloudscraper

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Rota para membros
@app.route('/members')
def members():
    return jsonify({'members': ['member1', 'member2', 'member34']})

# Rota para hora atual
@app.route('/hora')
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return jsonify({'hora': current_time})

# Função para fazer o web scraping e coletar os dados da tabela
def scrape_economic_events():
    url = 'https://br.investing.com/economic-calendar/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    events = []
    table = soup.find('table', id='economicCalendarData')
    rows = table.find_all('tr', class_='js-event-item')

    for row in rows:
        hora = row.find('td', class_='js-time').text.strip()
        moeda = row.find('td', class_='flagCur').text.strip()
        importancia = row.find('td', class_='sentiment').get('title')
        evento = row.find('td', class_='event').text.strip()
        atual = row.find('td', class_='act').text.strip()
        projecao = row.find('td', class_='fore').text.strip()
        anterior = row.find('td', class_='prev').text.strip()

        events.append({
            'hora': hora,
            'moeda': moeda,
            'importancia': importancia,
            'evento': evento,
            'atual': atual,
            'projecao': projecao,
            'anterior': anterior
        })
    
    return events

# Rota para obter todos os eventos
@app.route('/events', methods=['GET'])
def get_events():
    events = scrape_economic_events()
    return jsonify(events)

# Rota para filtrar eventos por moeda
@app.route('/events/<currency>', methods=['GET'])
def get_events_by_currency(currency):
    events = scrape_economic_events()
    filtered_events = [event for event in events if event['moeda'] == currency.upper()]
    return jsonify(filtered_events)

# Função para fazer o scraping do preço de BTC/USD
def scrape_btc_usd_price():
    url = 'https://br.investing.com/crypto/bitcoin/btc-usd'
    scraper = cloudscraper.create_scraper()  # cloudscraper é compatível com Cloudflare
    
    try:
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

# Rota para obter o preço atual do BTC/USD
@app.route('/market/btcusd/currentprice', methods=['GET'])
def current_btc_usd_price():
    price = scrape_btc_usd_price()
    
    if price:
        return jsonify({'price': price})
    else:
        return jsonify({'error': 'Price not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
