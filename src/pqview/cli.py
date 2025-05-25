import sys
from pprint import pprint
from typing import Annotated

import polars as pl
import typer

app = typer.Typer(help="View Parquet file contents using Polars.")

cfg_default = pl.Config(
    tbl_formatting="UTF8_FULL_CONDENSED",
    tbl_width_chars=-1,
    apply_on_context_enter=True,
)

cfg_allcols = pl.Config(
    tbl_formatting="UTF8_FULL_CONDENSED",
    tbl_cols=-1,
    tbl_width_chars=-1,
    apply_on_context_enter=True,
)

cfg_all = pl.Config(
    tbl_formatting="UTF8_FULL_CONDENSED",
    tbl_cols=-1,
    tbl_rows=-1,
    tbl_width_chars=-1,
    fmt_str_lengths=300,  # this is the max chars to display for a string column
    apply_on_context_enter=True,
)


@app.command()
def show(
    file: str,
    nrows: Annotated[int, typer.Option(help="Number of rows to show")] = 10,
    ncols: Annotated[int, typer.Option(help="Number of cols to show")] = 8,
    all: Annotated[bool, typer.Option(help="Show all rows")] = False,
):
    """Show first and last n/2 rows of the Parquet file.

    This is the default command if no command is specified."""
    lf = pl.scan_parquet(file)
    pl.Config.set_tbl_rows(nrows).set_tbl_cols(ncols)
    with cfg_all if all else cfg_default:
        print(lf.collect())


@app.command()
def schema(file: str) -> None:
    """Display schema of the Parquet file.

    Dictionary of column names and data types."""
    pprint(pl.read_parquet_schema(file))


@app.command()
def height(file: str) -> None:
    """Show number of records/rows in the Parquet file."""
    lf = pl.scan_parquet(file)
    print(lf.select(pl.len()).collect().item())


@app.command()
def glimpse(file: str) -> None:
    """Return a dense preview of the DataFrame.

    The formatting shows one line per column so that wide dataframes display cleanly.
    Each line shows the column name, the data type, and the first few values."""
    lf = pl.scan_parquet(file)
    lf.collect().glimpse()


@app.command()
def head(
    file: str,
    nrows: Annotated[int, typer.Option(help="Number of rows to show")] = 5,
    ncols: Annotated[int, typer.Option(help="Number of cols to show")] = 8,
    all: Annotated[bool, typer.Option(help="Show all cols")] = False,
) -> None:
    """Show first N rows of the Parquet file."""
    lf = pl.scan_parquet(file)
    pl.Config.set_tbl_cols(ncols)
    with cfg_allcols if all else cfg_default:
        print(lf.head(nrows).collect())


@app.command()
def tail(
    file: str,
    nrows: Annotated[int, typer.Option(help="Number of rows to show")] = 5,
    ncols: Annotated[int, typer.Option(help="Number of cols to show")] = 8,
    all: Annotated[bool, typer.Option(help="Show all cols")] = False,
) -> None:
    """Show last N rows of the Parquet file."""
    lf = pl.scan_parquet(file)
    pl.Config.set_tbl_cols(ncols)
    with cfg_allcols if all else cfg_default:
        print(lf.tail(nrows).collect())


@app.command()
def sql(
    file: str,
    query: Annotated[
        str, typer.Option(help="SQL query to run against the Parquet file")
    ],
    nrows: Annotated[int, typer.Option(help="Number of rows to show")] = 10,
    ncols: Annotated[int, typer.Option(help="Number of cols to show")] = 8,
    all: Annotated[bool, typer.Option(help="Show all rows")] = False,
):
    """
    Show the results of an SQL query against the Parquet file.

    For example, to show the Id, sex, age and Fare paid of those who
    survived the Titanic sinking, use:

    pqview sql --query "select PassengerId,Sex,Age,Fare from self where Survived=1" ~/titanic.parquet"""
    lf = pl.scan_parquet(file)
    pl.Config.set_tbl_rows(nrows).set_tbl_cols(ncols)
    with cfg_all if all else cfg_default:
        print(lf.sql(query).collect())


@app.command()
def csv(file: str, separator: str = "\t", header: bool = True) -> None:
    """Return contents of the Parquet file in CSV format.

    Optionally specify a separator other than Tab and whether to include the header."""
    lf = pl.scan_parquet(file)
    lf.sink_csv(sys.stdout, separator=separator, include_header=header)


def main():
    """Main function to run the CLI."""
    # detect if no "valid" command has been specified and default to 'show'
    from typer.main import get_command, get_command_name

    if (
        len(sys.argv) > 1
        and sys.argv[1]
        not in [get_command_name(key) for key in get_command(app).commands.keys()]
        and sys.argv[1]
        not in ["-h", "--help", "--show-completion", "--install-completion"]
    ):
        sys.argv.insert(1, "show")

    app()


if __name__ == "__main__":
    app()
