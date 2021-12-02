import sys, os
from subprocess import PIPE, STDOUT, CalledProcessError, TimeoutExpired, check_output

m_anno = "%mnr:"
s_anno = "incs:"

file_name = None

def usage():
  print("Usage: %s FILE COUNT" % sys.argv[0])
  exit(1)

def error_exit(reason):
  print("[%s] Error: %s" % (sys.argv[0], reason))
  exit(1)


# Parse MNR annotation
def parse_mnr(line):
  try:
    return int(line.split(':')[1])
  except ValueError:
    error_exit('wrong usage of "%% mnr: N" annotation in: %s' % line)

# Parse INCS annotation
def parse_incs(line):
  line = line.split(':')[1]
  return line.split(',')


#TODO: integrate set_of_sets -- so check if all items of all sets are included in at least one answerset
def run_test(path, model_size, set_of_sets):
  cmd = ['clingo', '-n', '0', path, file_name]

  try:
    output = check_output(cmd, timeout=2)
  except CalledProcessError as e:
    # clingo exists with 30 as retun code
    if e.returncode != 30:
      error_exit("'%s' failed with the reason above" % (' '.join(e.cmd)))
    else:
      output = e.output
  except TimeoutExpired as e:
    error_exit("'%s' failed because timeout of 2s was expired" % ' '.join(e.cmd))

  output = output.decode('utf-8').split('\n')

  actual_model_size = None

  for line in output: 
    line = ''.join(line.split())
    if 'Models:' in line:
      actual_model_size = parse_mnr(line)

  if actual_model_size is model_size:
    print("SUCCESS -- %d models found!" % model_size)
  elif model_size != 0:
    print("FAILED -- %d models found instead of %d" % (actual_model_size, model_size))
  else:
    print("PASSED -- Nothing found to worry about")


def test_for_file(path):
  
  print('''
  ----------
  Processing %s ...
  ---------
  ''' % path)

  try:
    with open(path) as f:
      lines = f.read().split('\n')
  except FileNotFoundError:
    return print("Warning: %s does not exist" % path)

  model_size = 0
  set_with_facts = []

  for line in lines:
    # remove whitespaces
    line = ''.join(line.split())
    if m_anno in line:
      model_size = parse_mnr(line)
    elif s_anno in line:
      set_with_facts.append(parse_incs(line))
  
  for s in set_with_facts:
    print("At least one set must include: ", ', '.join(s))

  run_test(path, model_size, set_with_facts)


def main():
  if(len(sys.argv) != 3):
    usage()

  global file_name
  file_name = sys.argv[1]
  
  if(not os.path.isfile(file_name)):
    error_exit('File to test does not exist')

  test_file_count = sys.argv[2]
  test_prefix = file_name.split('.')[0]

  for i in range(0,int(test_file_count)):
    test_for_file("%s_%d.dl" % (test_prefix, i))


if __name__ == "__main__":
  main()