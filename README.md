# lastfm-backup-cli
Super-simple CLI tool for backing up Last.fm scrobbling data into CSV file

### installation
- pre-requisites: Python 3.7 or newer, pip
- installation: `pip install --user lastfm-backup-cli`
  - or, if your default Python is 2.x: `python3 -m pip install --user lastfm-backup-cli`

### usage
- get your LastFM API key [here](https://www.last.fm/api)
- run: `lastfm-backup <PATH TO BACKUP CSV FILE> --user <YOUR LASTFM USERNAME> --api-key <YOUR API KEY> --time-from <DATE OF FIRST SCROBBLE IN BACKUP FILE> --time-to <DATE OF LAST SCROBBLE IN BACKUP FILE>`
  - example: `lastfm-backup lastfm-backup-2021-01.csv --user Rezult --api-key <YOUR API KEY> --time-from 2021-01-01 --time-to 2021-02-01`
- you can also set env variables: `LASTFM_API_KEY` and `LASTFM_USER`

### output
- output CSV file structure is:
```csv
<SCROBBLE DATE>,<SCROBBLE TIME (UTC)>,<ARTIST>,<TITLE>
...
```
- output CSV example:
```csv
2021-05-26,06:05:49,Alice Coltrane,Journey in Satchidananda
2021-05-25,14:16:08,London Music Works,"S.T.A.Y. (From ""Interstellar"")"
2021-05-25,13:18:39,Pantha du Prince,Silentium Larix
2021-05-25,13:11:10,Avenade,Have It Your Way
2021-05-25,13:03:51,Four Tet,Planet
2021-05-25,12:57:58,Songs: Ohia,Steve Albini's Blues
2021-05-25,12:52:31,Andy Stott,It Should Be Us
```

### options
```
usage: lastfm-backup [-h] [--user USER] [--api-key API_KEY] [--time-from TIME_FROM] [--time-to TIME_TO] [-d] file

Super-simple CLI tool for backing up Last.fm scrobbling data

positional arguments:
  file                  CSV file path where backup should be written to. Defaults to lastfm.csv

optional arguments:
  -h, --help            show this help message and exit
  --user USER           The last.fm username to fetch the recent tracks of.Might be provided by env variable LASTFM_USER
  --api_key API_KEY     A Last.fm API key. Might be provided by env variable LASTFM_API_KEY
  --time-from TIME_FROM
                        Beginning timestamp of a range - only display scrobbles after this time. Must be in UTC. Example: 2021-05-13
  --time-to TIME_TO     End timestamp of a range - only display scrobbles before this time. Must be in UTC. Example: 2021-05-15
  -d, --debug           Enable more verbose logging
```
