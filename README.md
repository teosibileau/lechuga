# Lechuga

:leaves:

"Lechuga" (lettuce) is a commonly used slang financial term in Argentina to refer to US Dollars.

## Installation

Requirements:

+ A [fixer.io](https://fixer.io/quickstart) free account
+ Python 3.10+

Install with [pipx](https://pipx.pypa.io/) (recommended for CLI tools):

```bash
$ pipx install lechuga
```

Or install with pip:

```bash
$ pip install lechuga
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
➔ lechuga --n 30

  Fecha       USD         EURO 
----------  ----------  ----------
2026-02-09  1416.49     1686.12
2026-02-10  1403.99 📉  1669.19 📉
2026-02-11  1404.38 📈  1667.79 📉
2026-02-12  1397.12 📉  1658.08 📉
2026-02-13  1398.43 📈  1660.04 📈
2026-02-14  1399.25 📈  1661.02 📈
2026-02-15  1399.25 📉  1660.50 📉
2026-02-16  1399.27 📈  1658.06 📉
2026-02-17  1393.48 📉  1651.46 📉
2026-02-18  1396.99 📈  1646.80 📉
2026-02-19  1390.48 📉  1636.41 📉
2026-02-20  1375.17 📉  1621.18 📉
2026-02-21  1375.75 📈  1621.87 📈
2026-02-22  1375.75 📈  1628.07 📈
2026-02-23  1369.25 📉  1614.82 📉
2026-02-24  1379.75 📈  1624.60 📈
2026-02-25  1397.52 📈  1651.14 📈
2026-02-26  1408.49 📈  1662.33 📈
2026-02-27  1393.63 📉  1646.92 📉
2026-02-28  1397.00 📈  1650.90 📈
2026-03-01  1397.00 📉  1642.71 📉
2026-03-02  1394.02 📉  1630.48 📉
2026-03-03  1415.01 📈  1643.03 📈
2026-03-04  1401.52 📉  1630.66 📉
2026-03-05  1407.45 📈  1633.72 📈
2026-03-06  1420.07 📈  1650.19 📈
2026-03-07  1415.50 📉  1644.88 📉
2026-03-08  1415.50 📉  1631.02 📉
2026-03-09  1415.75 📈  1644.61 📈
2026-03-10  1407.56 📉  1636.85 📉
```
