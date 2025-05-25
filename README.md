# pqview

`pqview` is a Python package for viewing the contents of Parquet files from the Linux command line.
`pqview` uses the Polars package to read and query parquet files.

## Features

- Display some or all of the contents of a parquet file in table format
- Show the number of records or schema of a parquet file
- Run SQL queries against the parquet file and view results
- Format the contents of a parquet as CSV

## Installation

```bash
uv pip install pqview  # install in virtual environment
uv tool install pqview  # install as tool available globally
```

## Usage

### Example commands:
```bash
pqview ~/titanic.parquet  # displays parquet file contents as a table using default max nrows & ncols
pqview show ~/titanic.parquet  # `show` is the default command, so doesn't need to be specified
pqview --all ~/titanic.parquet |less -S  # pipes all parquet file contents to `less -S`
pqview --ncols 10 ~/titanic.parquet  # displays parquet file contents as a table, showing a maximum of 10 columns
pqview --ncols -1 ~/titanic.parquet  # displays parquet file contents as a table, showing all columns
pqview height ~/titanic.parquet  # displays the number of records/rows in the parquet file
pqview schema ~/titanic.parquet  # displays the schema (column names & data types) of the parquet file
pqview glimpse ~/titanic.parquet  # displays a dense preview of the parquet file contents
pqview head ~/titanic.parquet  # displays 1st N rows of parquet file contents as a table
pqview tail ~/titanic.parquet  # displays last N rows of parquet file contents as a table
pqview csv --separator , --header ~/titanic.parquet > ~/titanic.csv  # formats contents of parquet as CSV and prints to stdout
pqview sql --query "select PassengerId,Sex,Age,Fare from self where Survived=1" ~/titanic.parquet
```

### Example Usage:

```bash
pqview ~/titanic.parquet
```
```
shape: (891, 12)
┌─────────────┬──────────┬────────┬─────────────────────────────────┬───┬──────────────────┬─────────┬───────┬──────────┐
│ PassengerId ┆ Survived ┆ Pclass ┆ Name                            ┆ … ┆ Ticket           ┆ Fare    ┆ Cabin ┆ Embarked │
│ ---         ┆ ---      ┆ ---    ┆ ---                             ┆   ┆ ---              ┆ ---     ┆ ---   ┆ ---      │
│ i64         ┆ i64      ┆ i64    ┆ str                             ┆   ┆ str              ┆ f64     ┆ str   ┆ str      │
╞═════════════╪══════════╪════════╪═════════════════════════════════╪═══╪══════════════════╪═════════╪═══════╪══════════╡
│ 1           ┆ 0        ┆ 3      ┆ Braund, Mr. Owen Harris         ┆ … ┆ A/5 21171        ┆ 7.25    ┆ null  ┆ S        │
│ 2           ┆ 1        ┆ 1      ┆ Cumings, Mrs. John Bradley (Fl… ┆ … ┆ PC 17599         ┆ 71.2833 ┆ C85   ┆ C        │
│ 3           ┆ 1        ┆ 3      ┆ Heikkinen, Miss. Laina          ┆ … ┆ STON/O2. 3101282 ┆ 7.925   ┆ null  ┆ S        │
│ 4           ┆ 1        ┆ 1      ┆ Futrelle, Mrs. Jacques Heath (… ┆ … ┆ 113803           ┆ 53.1    ┆ C123  ┆ S        │
│ 5           ┆ 0        ┆ 3      ┆ Allen, Mr. William Henry        ┆ … ┆ 373450           ┆ 8.05    ┆ null  ┆ S        │
│ …           ┆ …        ┆ …      ┆ …                               ┆ … ┆ …                ┆ …       ┆ …     ┆ …        │
│ 887         ┆ 0        ┆ 2      ┆ Montvila, Rev. Juozas           ┆ … ┆ 211536           ┆ 13.0    ┆ null  ┆ S        │
│ 888         ┆ 1        ┆ 1      ┆ Graham, Miss. Margaret Edith    ┆ … ┆ 112053           ┆ 30.0    ┆ B42   ┆ S        │
│ 889         ┆ 0        ┆ 3      ┆ Johnston, Miss. Catherine Hele… ┆ … ┆ W./C. 6607       ┆ 23.45   ┆ null  ┆ S        │
│ 890         ┆ 1        ┆ 1      ┆ Behr, Mr. Karl Howell           ┆ … ┆ 111369           ┆ 30.0    ┆ C148  ┆ C        │
│ 891         ┆ 0        ┆ 3      ┆ Dooley, Mr. Patrick             ┆ … ┆ 370376           ┆ 7.75    ┆ null  ┆ Q        │
└─────────────┴──────────┴────────┴─────────────────────────────────┴───┴──────────────────┴─────────┴───────┴──────────┘
```

```bash
pqview glimpse ~/titanic.parquet
```
```
Rows: 891
Columns: 12
$ PassengerId <i64> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
$ Survived    <i64> 0, 1, 1, 1, 0, 0, 0, 0, 1, 1
$ Pclass      <i64> 3, 1, 3, 1, 3, 3, 1, 3, 3, 2
$ Name        <str> 'Braund, Mr. Owen Harris', 'Cumings, Mrs. John Bradley (Florence Briggs Thayer)', 'Heikkinen, Miss. Laina', 'Futrelle, Mrs. Jacques Heath (Lily May Peel)', 'Allen, Mr. William Henry', 'Moran, Mr. James', 'McCarthy, Mr. Timothy J', 'Palsson, Master. Gosta Leonard', 'Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)', 'Nasser, Mrs. Nicholas (Adele Achem)'
$ Sex         <str> 'male', 'female', 'female', 'female', 'male', 'male', 'male', 'male', 'female', 'female'
$ Age         <f64> 22.0, 38.0, 26.0, 35.0, 35.0, None, 54.0, 2.0, 27.0, 14.0
$ SibSp       <i64> 1, 1, 0, 1, 0, 0, 0, 3, 0, 1
$ Parch       <i64> 0, 0, 0, 0, 0, 0, 0, 1, 2, 0
$ Ticket      <str> 'A/5 21171', 'PC 17599', 'STON/O2. 3101282', '113803', '373450', '330877', '17463', '349909', '347742', '237736'
$ Fare        <f64> 7.25, 71.2833, 7.925, 53.1, 8.05, 8.4583, 51.8625, 21.075, 11.1333, 30.0708
$ Cabin       <str> None, 'C85', None, 'C123', None, None, 'E46', None, None, None
$ Embarked    <str> 'S', 'C', 'S', 'S', 'S', 'Q', 'S', 'S', 'S', 'C'
```
```bash
pqview sql --query "select PassengerId,Sex,Age,Fare from self where Survived=1" --nrows 4 ~/titanic.parquet
```
```
shape: (342, 4)
┌─────────────┬────────┬──────┬─────────┐
│ PassengerId ┆ Sex    ┆ Age  ┆ Fare    │
│ ---         ┆ ---    ┆ ---  ┆ ---     │
│ i64         ┆ str    ┆ f64  ┆ f64     │
╞═════════════╪════════╪══════╪═════════╡
│ 2           ┆ female ┆ 38.0 ┆ 71.2833 │
│ 3           ┆ female ┆ 26.0 ┆ 7.925   │
│ …           ┆ …      ┆ …    ┆ …       │
│ 888         ┆ female ┆ 19.0 ┆ 30.0    │
│ 890         ┆ male   ┆ 26.0 ┆ 30.0    │
└─────────────┴────────┴──────┴─────────┘
```
## License

MIT