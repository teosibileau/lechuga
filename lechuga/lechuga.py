from datetime import datetime
import simplejson as json
import re, os, copy, csv
import requests, requests_cache
from colorama import init, Fore, Back, Style
from tabulate import tabulate

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))

init(autoreset=True)
requests_cache.install_cache('%s/lechuga' % SCRIPT_ROOT, backend='sqlite', expire_after=60)

class Lechuga:
  def __init__(self):
    self.refresh()

  def refresh(self):
    # Request data and remove first item.
    r = requests.get(
      'http://olcreativa.lanacion.com.ar/dev/get_url/?key=0AuNh4LTzbqXMdFJobGlLMWl2bzR3SHM3Nmc1dExLZmc'
    )
    r = r.json()
    r.pop(0)
    # Make it pretty
    self.p = [
      {
        'date': Lechuga.fix_date(i[0]),
        'type': Lechuga.replace_type(i[1].lower().strip()),
        'sell': float(i[2].replace(',', '.')),
        'buy': float(i[3].replace(',', '.'))
      }
      for i in r if i[0] != '' and i[3] != ''
    ]
    self.types = [i['type'] for i in self.p]
    self.types.append('tarjeta')
    self.types = set(self.types)
    # Guess tarjeta from oficial
    tarjeta = [i for i in self.p if i['type'] == 'oficial']
    tarjeta = copy.deepcopy(tarjeta)
    for i in range(len(tarjeta)):
      tarjeta[i]['type'] = 'tarjeta'
      b = tarjeta[i]['buy']
      s = tarjeta[i]['sell']
      tarjeta[i]['sell'] = tarjeta[i]['buy'] = (b + (s - b) /2) * 1.35
    self.p = self.p + tarjeta

  @classmethod
  def replace_type(cls, t):
    d = {
      'casas de cambio': 'oficial',
      'informal': 'blue',
      'inforrmal': 'blue',
    }
    if t in d.keys():
      t = d[t]
    return t

  @classmethod
  def fix_date(cls, month):    
    # Create a dictionary of regex for replacemants over dates.
    rep = {'ene': '1', 'feb': '2', 'mar': '3', 'abr': '4', 'may': '5',
           'jun': '6', 'jul': '7', 'ago': '8', 'sept': '9', 'oct': '10',
           'nov': '11', 'dic': '12', '.': '', '-': '/'}
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile('|'.join(rep.keys()))
    r = pattern.sub(lambda m: rep[re.escape(m.group(0))], month)
    r = r.split('/')
    r = ["%02d" % int(i) for i in r]
    r = '/'.join(r)
    r = datetime.strptime(r, '%d/%m/%Y').strftime('%Y/%m/%d')
    return r

  def validate_types(self, types=[]):
    types = [t for t in types if t in self.types]
    if not len(types):
      types = self.types
    return types

  def filter_type(self, t):
    return [i for i in self.p if i['type'] == t]

  def print_it(self, n=False, types=[]):
    if not n:
      n = 4
    types = self.validate_types(types)
    for t in types:
      s = self.filter_type(t)
      print
      print(Back.GREEN + Fore.BLACK + ' ' + t.upper() + ' ' + Style.RESET_ALL)
      print
      h = [
        Back.YELLOW + Fore.BLACK + ' Fecha ' + Style.RESET_ALL,
        Back.RED + Fore.WHITE + ' Compra ' + Style.RESET_ALL,
        Back.BLUE + Fore.WHITE + ' Venta ' + Style.RESET_ALL, 
      ]
      o = [[i['date'], "%.2f" % i['buy'], "%.2f" % i['sell']] for i in reversed(s[-n:])]
      print tabulate(o, headers=h)
      print

  def save_as_json(self, data_folder=False, types=[], n=False):
    if not data_folder:
      data_folder = os.getcwd()
    if os.path.isdir(data_folder):
      types = self.validate_types(types)
      for t in types:
        s = self.filter_type(t)
        if n:
          s = s[-n:]
        f = os.path.join(data_folder, 'usd-%s.json' % t)
        with open(f, 'w') as jsonfile:
          json.dump(s, jsonfile, indent=2)

  def save_as_csv(self, data_folder=False, types=[], n=False):
    if not data_folder:
      data_folder = os.getcwd()
    if os.path.isdir(data_folder):
      types = self.validate_types(types)
      for t in types:
        h = ['Fecha', 'Compra', ' Venta ']
        s = self.filter_type(t)
        if n:
          s = [s[-n:]]
        s = [[i['date'], "%.2f" % i['buy'], "%.2f" % i['sell']] for i in s]
        f = os.path.join(data_folder, 'usd-%s.csv' % t)
        with open(f, 'w') as csvfile:
          w = csv.writer(csvfile)
          w.writerow(h)
          for r in s:
            w.writerow(r)


import click
@click.command()
@click.option('--n', default=4, help='How many entries per type')
@click.option('--save', is_flag=True, default=False, help='Save output')
@click.option('--types', default=[], multiple=True, help='Type to display (Multiple)')
@click.option('--json', is_flag=True, default=False, help='Save as json')
@click.option('--output', default=False, help='Directory to save output to')
def run(n, save, types, json, output):
  l = Lechuga()
  if not save:
    l.print_it(n, types)
  elif not json:
    l.save_as_csv(output, types)
  else:
    l.save_as_json(output, types)

if __name__ == '__main__':
  run()
