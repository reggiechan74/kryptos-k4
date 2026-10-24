"""IO-only streaming adapter for the frozen037 computation.
Preserves original runner bytes/results; avoids a joined116MB output string.
Use a whole-process time/RSS measurement around this script.
"""
import argparse,json
from pathlib import Path
import run_site_cylinder_validation as frozen

def streaming_save(path,value):
 with Path(path).open('w') as out:json.dump(value,out,indent=2);out.write('\n')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--snapshot',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();frozen.save=streaming_save;frozen.run(args.snapshot,args.output)
