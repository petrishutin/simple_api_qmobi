import re
import logging
from urllib import request
from urllib.error import HTTPError, URLError


def get_exchange_rates() -> dict:
    url = 'http://cbr.ru'
    error = {'error': f'Rates are temporary unavailable. Call for it later'}
    try:
        response = request.urlopen(url)
    except HTTPError as e:
        logging.info(f"An error occurred while calling {url}. Error: {e}")
        return error
    except URLError as e:
        logging.info(f"An error occurred while calling {url}. Error: {e}")
        return error
    if response.status != 200:
        logging.info(f"An error occurred while calling {url}")
        return error
    html = response.read().decode()
    dates = re.findall(
        '(?is)<div class="col-md-2 col-xs-7 _right"[^>]*>(.+?)</div>',
        html
    )
    try:
        dates = [
            re.findall('(?is)<a[^>]*>(.+?)</a>', date)[0] for date in dates
        ]
    except IndexError as e:
        logging.info(f"Can not parse dates from payload. Error: {e}")
        return error
    data = re.findall(
        '(?is)<div class="col-md-2 col-xs-9 _right mono-num"[^>]*>(.+?)</div>',
        html
    )
    if len(data) != 4:
        logging.info(f"Can not parse dates from payload. Error: {e}")
        return error
    data = [float(i.replace(',', '.')[:7]) for i in data]
    return {'exchange_rates': {
        dates[0]: {'USD/RUR': data[0], 'EUR/RUR': data[2]},
        dates[1]: {'USD/RUR': data[1], 'EUR/RUR': data[3]},
    }
    }
