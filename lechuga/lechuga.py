from datetime import datetime, timedelta
import simplejson as json
import re, os, copy, csv, logging
import requests, requests_cache
from colorama import init, Fore, Back, Style
from tabulate import tabulate

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))

init(autoreset=True)
requests_cache.install_cache('%s/lechuga' % SCRIPT_ROOT, backend='sqlite', expire_after=60)

class Lechuga:
  def __init__(self, depth=1):
    self.api_key = os.environ.get('FIXERIOKEY', False)
    if not self.api_key:
      raise Exception('Please set the FIXERIOKEY environ variable')
    self.depth = depth
    self.p = []
    self.refresh()

  def refresh(self):
    # Request data and remove first item.
    API = 'http://data.fixer.io/api/%s?access_key=%s&format=1&symbols=USD,ARS'
    last = False
    while(self.depth):
      uri = API % (
        'latest' if not last else last.strftime('%Y-%m-%d'),
        self.api_key
      )
      r = requests.get(uri)
      r = r.json()
      self.p.append({
        'date': r['date'],
        'usd': r['rates']['ARS'] / r['rates']['USD'],
        'euro': r['rates']['ARS'],
        }
      )
      last = datetime.strptime(r['date'], '%Y-%m-%d') - timedelta(days=1)
      self.depth -= 1

  def print_it(self):
    print('')
    h = [
      Back.YELLOW + Fore.BLACK + ' Fecha ' + Style.RESET_ALL,
      Back.GREEN + Fore.WHITE + ' USD ' + Style.RESET_ALL,
      Back.BLUE + Fore.WHITE + ' EURO ' + Style.RESET_ALL,
    ]
    o = [[i['date'], "%.2f" % i['usd'], "%.2f" % i['euro']] for i in reversed(self.p)]
    print(tabulate(o, headers=h))
    print('')


import click
@click.command()
@click.option('--n', default=4, help='How far in the past should we go?')
def run(n):
  l = Lechuga(n)
  l.print_it()

if __name__ == '__main__':
  logging.captureWarnings(True)
  run()
