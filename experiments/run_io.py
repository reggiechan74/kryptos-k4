"""Atomic, uniquely named run snapshots; manifest status governs validity."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import uuid


def atomic_write(path, content):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.'+path.name+'.',dir=str(path.parent))
    try:
        with os.fdopen(fd,'wb') as handle:
            handle.write(content);handle.flush();os.fsync(handle.fileno())
        os.replace(name,path)
    finally:
        if os.path.exists(name):os.unlink(name)


def json_bytes(value):return (json.dumps(value,indent=2)+'\n').encode()


def specification(commit, path):
    if not re.fullmatch(r'[0-9a-f]{40}',commit or ''):
        raise ValueError('a full already-committed specification SHA is required')
    label=Path(path).name if Path(path).is_absolute() else str(path)
    return {'commit':commit,'file':label,'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'verification':'Caller supplies committed specification; chronology must be checked against repository history.'}


class RunSnapshot:
    """Stage a complete snapshot then publish its directory with one rename.

    Prior runs and original audited artifacts are never overwritten. On failure
    only the new run's manifest is published, marked incomplete, without result
    artifacts. latest.json immediately marks a new attempt running/incomplete so
    an earlier successful run cannot masquerade as the current attempt.
    """
    def __init__(self, root, label, spec, run_id=None, execution_kind="unspecified"):
        if execution_kind not in ("original","replay","validation","unspecified"):raise ValueError("invalid execution kind")
        self.root=Path(root)
        self.run_id=run_id or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex
        if not re.fullmatch(r'[A-Za-z0-9_-]+',self.run_id):raise ValueError('invalid run id')
        self.stage=self.root/('.'+self.run_id+'.pending');self.final=self.root/self.run_id
        self.manifest={'run_id':self.run_id,'started_at_utc':datetime.now(timezone.utc).isoformat(),'label':label,'execution_kind':execution_kind,'status':'running','specification':spec,'jobs':[],'artifacts':{}}
        self.files=[]
        self.final_check=None

    def pointer(self):
        atomic_write(self.root/'latest.json',json_bytes({'run_id':self.run_id,'status':self.manifest['status'],'manifest':self.run_id+'/manifest.json'}))

    def __enter__(self):
        self.root.mkdir(parents=True,exist_ok=True)
        if self.final.exists():raise FileExistsError('run id already published')
        self.stage.mkdir()
        atomic_write(self.stage/'manifest.json',json_bytes(self.manifest));self.pointer()
        return self

    def write(self,name,content):
        if Path(name).name!=name or name in ['manifest.json','latest.json']:
            raise ValueError('result names must be plain filenames')
        atomic_write(self.stage/name,content)
        if name not in self.files:self.files.append(name)
        self.manifest['artifacts'][name]={'sha256':hashlib.sha256(content).hexdigest(),'bytes':len(content)}

    def __exit__(self,kind,error,traceback):
        publish_error=None
        if kind is None and self.final_check is not None:
            try:self.final_check()
            except BaseException as caught:
                kind,error,publish_error=type(caught),caught,caught
                if self.manifest['jobs']:self.manifest['jobs'][-1]['status']='incomplete'
        if kind is None:self.manifest['status']='completed'
        else:
            self.manifest.update({'status':'incomplete','outcome':'timed_out' if isinstance(error,TimeoutError) else 'interrupted' if isinstance(error,KeyboardInterrupt) else 'error','error_type':kind.__name__})
            for name in self.files:(self.stage/name).unlink(missing_ok=True)
            self.manifest['artifacts']={}
        self.manifest['finished_at_utc']=datetime.now(timezone.utc).isoformat()
        atomic_write(self.stage/'manifest.json',json_bytes(self.manifest))
        os.replace(self.stage,self.final)
        self.pointer()
        if publish_error is not None:raise publish_error
        return False
