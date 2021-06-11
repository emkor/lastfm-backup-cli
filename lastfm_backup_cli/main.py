import argparse
import logging
import os
import sys
from enum import Enum
import typing as t
import pylast
import itertools
import csv
from datetime import datetime as dt, timezone as tz

DEFAULT_CSV_FILE = "lastfm.csv"
ACCEPTED_DT_FMT = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M.%S",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M.%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%d",
)


class EnvVar(Enum):
    USER = "LASTFM_USER"
    API_KEY = "LASTFM_API_KEY"

    @classmethod
    def get(cls, var: "EnvVar") -> t.Optional[str]:
        return os.getenv(var.value)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Super-simple CLI tool for backing up Last.fm scrobbling data")
    parser.add_argument(
        "file",
        type=str,
        default=DEFAULT_CSV_FILE,
        help=f"CSV file path where backup should be written to. Defaults to {DEFAULT_CSV_FILE}",
    )
    parser.add_argument(
        "--user",
        type=str,
        help=f"The last.fm username to fetch the recent tracks of."
        f"Might be provided by env variable {EnvVar.USER.value}",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help=f"A Last.fm API key. Might be provided by env variable {EnvVar.API_KEY.value}",
    )
    parser.add_argument(
        "--time-from",
        type=str,
        default=None,
        help="Beginning timestamp of a range - only download scrobbles after this time. "
        "Must be in UTC. Example: 2021-05-13",
    )
    parser.add_argument(
        "--time-to",
        type=str,
        default=None,
        help="End timestamp of a range - only download scrobbles before this time. "
        "Must be in UTC. Example: 2021-05-15",
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Enable more verbose logging")
    return parser.parse_args()


def _parse_dt_into_timestamp(dt_str: str) -> t.Optional[float]:
    for fmt in ACCEPTED_DT_FMT:
        try:
            dt_val = dt.strptime(dt_str, fmt).replace(tzinfo=tz.utc)
            return int(dt_val.timestamp())
        except ValueError:
            continue
    return None


def _chunks(n: int, iterable: t.Iterable) -> t.Generator[t.Any, None, None]:
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def _to_csv_row(
    played_track: pylast.PlayedTrack,
) -> t.Optional[t.Tuple[str, str, str, str]]:
    try:
        scrobble_dt = dt.fromtimestamp(int(played_track.timestamp), tz=tz.utc)
        return (
            scrobble_dt.date().isoformat(),
            scrobble_dt.time().isoformat(),
            played_track.track.artist,
            played_track.track.title,
        )
    except (TypeError, ValueError):
        logging.warning(f"Could not parse track {played_track} as CSV row")
        return None


def cli_main():
    args = _parse_args()
    logging.basicConfig(
        format="%(asctime)s|%(levelname)s|%(message)s",
        level=logging.DEBUG if args.debug else logging.INFO,
    )
    target_file = os.path.abspath(os.path.expanduser(args.file))

    if os.path.isfile(target_file):
        logging.warning(f"Given output file {target_file} already exists!")
        sys.exit(1)

    timestamp_from = _parse_dt_into_timestamp(args.time_from) if args.time_from else None
    timestamp_to = _parse_dt_into_timestamp(args.time_to) if args.time_to else None

    network = pylast.LastFMNetwork(
        api_key=args.api_key or EnvVar.get(EnvVar.API_KEY),
        username=args.user or EnvVar.get(EnvVar.USER),
    )

    recent_tracks_gen = pylast.User(network.username, network).get_recent_tracks(
        stream=True, limit=None, time_from=timestamp_from, time_to=timestamp_to
    )
    logging.info(
        f"Backing up scrobbles for user {network.username} with "
        f"time range {args.time_from} ({timestamp_from}) - {args.time_to} ({timestamp_to}) "
        f"into {target_file}..."
    )
    for played_tracks_chunk in _chunks(n=50, iterable=recent_tracks_gen):
        with open(target_file, "a") as csv_:
            writer = csv.writer(csv_, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for played_track in played_tracks_chunk:
                logging.debug(f"Writing track played at {played_track.timestamp}: {played_track.track}")
                row = _to_csv_row(played_track)
                if row:
                    writer.writerow(row)
        logging.info(f"Written {len(played_tracks_chunk)} tracks into {target_file} file")


if __name__ == "__main__":
    cli_main()
