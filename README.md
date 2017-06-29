# Lechuga

:leaves:

"Lechuga" (lettuce) is a commonly used slang financial term in Argentina to refer to US Dollars. 

## Installation

Requirements:

+ python 2.7+
+ pip

```bash
$ pip install git+https://github.com/drkloc/lechuga.git
```

## What it does

It retrieves data from a webservice at `lanacion.com.ar` && prints it with pretty colors right to the cli output.

![Demo](lechuga.gif)

## How it works

### Help

```bash
$ lechuga --help                               

Usage: lechuga [OPTIONS]

Options:
  --n INTEGER    How many entries per type
  --save         Save output
  --types TEXT   Type to display (Multiple)
  --json         Save as json
  --output TEXT  Directory to save output to
  --help         Show this message and exit.
```

### Get a number of items per type

```
$ lechuga --n 2

 OFICIAL 

 Fecha         Compra      Venta 
----------  ----------  ---------
2015/12/18       13.75      13.95
2015/12/17       14.5       13.5


 BLUE 

 Fecha         Compra      Venta 
----------  ----------  ---------
2015/12/10       14.7       14.77
2015/12/03       14.66      14.73


 TARJETA 

 Fecha         Compra      Venta 
----------  ----------  ---------
2015/12/18        18.7       18.7
2015/12/17        18.9       18.9


 BOLSA 

 Fecha         Compra      Venta 
----------  ----------  ---------
2015/12/10       14.98      14.98
2015/12/03       14.59      14.59
```

### Get just one type

```bash
$ lechuga --types blue

 BLUE 

 Fecha         Compra      Venta 
----------  ----------  ---------
2015/12/10       14.7       14.77
2015/12/03       14.66      14.73
2015/11/26       14.98      15.04
2015/11/16       15.05      15.1
```

### Save as csv (one file per type)

```bash
$ lechuga --save
$ ls | grep .csv

usd-blue.csv
usd-bolsa.csv
usd-oficial.csv
usd-tarjeta.csv
```

### Save as json

```bash
$ lechuga --save --json
$ ls | grep .json

usd-blue.json
usd-bolsa.json
usd-oficial.json
usd-tarjeta.json
```

### Save to a specific path

```
$ lechuga --save --output ~/Desktop
$ ls ~/Desktop | grep .csv

usd-blue.csv
usd-bolsa.csv
usd-oficial.csv
usd-tarjeta.csv
```

### Combine

```bash
$ lechuga --types oficial --n 40
$ lechuga --save --types blue
$ lechuga --save --types oficial --path ~/Desktop --json
```
