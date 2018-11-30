# Lechuga

:leaves:

"Lechuga" (lettuce) is a commonly used slang financial term in Argentina to refer to US Dollars.

## Installation

Requirements:

+ A [fixer.io](https://fixer.io/quickstart) free account
+ python 3.6+
+ pip

```bash
$ pip install git+https://github.com/drkloc/lechuga.git
```

Setup an environment variable with the Fixer IO API access key:

```
export FIXERIOKEY=YOUR_API_KEY
```

## What it does

It retrieves data from the `fixer.io` API && prints it using pretty colors right to the cli output.


## How it works

### Help

```bash
$ lechuga --help

Usage: lechuga.py [OPTIONS]

Options:
  --n INTEGER  How far in the past should we go?
  --help       Show this message and exit.
```

### Get latest n rates

```bash
➔ lechuga --n 20

 Fecha         USD      EURO 
----------  -------  --------
2018-11-11    35.42     40.1
2018-11-12    35.54     39.92
2018-11-13    36.01     40.73
2018-11-14    35.89     40.6
2018-11-15    36.04     40.82
2018-11-16    35.92     41.02
2018-11-17    35.76     40.84
2018-11-18    35.78     40.84
2018-11-19    35.91     41.13
2018-11-20    36.18     41.14
2018-11-21    36.27     41.3
2018-11-22    36.43     41.54
2018-11-23    37.56     42.61
2018-11-24    37.56     42.61
2018-11-25    37.58     42.61
2018-11-26    39.08     44.29
2018-11-27    38.54     43.55
2018-11-28    38.45     43.71
2018-11-29    37.73     42.98
2018-11-30    37.73     42.67
```
