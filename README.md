# Clingo Test Runner

This test runner automates the test process of multiple test cases for an Asp program with clingo.

There are two comments in the testcase files that provide information about the expected test results.  
- `% mnr: N` is the expected number of models/answer sets
- `% incs: P;[P;..]` while the set of all predicates P must be a subset of at least one answer set


If we want to test a file named `test.dl`, then our test case files must be named `test_0.dl, test_1.dl, ... , test_n.dl` and be stored in the same directory as the file to be tested.

---

An example:
``` prolog
% inside of ./example/exercise1_0.dl

% mnr: 1
% incs: visited(d,1);visited(f,4);visited(b,3);visited(c,5);visited(e,6); visited(a,2)
% incs: visited(f,4)

node(a). node(b). node(c).
...
```
So we expect the result to contain 1 answer set, and we have specified two subsets that the answer set should contain.

To execute the test we run
```
python3 clingo_testRunner.py example/exercise1.dl 2
```

So this command tests the `exercise1.dl` program with the two test cases `exercise1_0.dl` and `exercise1_1.dl` (since the test size is 2).

The result would look like:
``` shell
$ python3 clingo_testRunner.py example/exercise1.dl 2

  ----------
  Processing example/exercise1_0.dl ...
  ---------
  
💡 INFO -- Exactly 1 model must be found
💡 INFO -- Result must include visited(d,1) visited(f,4) visited(b,3) visited(c,5) visited(e,6) visited(a,2)
💡 INFO -- Result must include visited(f,4)

    🏃 Test running ...
  
✅ PASSED -- All models and sets passed the test

  ----------
  Processing example/exercise1_1.dl ...
  ---------
  
💡 INFO -- Exactly 2 models must be found

    🏃 Test running ...
  
✅ PASSED -- All models and sets passed the test

------------------------

RESULTS:
🎉 All tests passed!
```