"""Narrow read-only AST literal selector. Never executes inspected source."""
import ast
import hashlib
import json
import sys

MAX_SOURCE=262144
MAX_NODES=20000
MAX_DEPTH=80
LIMITATION='Literal extraction only; comprehension semantics, later runtime behavior and provenance authenticity are not validated.'

def fail(reason): return {'status':'FAIL','reason':reason}
def location(node): return {k:getattr(node,k,None) for k in ('lineno','col_offset','end_lineno','end_col_offset')}

def verify(source,request):
    if not isinstance(source,bytes) or len(source)>MAX_SOURCE:return fail('SOURCE_SIZE_OR_TYPE')
    if not isinstance(request,dict) or set(request)!={'sha256','provenance','assignment','key','expected'}:return fail('REQUEST_SHAPE')
    sha=request['sha256'];name=request['assignment'];key=request['key'];expected=request['expected']
    if not isinstance(sha,str) or len(sha)!=64 or any(c not in '0123456789abcdef' for c in sha):return fail('HASH_SHAPE')
    if not isinstance(request['provenance'],str) or not 1<=len(request['provenance'])<=2048:return fail('PROVENANCE_SHAPE')
    if not isinstance(name,str) or not name.isidentifier() or not isinstance(key,str) or len(key)>256:return fail('SELECTOR_SHAPE')
    if not isinstance(expected,list) or len(expected)>256 or any(type(x) is not str or len(x)>256 for x in expected):return fail('EXPECTED_SHAPE')
    digest=hashlib.sha256(source).hexdigest()
    if digest!=sha:return fail('HASH_MISMATCH')
    try: text=source.decode('utf-8');tree=ast.parse(text)
    except (UnicodeDecodeError,SyntaxError,ValueError,MemoryError,RecursionError):return fail('PARSE_FAILURE')
    nodes=[];stack=[(tree,0)]
    while stack:
        n,d=stack.pop();nodes.append(n)
        if len(nodes)>MAX_NODES or d>MAX_DEPTH:return fail('AST_LIMIT')
        stack.extend((c,d+1) for c in ast.iter_child_nodes(n))
    assignments=[n for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id==name]
    if len(assignments)!=1:return fail('ASSIGNMENT_MISSING_OR_DUPLICATE')
    assignment=assignments[0];allowed_target=assignment.targets[0]
    for n in nodes:
        if isinstance(n,ast.Name) and n.id==name and isinstance(n.ctx,(ast.Store,ast.Del)) and n is not allowed_target:return fail('AMBIGUOUS_BINDING')
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and n.name==name:return fail('AMBIGUOUS_BINDING')
        if isinstance(n,ast.arg) and n.arg==name:return fail('AMBIGUOUS_BINDING')
        if isinstance(n,ast.alias) and (n.asname or n.name.split('.')[0])==name:return fail('AMBIGUOUS_BINDING')
        if isinstance(n,ast.ExceptHandler) and n.name==name:return fail('AMBIGUOUS_BINDING')
        if isinstance(n,(ast.MatchAs,ast.MatchStar)) and n.name==name:return fail('AMBIGUOUS_BINDING')
        if isinstance(n,ast.MatchMapping) and n.rest==name:return fail('AMBIGUOUS_BINDING')
        if isinstance(n,(ast.Attribute,ast.Subscript)) and isinstance(n.ctx,(ast.Store,ast.Del)):
            base=n
            while isinstance(base,(ast.Attribute,ast.Subscript)):base=base.value
            if isinstance(base,ast.Name) and base.id==name:return fail('AMBIGUOUS_BINDING')
    dictionary=assignment.value
    if not isinstance(dictionary,ast.Dict):return fail('UNSUPPORTED_DICTIONARY')
    if any(not isinstance(k,ast.Constant) or type(k.value) is not str for k in dictionary.keys):return fail('DYNAMIC_OR_UNPACKED_KEY')
    matches=[(k,v) for k,v in zip(dictionary.keys,dictionary.values) if k.value==key]
    if len(matches)!=1:return fail('KEY_MISSING_OR_DUPLICATE')
    keynode,value=matches[0]
    comp=value
    if isinstance(value,ast.Call):
        if not isinstance(value.func,ast.Name) or value.func.id!='tuple' or len(value.args)!=1 or value.keywords or not isinstance(value.args[0],ast.GeneratorExp):return fail('UNSUPPORTED_COMPREHENSION')
        comp=value.args[0]
    if not isinstance(comp,(ast.ListComp,ast.GeneratorExp)) or len(comp.generators)!=1 or comp.generators[0].is_async or comp.generators[0].ifs:return fail('UNSUPPORTED_COMPREHENSION')
    if isinstance(value,ast.GeneratorExp):return fail('UNSUPPORTED_COMPREHENSION')
    iterable=comp.generators[0].iter
    if not isinstance(iterable,(ast.Tuple,ast.List)) or len(iterable.elts)>256:return fail('NONLITERAL_ITERABLE')
    if any(not isinstance(x,ast.Constant) or type(x.value) is not str or len(x.value)>256 for x in iterable.elts):return fail('NONLITERAL_ITEM')
    actual=[x.value for x in iterable.elts]
    if actual!=expected:return fail('VALUE_MISMATCH')
    return {'status':'PASS','selector_version':1,'source_sha256':digest,'provenance_supplied':request['provenance'],'assignment':name,'key':key,'assignment_location':location(assignment),'key_location':location(keynode),'iterable_location':location(iterable),'actual':actual,'limitation':LIMITATION}

def unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError("duplicate request key")
        result[key]=value
    return result

def main():
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_CPU,(2,2));resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,256*1024*1024))
        if len(sys.argv)!=3:print(json.dumps(fail('USAGE')));return 2
        with open(sys.argv[1],'rb') as f:raw=f.read(65537)
        if len(raw)>65536:print(json.dumps(fail('REQUEST_SIZE')));return 2
        request=json.loads(raw,object_pairs_hook=unique_object)
        with open(sys.argv[2],'rb') as f:source=f.read(MAX_SOURCE+1)
        result=verify(source,request)
    except (OSError,ValueError,TypeError,MemoryError,RecursionError):result=fail('INPUT_FAILURE')
    print(json.dumps(result,ensure_ascii=True));return 0 if result['status']=='PASS' else 2

if __name__=='__main__':sys.exit(main())
