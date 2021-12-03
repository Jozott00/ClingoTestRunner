# Clingo Test Runner

This test runner automates the test process of multiple test cases for an Asp program with clingo.

There are two comments in the testcase files that provide information about the expected test results.  
- `% mnr: N` is the expected number of models/answer sets
- `% incs: P [P..]` while the set of all predicates P must be a subset of at least one answer set


If we want to test a file named `test.dl`, then our test case files must be named `test_0.dl, test_1.dl, ... , test_n.dl` and be stored in the same directory as the file to be tested.

---

#### Known issues: 
- For `mnr` greater than 999, the script says failed even if the expected number of models are equal to the result

---

An example:
``` prolog
% inside of ./example/example1_0.dl

% mnr: 1
% incs: guilty(harry)
% incs: innocent(sally)
% incs: guilty(harry) innocent(sally)

motive(harry).
motive(sally).
guilty(harry).
```
So we expect the result to contain 1 answer set, and we have specified three subsets that the answer set should contain.

To execute the test we run
```
python3 clingo_testRunner.py example/example1.dl 1
```

So this command tests the `example1.dl` program with the two test cases `example1_0.dl` (since the test size is 1).

The result would look like:
``` shell
$ python3 clingo_testRunner.py example/example1.dl 2

  ----------
  Processing example/example1_0.dl ...
  ---------
  
💡 INFO -- Exactly 1 model(s) must be found
💡 INFO -- Result must include guilty(harry) innocent(sally)

    🏃 Test running ...
  
✅ PASSED -- All models and sets passed the test

------------------------

RESULTS:
🎉 All tests passed!
```