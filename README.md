# Two-Phase Locking Protocol
Implementation of database two-phase locking protocol for concurrency control using Python.

## How to run
Type this command in the terminal to run the program:
```sh
python3 main.py -f "file_path" 
```
```sh
python3 main.py -f "tests/input1.txt" 
```

Example inputs are included in `tests` folder. The input format are the operations separated by semicolon, where
each operation consists of an operation, transaction id, and data item (eg. R1(X): reading data item x in transaction 1)



## Authors
| Name                          |   NIM    |
| ----------------------------- | :------: |
| Hanif Muhammad Zhafran        | 13521157 |
| Shidqi Indy Izhari            | 13521097 |
| Manuella Ivana Uli Sianipar   | 13521051 |
| Rava Maulana                  | 13521149 |
