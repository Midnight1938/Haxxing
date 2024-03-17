# Yea ik im reading the writeup

## Python + Ruby

```python
0 and 1 or 2
```

## Pearl

```pearl
"b" + "0" == 0
```

## Combination

```python
("b" + "0" == 0 and 3) or (0 and 1 or 2)
```

or, to get the output via all three languages:

```python
print((("b" + "0" == 0 and exec("cat flag.txt")) or (0 and exec("cat flag.txt") or eval('__import__("sys").stdout.write(open("flag.txt").read())'))));
```

## Adding PHP

```php
#//<?php system('cat flag.txt;'); __halt_compiler();?>
print((("b" + "0" == 0 and exec("cat flag.txt")) or (0 and exec("cat flag.txt") or eval('__import__("sys").stdout.write(open("flag.txt").read())'))));
```

## Adding final C/C++

```c

```
