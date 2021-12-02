# Clingo Test Runner

`exercise1_0.dl`:
```
% mnr: 3
% incs: node(a)
% incs: node(b) node(c)

node(a).node(b).
```

Execute:
```
python3 clingo ercercise1.dl 1
```

Checks if the number of models is equal to the `%mnr` comment.

---

TODO:
- check if all items of all sets (`%incs`) are included in at least one answer set