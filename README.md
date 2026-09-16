[![CI](https://github.com/TynK-M/sdb/actions/workflows/checks.yml/badge.svg)](https://github.com/TynK-M/sdb/actions/workflows/checks.yml)

# sdb

A small command-line tool for exporting [seriousdb](https://github.com/danieldeer/seriousdb) databases to common formats.

`sdb` is intentionally separate from `seriousdb`. It reads an existing `sdb` database file and produces an export file without modifying the original database.

## Features

* Export `seriousdb` databases from the command line.
* Export to:
  * PostgreSQL SQL
  * MySQL SQL
  * SQLite SQL
  * JSON
  * CSV
* Custom output paths.
* Custom table names for SQL exports.
* Dry-run mode to inspect an export without writing a file.

## Requirements

* Python 3.11 or newer.

## Installation

Clone the repository and install it with `uv`:

```bash
git clone https://github.com/your-username/sdb.git
cd sdb

uv sync
```

The `sdb` command is then available through `uv`:

```bash
uv run sdb --help
```

## Usage

The basic syntax is:

```bash
sdb <database_file_path> --format <format>
```

For example:

```bash
uv run sdb database.sdb --format postgresql
```

By default, the output is written to the `dump/` directory:

```text
dump/
└── database.sql
```

### Specify an output file

Use `--output` to choose the output path:

```bash
uv run sdb database.json \
    --format postgresql \
    --output dump/database.sql
```

### Specify a table name

SQL exporters use `seriousdb_kv` by default.

You can change the table name with `--table`:

```bash
uv run sdb database.json \
    --format postgresql \
    --table users
```

The table name is safely quoted by the SQL exporter.

### Dry run

Use `--dry-run` to see what would be exported without creating an output file:

```bash
uv run sdb database.json \
    --format json \
    --dry-run
```

Example output:

```text
Would export 42 entries to dump/database.json
```

## Export formats

### PostgreSQL

```bash
uv run sdb database.json --format postgresql
```

`pg` is also accepted as an alias:

```bash
uv run sdb database.json --format pg
```

The generated SQL creates the table if necessary and uses an upsert for each key.

### MySQL

```bash
uv run sdb database.json --format mysql
```

The generated SQL creates the table if necessary and uses MySQL's duplicate-key update behavior.

### SQLite

```bash
uv run sdb database.json --format sqlite
```

The generated SQL creates the table if necessary and replaces existing rows with matching keys.

### JSON

```bash
uv run sdb database.json --format json
```

The resulting file contains the key-value database as a JSON object.

### CSV

```bash
uv run sdb database.json --format csv
```

The resulting file contains two columns:

```text
key,value
foo,bar
hello,world
```

## Security

SQL exports quote identifiers and escape string values before placing them in generated SQL.

Database contents are treated as data. They are not interpreted as SQL commands.

`sdb` does not connect to or execute queries against a database server. The SQL exporters only generate SQL files.

## Development

Install the development dependencies:

```bash
uv sync --dev
```

Run the formatter:

```bash
uv run ruff format .
```

Check formatting:

```bash
uv run ruff format --check .
```

Run the linter:

```bash
uv run ruff check .
```

Run the type checker:

```bash
uv run ty check .
```

Run the tests:

```bash
uv run pytest
```

## Scope

`sdb` is intentionally focused on **exporting** `seriousdb` databases.

It does not provide a replacement database implementation, modify the source database, or require a running `seriousdb` server.

The input is the sdb database file produced by `seriousdb`, and the output is a standalone export file.

## License

See the [MIT License](LICENSE) for details.
