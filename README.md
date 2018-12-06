# What is this?

This is a set of Python macros to calculate German income tax Lohnsteuer.

# How to use?

Please consider the following test in a reference environment:

```

docker build -t lohnsteuer .
docker run -it lohnsteuer

```

As result, you should see the program pritout.
```
+---------------------------------+---------+------+---------+
| Position                        |   Value | Test | Control |
+---------------------------------+---------+------+---------+
| brutto-svbrutto                 | 4926.59 |  OK  | 4926.59 |
| sozialversicherung-kv           |  362.85 |  !   |   389.4 |
| sozialversicherung-rv           |  458.17 |  OK  |  458.17 |
| sozialversicherung-av           |    73.9 |  OK  |    73.9 |
| sozialversicherung-pv           |   56.42 |  OK  |   56.42 |
| freibetrag-kinderfreibetrag     |  3714.0 |  !   |       0 |
| freibetrag-versorgungspauschale | 7442.41 |  !   |       0 |
| steuer-soli                     |   51.53 |  !   |    42.2 |
| steuer-lohnsteuer               |  936.91 |  !   | 1000.75 |
| netto                           |  2986.8 |  !   | 2804.49 |
+---------------------------------+---------+------+---------+
```

For a local system, install all dependendies as specified in the reference environment.

