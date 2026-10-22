#!/usr/bin/env python3
"""Bounded independent calibration. See immutable preregistration; no repository IO."""
from pathlib import Path
import hashlib,json,math,time
import numpy as np
import scipy
import sklearn
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,accuracy_score,f1_score

ROOT=Path(__file__).resolve().parent
SEED=20261022
AZ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KA='KRYPTOSABCDEFGHIJLMNQUVWXZ'
K4='OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR'
CRIB1=(21,'EASTNORTHEAST'); CRIB2=(63,'BERLINCLOCK')
LABELS=['PERIODIC','BLOCK_TRANSPOSE','EVOLVING_ALPHABET']
FEATURES=['IC','entropy_bits','distinct_symbols','largest_count','bigram_pair_collision','lag1_coincidence','max_lag2_12_coincidence','max_period2_12_residue_IC']
assert len(K4)==97 and len(CRIB1[1])==13 and len(CRIB2[1])==11
assert len(KA)==26 and set(KA)==set(AZ)
assert len(set(range(21,34))|set(range(63,74)))==24

def encode(s,alphabet=AZ): return np.array([alphabet.index(t) for t in s],dtype=np.int64)
def decode(x,alphabet=AZ): return ''.join(alphabet[int(t)] for t in x)
def clean(s): return ''.join(t for t in s.upper() if t in AZ)
def ic(x):
    if len(x)<2:return 0.
    n=np.bincount(x,minlength=26)
    return float((n*(n-1)).sum()/(len(x)*(len(x)-1)))
def features(x):
    n=np.bincount(x,minlength=26); p=n[n>0]/len(x)
    b=np.bincount(x[:-1]*26+x[1:],minlength=676)
    return np.array([ic(x),float(-(p*np.log2(p)).sum()),np.count_nonzero(n),n.max(),float((b*(b-1)).sum()/((len(x)-1)*(len(x)-2))),float(np.mean(x[1:]==x[:-1])),max(float(np.mean(x[l:]==x[:-l])) for l in range(2,13)),max(float(np.mean([ic(x[j::m]) for j in range(m)])) for m in range(2,13))])

def encrypt(p,family,rng):
    if family==0:
        m=int(rng.integers(2,13)); k=rng.integers(0,26,m)
        return (p+k[np.arange(len(p))%m])%26,{'period':m,'key':k.tolist()}
    if family==1:
        m=int(rng.integers(5,13)); order=rng.permutation(m)
        c=np.concatenate([p[i+order[order<min(m,len(p)-i)]] for i in range(0,len(p),m)])
        return c,{'width':m,'permutation':order.tolist()}
    a=rng.permutation(26); initial=a.copy(); c=[]
    for x in p:
        y=int(a[x]); c.append(y);a=np.roll(a,-((y+1)%26));a[0],a[13]=a[13],a[0]
    return np.array(c),{'initial_alphabet':initial.tolist()}

def decrypt(c,family,key):
    if family==0:
        k=np.array(key['key']);return(c-k[np.arange(len(c))%len(k)])%26
    if family==1:
        m=key['width']; order=np.array(key['permutation']);p=np.empty_like(c)
        for i in range(0,len(c),m):
            use=order[order<min(m,len(c)-i)];p[i+use]=c[i:i+len(use)]
        return p
    a=np.array(key['initial_alphabet']);p=[]
    for y in c:
        p.append(int(np.flatnonzero(a==y)[0]));a=np.roll(a,-((int(y)+1)%26));a[0],a[13]=a[13],a[0]
    return np.array(p)

def model(): return make_pipeline(StandardScaler(),LogisticRegression(C=1,solver='lbfgs',max_iter=2000))
def plain_windows(corpus,split,rng):
    result=[]
    for source,text in enumerate(corpus[split]):
        text=clean(text);assert len(text)>=97
        for offset in rng.integers(0,len(text)-96,8):
            result.append({'source':source,'offset':int(offset),'plaintext':text[int(offset):int(offset)+97]})
    assert len(result)==48
    return result

def classification():
    rng=np.random.default_rng(SEED)
    corpus=json.loads((ROOT/'corpus.json').read_text())
    windows={split:plain_windows(corpus,split,rng) for split in ['train','test']}
    data={}
    for split,ww in windows.items():
        rows=[]
        for index,w in enumerate(ww):
            p=encode(w['plaintext'])
            for family in range(3):
                c,key=encrypt(p,family,rng);assert len(c)==97
                assert np.array_equal(decrypt(c,family,key),p)
                rows.append({**w,'plain_index':index,'label':family,'ciphertext':decode(c),'key':key,'features':features(c).tolist()})
        data[split]=rows
    X={s:np.array([r['features'] for r in rr]) for s,rr in data.items()}
    y={s:np.array([r['label'] for r in rr]) for s,rr in data.items()}
    fitted=model().fit(X['train'],y['train'])
    preds={s:fitted.predict(X[s]) for s in data}
    out={'seed':SEED,'versions':{'numpy':np.__version__,'scipy':scipy.__version__,'sklearn':sklearn.__version__},'labels':LABELS,'features':FEATURES,'source_lengths':{s:[len(clean(t)) for t in corpus[s]] for s in corpus},'metrics':{}}
    for s in data:
        cm=confusion_matrix(y[s],preds[s],labels=range(3))
        out['metrics'][s]={'n':len(y[s]),'accuracy':float(accuracy_score(y[s],preds[s])),'macro_f1':float(f1_score(y[s],preds[s],average='macro')),'confusion_matrix':cm.tolist(),'recall':(cm.diagonal()/cm.sum(axis=1)).tolist()}
        for row,p in zip(data[s],preds[s]): row['predicted_label']=int(p)
    source=np.array([r['source'] for r in data['test']]); correct=preds['test']==y['test']
    source_acc=np.array([correct[source==i].mean() for i in range(6)])
    bs=np.random.default_rng(SEED+1).choice(source_acc,size=(2000,6),replace=True).mean(axis=1)
    out['metrics']['test']['source_accuracies']=source_acc.tolist()
    out['metrics']['test']['source_bootstrap_accuracy_CI95']=np.quantile(bs,[.025,.975]).tolist()
    out['metrics']['test']['source_bootstrap_effective_clusters']=6
    controls={name:[] for name in ['PLAINTEXT','MONOALPHABETIC','CHARACTER_SHUFFLE','IID_UNIFORM']}
    for w in windows['test']:
        p=encode(w['plaintext']);sub=rng.permutation(26)
        for name,c in [('PLAINTEXT',p),('MONOALPHABETIC',sub[p]),('CHARACTER_SHUFFLE',rng.permutation(p)),('IID_UNIFORM',rng.integers(0,26,97))]:
            controls[name].append({'source':w['source'],'ciphertext':decode(c),'features':features(c).tolist()})
    out['controls']={}
    for name,rows in controls.items():
        pred=fitted.predict(np.array([r['features'] for r in rows]))
        out['controls'][name]={'n':48,'forced_label_counts':np.bincount(pred,minlength=3).tolist()}
    nullrng=np.random.default_rng(SEED+2); null=[]
    for j in range(199):
        ym=nullrng.permutation(y['train']);m=model().fit(X['train'],ym)
        null.append(float(accuracy_score(y['test'],m.predict(X['test']))))
    actual=out['metrics']['test']['accuracy']
    out['randomized_training_label_null']={'runs':199,'accuracy_mean':float(np.mean(null)),'accuracy_range':[min(null),max(null)],'accuracy_q95':float(np.quantile(null,.95)),'add_one_p':float((1+sum(t>=actual for t in null))/200),'interpretation':'Conditional toy label-randomization diagnostic, not a p-value about K4 or universal classification. Global label permutation does not model plaintext-source uncertainty.'}
    kfeat=features(encode(K4));kpred=int(fitted.predict(kfeat[None,:])[0]);kz=fitted[0].transform(kfeat[None,:])[0]
    out['K4']={'ciphertext':K4,'features':kfeat.tolist(),'training_standardized_features':kz.tolist(),'forced_label':LABELS[kpred],'warning':'Forced nearest-family label is NOT evidence that K4 belongs to any trained family; no class probability or K4 significance is estimated.'}
    out['feature_means']={s:{LABELS[j]:X[s][y[s]==j].mean(axis=0).tolist() for j in range(3)} for s in data}
    (ROOT/'classification_results.json').write_text(json.dumps(out,indent=2)+'\n')
    (ROOT/'generated_examples.json').write_text(json.dumps({'data':data,'controls':controls,'windows':windows},indent=2)+'\n')
    (ROOT/'label_null_accuracy.json').write_text(json.dumps(null)+'\n')
    return out,windows

def recurrence_encrypt(p,a,b,d,k):
    c=[];state=k
    for x in p:
        y=(int(x)+state)%26;c.append(y);state=(a*state+b+d*y)%26
    return np.array(c)

def synthesize(cipher,train_cribs,validation_cribs,timeout=120):
    begin=time.monotonic();all_candidates=[];alphabet_counts=[];descriptions=0;finished=True
    for alphabet in [AZ,KA]:
        c=encode(cipher,alphabet)
        train={start+i:alphabet.index(letter) for start,txt in train_cribs for i,letter in enumerate(txt)}
        val={start+i:alphabet.index(letter) for start,txt in validation_cribs for i,letter in enumerate(txt)}
        assert not(set(train)&set(val))
        boundary=max(train);end=max([boundary]+list(val));before=0;after=0
        # Every tuple visited once; no modular rank or invertibility assumptions.
        for a in range(26):
            if time.monotonic()-begin>timeout:finished=False;break
            k,b,d=np.indices((26,26,26),dtype=np.int64).reshape(3,-1)
            descriptions+=len(k);state=k.copy()
            for i in range(end+1):
                if i>0: state=(a*state+b+d*c[i-1])%26
                if i in train or i in val:
                    target=train[i] if i in train else val[i]
                    mask=(c[i]-state)%26==target
                    k,b,d,state=k[mask],b[mask],d[mask],state[mask]
                if i==boundary:before+=len(k)
                # Empty remains empty; ensure boundary counting is already zero.
                if not len(k):break
            after+=len(k)
            all_candidates.extend((alphabet,a,int(bb),int(dd),int(kk)) for kk,bb,dd in zip(k,b,d))
        alphabet_counts.append({'alphabet':alphabet,'after_first_crib':before,'after_validation':after})
        if not finished:break
    # Replay all full plaintexts and count distinct plaintext strings/forced sets.
    plaintexts=set();chars=[set() for _ in range(97)]
    for alphabet,a,b,d,k in all_candidates:
        c=encode(cipher,alphabet);state=k;pp=[]
        for i,y in enumerate(c):
            if i>0:state=(a*state+b+d*int(c[i-1]))%26
            pp.append(alphabet[(int(y)-state)%26])
        p=''.join(pp);plaintexts.add(p)
        for ss,ch in zip(chars,p):ss.add(ch)
    forced=[{'position_1based':i+1,'character':next(iter(ch))} for i,ch in enumerate(chars) if len(ch)==1]
    ambiguous=[{'position_1based':i+1,'possible_characters':''.join(sorted(ch))} for i,ch in enumerate(chars) if len(ch)>1]
    if not finished:status='TIMEOUT'
    elif not all_candidates:status='UNSAT'
    elif len(all_candidates)==1:status='SAT_UNIQUE_DESCRIPTION'
    else:status='SAT_AMBIGUOUS_DESCRIPTIONS'
    result={'status':status,'elapsed_seconds':time.monotonic()-begin,'descriptions_examined':descriptions,'description_budget':2*26**4,'full_budget_exhausted':finished,'counts_by_alphabet':alphabet_counts,'parameter_candidates':len(all_candidates),'distinct_full_plaintexts':len(plaintexts),'forced_positions':forced,'ambiguous_positions':ambiguous,'candidate_preview':[{'alphabet':al,'a':a,'b':b,'d':d,'k':k} for al,a,b,d,k in all_candidates[:10]],'plaintext_preview':sorted(plaintexts)[:3]}
    return result,all_candidates

def synthesis(windows):
    rng=np.random.default_rng(SEED+3)
    kresult,_=synthesize(K4,[CRIB1],[CRIB2]);results={'grammar':'C_i=P_i+K_i mod26; K_0=k; K_i=a*K_(i-1)+b+d*C_(i-1) mod26','fixed_slot_parameter_bits':21,'K4':kresult,'synthetic_positives':[]}
    targets=[]
    for case,a in enumerate([0,1,2,5,13,25]):
        p=list(windows['test'][case*8]['plaintext'])
        for start,s in [CRIB1,CRIB2]:p[start:start+len(s)]=list(s)
        p=''.join(p);k,b,d=map(int,rng.integers(0,26,3));c=decode(recurrence_encrypt(encode(p),a,b,d,k))
        r,cands=synthesize(c,[CRIB1],[CRIB2]);planted=(AZ,a,b,d,k)
        assert planted in cands and r['status']!='UNSAT'
        r.update({'case':case,'planted':{'alphabet':AZ,'a':a,'b':b,'d':d,'k':k},'planted_survives':True,'ciphertext':c,'planted_plaintext':p})
        results['synthetic_positives'].append(r);targets.append((c,planted))
    r,cands=synthesize(targets[1][0],[(21,'E')],[])
    r['planted_survives']=targets[1][1] in cands
    results['underconstrained_control']=r
    assert r['parameter_candidates']>1 and r['planted_survives']
    # Explicit timeout-path check: zero budget cannot be confused with UNSAT.
    timeout,_=synthesize(K4,[CRIB1],[CRIB2],timeout=0)
    assert timeout['status']=='TIMEOUT' and not timeout['full_budget_exhausted']
    results['zero_time_budget_status_test']=timeout
    (ROOT/'synthesis_results.json').write_text(json.dumps(results,indent=2)+'\n')
    return results

def main():
    t=time.monotonic();cl,ww=classification();sy=synthesis(ww)
    report={'classification':cl['metrics'],'controls':cl['controls'],'null':cl['randomized_training_label_null'],'K4_forced_label':cl['K4']['forced_label'],'K4_synthesis':{k:sy['K4'][k] for k in ['status','descriptions_examined','counts_by_alphabet','parameter_candidates','distinct_full_plaintexts']},'positive_synthesis_counts':[{k:r[k] for k in ['case','parameter_candidates','distinct_full_plaintexts','planted_survives']} for r in sy['synthetic_positives']],'elapsed_seconds':time.monotonic()-t}
    print(json.dumps(report,indent=2))
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.iterdir() if p.is_file() and p.name!='MANIFEST.json'}
    (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
