import sys, os
from subprocess import PIPE, STDOUT, CalledProcessError, TimeoutExpired, check_output

m_anno = "%mnr:"
s_anno = "incs:"

file_name = None

failed_tests = 0
succeeded_tests = 0


def usage():
    print("Usage: %s FILE COUNT" % sys.argv[0])
    exit(1)


def error_exit(reason):
    print("[%s] Error: %s" % (sys.argv[0], reason))
    exit(1)


# Parse MNR annotation
def parse_mnr(line):
    try:
        return int(line.split(":")[1])
    except ValueError:
        error_exit('wrong usage of "%% mnr: N" annotation in: %s' % line)


# Parse INCS annotation
def parse_incs(line):
    line = line.split(":")[1]
    return line.split(";")


# TODO: integrate set_of_sets -- so check if all items of all sets are included in at least one answerset
def run_test(path, model_size, set_of_sets):
    cmd = ["clingo", "-n", "0", path, file_name]

    try:
        output = check_output(cmd, timeout=2)
    except CalledProcessError as e:
        # clingo exists with 30 as retun code
        if e.returncode != 30:
            error_exit("'%s' failed with the reason above" % (" ".join(e.cmd)))
        else:
            output = e.output
    except TimeoutExpired as e:
        error_exit("'%s' failed because timeout of 2s was expired" % " ".join(e.cmd))

    output = output.decode("utf-8").split("\n")

    actual_model_size = None
    found_sets = [False] * len(set_of_sets)

    answer_next_line = False
    for line in output:
        if answer_next_line:
            answer_next_line = False
            aset = line.split()
            for i, s in enumerate(set_of_sets):
                if set(s) <= set(aset):
                    found_sets[i] = True
        line = "".join(line.split())
        if "Models:" in line:
            actual_model_size = parse_mnr(line)
        if "Answer:" in line:
            answer_next_line = True

    model_pass = True
    global succeeded_tests
    global failed_tests

    if actual_model_size is not model_size and model_size != 0:
        model_pass = False
        print(
            "❌ FAILED -- %d models found instead of %d"
            % (actual_model_size, model_size)
        )

    set_failed = False
    for i, r in enumerate(found_sets):
        if not r:
            set_failed = True
            print(f"❌ FAILED -- {' '.join(set_of_sets[i])} is in no answer set")

    if not set_failed and model_pass:
        succeeded_tests += 1
        print("✅ PASSED -- All models and sets passed the test")
    else:
        failed_tests += 1


def test_for_file(path):

    print(
        """
  ----------
  Processing %s ...
  ---------
  """
        % path
    )

    try:
        with open(path) as f:
            lines = f.read().split("\n")
    except FileNotFoundError:
        return print("❗ Error: %s does not exist" % path)

    model_size = 0
    set_with_facts = []

    for line in lines:
        # remove whitespaces
        line = "".join(line.split())
        if m_anno in line:
            model_size = parse_mnr(line)
        elif s_anno in line:
            set_with_facts.append(parse_incs(line))

    if model_size is 0:
        print("❗ WARNING -- No model size given. This leads to inaccurate tests!")
    else:
        print(f"💡 INFO -- Exactly {model_size} models must be found")

    for s in set_with_facts:
        print(f"💡 INFO -- Result must include {' '.join(s)}")

    print(
        f"""
    🏃 Tests running ...
  """
    )

    run_test(path, model_size, set_with_facts)


def main():
    if len(sys.argv) != 3:
        usage()

    global file_name
    file_name = sys.argv[1]

    if not os.path.isfile(file_name):
        error_exit("File to test does not exist")

    test_file_count = int(sys.argv[2])
    test_prefix = file_name.split(".")[0]

    for i in range(0, test_file_count):
        test_for_file("%s_%d.dl" % (test_prefix, i))

    print(
        f"""
------------------------

RESULTS:"""
    )

    if succeeded_tests is test_file_count:
        print("🎉 All tests passed!")
    elif succeeded_tests > 0:
        print(f"✅ PASSED: {succeeded_tests}")

    if failed_tests is not 0:
        print(f"❌ FAILED: {failed_tests}")
    if failed_tests + succeeded_tests is not test_file_count:
        print(
            f"❗ INTERRUPTED BY AN ERROR: {test_file_count - (failed_tests + succeeded_tests)}"
        )

    print("")


if __name__ == "__main__":
    main()