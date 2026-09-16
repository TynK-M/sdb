"""Command-line interface for sdb."""

import argparse
from pathlib import Path

from sdb import exporters
from sdb.reader import load

EXPORTERS = {
    "postgresql": exporters.postgresql.export,
    "pg": exporters.postgresql.export,
    "mysql": exporters.mysql.export,
    "sqlite": exporters.sqlite.export,
    "json": exporters.json.export,
    "csv": exporters.csv.export,
}

SQL_EXPORTERS = {
    "postgresql",
    "pg",
    "mysql",
    "sqlite",
}


def main() -> None:
    """Parse arguments and export a seriousdb database."""
    parser = argparse.ArgumentParser(description="Export a seriousdb database.")

    parser.add_argument(
        "database",
        help="Path to the seriousdb database file.",
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=EXPORTERS,
        required=True,
        help="Export format.",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file.",
    )

    parser.add_argument(
        "--table",
        default="seriousdb_kv",
        help="Table name for SQL exports.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be exported without writing a file.",
    )

    args = parser.parse_args()

    db = load(args.database)
    exporter = EXPORTERS[args.format]

    if args.output:
        output = Path(args.output)
    else:
        database_name = Path(args.database).stem
        extension = "sql" if args.format in SQL_EXPORTERS else args.format
        output = Path("dump") / f"{database_name}.{extension}"

    if args.dry_run:
        print(f"Would export {len(db)} entries to {output}")
        return

    output.parent.mkdir(parents=True, exist_ok=True)

    exporter(
        db,
        output,
        table_name=args.table,
    )

    print(f"Exported {len(db)} entries to {output}")


if __name__ == "__main__":
    main()
