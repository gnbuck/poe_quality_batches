# Poe Quality Batches

## Description

This tool is a Python script to compute the best vendor receipe batches for obtaining items like Gemcutter's Prism or Glassblower's Bauble.

It is able to query the inventory of a character via Path Of Exile [official website](https://www.pathofexile.com/) and to tell you how to get the most possible of those currencies. Alternatively and for historical reason, it is able to compute the result via a [hardcoded list](poe_quality_batches/samples.py) of quality values

## Prerequisites

- Python 3.8
- Make

## Usage

- Create environnement

``` shell
make env
```

- Run in online mode

``` shell
make run
```

- Run in offline mode

``` shell
make run-offline
```

## Contributing

If you want to contribute to this project, do not hesitate to open a pull request.

- Create dev environnement

``` shell
make env-dev
```

- Run offline with debug enabled (logs into /out.txt)
``` shell
make run-debug
