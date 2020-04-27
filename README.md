# csv_compare
Simple tool to compare a column of two csv files, matching their record Ids

## Usage
Say you have two csv files, sharing a key column (say, the first one):

```
  $ cat file1.csv
  a,a2,a3
  b,b2,b3
  c,c3,c4
  
  $ cat file2.csv
  c,c2,c3
  a,a3,a3
  d,d2,d3
```
And you want to check which records have different values in the third column. You can find out by running:
```
  $ csv_compare file1.csv file2.csv 1 3
  key,file1,file2
  c,c4,c3
```
  
  
