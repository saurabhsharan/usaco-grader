import os
import sys
import glob
import shutil
import urllib
import zipfile
import itertools

DOWNLOAD_URL = "http://ace.delos.com/TESTDATA/%s.zip"

# Runs all the test cases for a given problem
# problem_name should be the name of the problem to check without the file extension (e.g. "hello", "space")
def check_problem(problem_name):
   print "====== %s ======" % problem_name
   path_to_zip_file = urllib.urlretrieve(DOWNLOAD_URL % problem_name)[0]
   test_data_zip_file = zipfile.ZipFile(path_to_zip_file)
   test_data_zip_file.extractall()
   for i, input_file in enumerate(sorted(glob.glob('*.in'), key=lambda x: int(x.split(".")[1]))):
      command = "python %s < %s > output.txt" % (problem_name + '.py', input_file)
      print "Executing test case #" + str(i + 1) + "...",
      os.system(command)
      program_output = open("output.txt").read()
      solution = open(os.path.splitext(input_file)[0] + '.out').read()
      if solution == program_output:
         print "successful"
      else:
         print "WRONG"
   for f in itertools.chain(glob.glob('*.out'), glob.glob('*.in')):
      os.remove(f)
   os.remove("output.txt")
   print ''.join("=" for i in range(14 + len(problem_name)))
   
def main():
   if len(sys.argv) > 1:
      for problem_name in sys.argv[1:]:
         check_problem(problem_name)
   else:
      for f in os.listdir(os.getcwd()):
         if os.path.splitext(f)[1] == '.py' and os.path.splitext(f)[0] != 'usaco':
            check_problem(os.path.splitext(f)[0])
   
if __name__ == '__main__':
   main()