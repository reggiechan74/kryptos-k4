"""Sequential-memory complete replay fingerprint/float-stream comparison."""
import argparse,array,datetime,gc,gzip,hashlib,json,math,struct
from pathlib import Path
SKIP={'peak_rss_bytes','elapsed_seconds'}
def fingerprint(path,float_path,reference=False):
 with (gzip.open(path,'rt') if str(path).endswith('.gz') else Path(path).open()) as input_file:data=json.load(input_file)
 digest=hashlib.sha256();count=0;maximum=0;different=0;buffer=array.array('d');stream=Path(float_path).open('rb' if reference else 'wb')
 def token(kind,raw=b''):digest.update(kind+struct.pack('>Q',len(raw))+raw)
 def walk(value):
  nonlocal count,maximum,different,buffer
  if isinstance(value,dict):
   keys=sorted(k for k in value if k not in SKIP and not k.endswith('_utc'));token(b'{',str(len(keys)).encode())
   for k in keys:token(b'k',k.encode());walk(value[k])
  elif isinstance(value,list):
   token(b'[',str(len(value)).encode())
   for x in value:walk(x)
  elif isinstance(value,float):
   token(b'd');count+=1
   if reference:
    raw=stream.read(8);assert len(raw)==8,'extra replay float';previous=struct.unpack('d',raw)[0];error=abs(previous-value);assert error<=1e-9,('float difference',count,previous,value);maximum=max(maximum,error);different+=error!=0
   else:
    buffer.append(value)
    if len(buffer)>=8192:buffer.tofile(stream);buffer=array.array('d')
  elif value is None:token(b'n')
  elif isinstance(value,bool):token(b't' if value else b'f')
  elif isinstance(value,int):token(b'i',str(value).encode())
  else:token(b's',value.encode())
 try:
  walk(data)
  if not reference:buffer.tofile(stream)
  else:assert not stream.read(1),'missing replay floats'
 finally:stream.close()
 del data;gc.collect();return dict(discrete_structure_sha256=digest.hexdigest(),floats=count,maximum_absolute_difference=maximum,different_floats=different)
def copy_gzip(source,dest):
 import shutil
 with Path(source).open('rb') as a,Path(dest).open('wb') as raw,gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as b:shutil.copyfileobj(a,b)
def run(original,replay,output,work):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();a=fingerprint(original,work);b=fingerprint(replay,work,True);assert a['discrete_structure_sha256']==b['discrete_structure_sha256'],'discrete model/decision replay differs'
 out=dict(kind='Complete sequential-memory cross-version model replay; every discrete value exact, all floats absolute tolerance1e-9',started_at_utc=start,finished_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),complete=True,discrete_structure_sha256=a['discrete_structure_sha256'],floats_compared=a['floats'],maximum_absolute_float_difference=b['maximum_absolute_difference'],different_floats=b['different_floats'],excluded_metadata=['*_utc','elapsed_seconds','peak_rss_bytes'],actual_K4_evaluations=0,geometry_unchanged=True,io_only_replay_adapter='experiments/replay_site_cylinder037_stream.py')
 Path(output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--original',required=True);ap.add_argument('--replay',required=True);ap.add_argument('--output',required=True);ap.add_argument('--float-work',required=True);args=ap.parse_args();run(args.original,args.replay,args.output,args.float_work)
