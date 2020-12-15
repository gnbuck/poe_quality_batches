# Poe Quality Batches

## Description

This tool is a Python script to compute the best vendor receipe batches for obtaining items like Gemcutter's Prism or Glassblower's Bauble.

It is able to query the inventory of a character via Path of Exile [official website](https://www.pathofexile.com/) and to tell you how to get the most possible of those currencies. Alternatively and for historical reason, it is able to compute the result via a [hardcoded list](poe_quality_batches/samples.py) of quality values.

I don't know if either your game language or the language on the website affects the item properties the script queries. Please make sure to use English if you encounter any problems.

## Prerequisites

- Git
- Python 3.8
- Make (optionnal)

## Usage

### Clone the project

``` shell
mkdir ~/repos
git clone https://github.com/gnbuck/poe_quality_batches.git
cd ~/repos/poe_quality_batches
```

### Define environement variables

``` shell
export ACCOUNT=<account_name>
export REALM=<platform> # e.g. pc
export LEAGUE=<league>
export CHARACTER=<character_name>
export POESESSID=<poe_session_id>
export OBJECT_TYPE=<object_name>
export STASH_NAME=<stash_to_inspect>
```

- account_name: Your account name
- character_name: The name of the character you want to retreive the inventory
- platform: On which platform your character is. Can be either: pc, ps4 or xbox. CAUTION! Only tested for pc.
- league: The league on which your character is
- poe_session_id: Cookie stored in your browser when you are logged into Path of Exile website
- object_type: The object you want to compute. Can be either: flask or gem.
- stash_name: The name of the stash you want to compute the item qualities

Depending on what variables are assigned and their values, the script will act differently:

| Object Type  | Stash Name           | Result                                                                          |
| :----------: | :------------------: | :-----------------------------------------------------------------------------: |
| Gem          | `Quad Stash`         | Search inside the tab named `Quad Stash` for all quality gems                 |
| Gem          | N/A                  | Search in all tabs each quality gem                                             |
| N/A          | `Glassblower Bauble` | Search inside the tab named `Glassblower Bauble` for all quality gems and flasks        |
| N/A          | N/A                  | Search in all tabs each quality gems and flasks                                 |


### Create environnement

``` shell
make env
```

### Run in online mode

``` shell
make run
```

### Run in offline mode

``` shell
make run-offline
```

## Usage on Windows

I personnaly recommend you to runthe above procedure via WSL (Windows Subsystem for Linux). WSL is a Windows feature to execute a small Linux and it can be installed easily. If your CPU has not the virtualization support, please wait a future release, where all variables will be handled via a local web UI.

## Contributing

If you want to contribute to this project, do not hesitate to open a pull request.

- Create dev environnement

``` shell
make env-dev
```

- Run offline with debug enabled (logs into /out.txt)
``` shell
make run-debug
