"""Run tracked test files only; never execute untracked duplicate-name files."""
import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def suite():
 result=unittest.TestSuite()
 for p in sorted(set(subprocess.check_output(['git','ls-files','tests'],cwd=ROOT).decode().splitlines())):
  if Path(p).name.startswith('test_') and p.endswith('.py'):result.addTests(unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern=Path(p).name))
 return result
if __name__=='__main__':sys.exit(not unittest.TextTestRunner(verbosity=2).run(suite()).wasSuccessful())
