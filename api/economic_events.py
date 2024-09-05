from flask import Blueprint, jsonify
import requests
from bs4 import BeautifulSoup

bp = Blueprint('economic_events', __name__)

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
@bp.route('/events', methods=['GET'])
def get_events():
    events = scrape_economic_events()
    return jsonify(events)

@bp.route('/events/<currency>', methods=['GET'])
def get_events_by_currency(currency):
    events = scrape_economic_events()
    filtered_events = [event for event in events if event['moeda'] == currency.upper()]
    return jsonify(filtered_events)
