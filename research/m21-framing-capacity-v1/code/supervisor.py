"""Launch once only after root's exact grant; bounds apply to whole child process."""
import os
import hashlib
import json
import resource
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent

def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(180,180))
    resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
    resource.setrlimit(resource.RLIMIT_FSIZE,(128*1024**2,128*1024**2))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))

if __name__=='__main__':
    if sys.argv[1:]!=['--root-granted']:
        raise SystemExit('No implicit experiment grant: explicit --root-granted required')
    binding=json.loads((HERE/'RUNTIME.json').read_text())
    executable=Path(sys.executable).resolve()
    if str(executable)!=binding['executable'] or hashlib.sha256(executable.read_bytes()).hexdigest()!=binding['sha256']:
        raise SystemExit('Interpreter binding mismatch')
    if list(sys.version_info[:3])!=binding['version_info']:raise SystemExit('Interpreter version mismatch')
    frozen=json.loads((HERE/'SOURCE-SHA256.json').read_text())
    for name,expected in frozen.items():
        actual=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
        if actual!=expected:raise SystemExit('Frozen source mismatch: '+name)
    marker=HERE/'ATTEMPT_STARTED'
    with marker.open('x') as f:f.write('One-shot attempt; do not remove or overwrite.\n')
    result_dir=HERE/'results'
    result_dir.mkdir(exist_ok=False)
    with (result_dir/'stdout.txt').open('w') as out,(result_dir/'stderr.txt').open('w') as err:
        try:
            cp=subprocess.run([str(executable),'-I','-S','-B',str(HERE/'run_pilot.py')],cwd=HERE,
                stdin=subprocess.DEVNULL,stdout=out,stderr=err,timeout=240,preexec_fn=limits,
                env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'})
            status=str(cp.returncode)
        except subprocess.TimeoutExpired:status='WALL_TIMEOUT_UNKNOWN'
    (result_dir/'supervisor_status.txt').write_text(status+'\n')
    print(status)
