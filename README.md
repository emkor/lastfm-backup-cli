# lastfm-backup-cli
Super-simple CLI tool for backing up Last.fm scrobbling data into CSV file

### installation
- pre-requisites: Python 3.7 or newer, pip
- `pip install --user lastfm-backup-cli`
    - or `python3 -m pip install --user lastfm-backup-cli` if your default Python is 2.x

### usage
- get your LastFM API key [here](https://www.last.fm/api)
- run `lastfm-backup <PATH TO BACKUP CSV FILE> --user <YOUR LASTFM USERNAME> --api-key <YOUR API KEY> --time-from <DATE OF FIRST SCROBBLE IN BACKUP FILE> --time-to <DATE OF LAST SCROBBLE IN BACKUP FILE>`
    - example: `lastfm-backup lastfm-backup-2021-01.csv --user Rezult --api-key <YOUR API KEY> --time-from 2021-01-01 --time-to 2021-01-02`

- output structure is:
```csv
<SCROBBLE DATE>,<SCROBBLE TIME (UTC)>,<ARTIST>,<TITLE>
...
```
- output example:
```csv
2021-04-01,10:42:53,PRO8L3M,Backstage
2021-04-01,10:39:59,PRO8L3M,Byłem tam
2021-04-01,10:34:52,Deftones,Pompeji
2021-04-01,10:30:14,Deftones,This Link Is Dead
2021-04-01,10:26:38,Deftones,Radiant City
2021-04-01,10:21:48,Deftones,Error
2021-04-01,10:17:37,Deftones,Ohms
2021-04-01,10:13:08,The Avalanches,Gold Sky
2021-04-01,10:10:49,The Avalanches,Oh the Sunn!
2021-04-01,10:07:18,The Avalanches,Overcome
2021-04-01,10:03:56,The Avalanches,Music Makes Me High
2021-04-01,09:59:34,The Avalanches,Reflecting Light
2021-04-01,09:53:43,The Avalanches,Wherever You Go
```
