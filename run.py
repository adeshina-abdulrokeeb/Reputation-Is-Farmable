import numpy as np, json, time
from bridge import *
MODELS=['base','qs','qs_cap','qs_zero']; KINDS=['fresh','mimic','sleeper']
KS=[10,20,40,80,160]; H=20; T=8; SEEDS=list(range(6))
out=[]
t0=time.time()
for s in SEEDS:
    rng=np.random.default_rng(100+s)
    pop=make_population(rng)
    M=pop['mask'].astype(float)
    R=draw_ratings(rng,pop['mu'],pop['a'],pop['rho'],pop['g'],pop['beta'],pop['d'],pop['mask'])
    q=np.quantile(pop['beta'],0.25)
    cand=np.where(pop['beta']<q)[0]
    targets=rng.choice(cand,T,replace=False)
    clean={m:fit(R,M,m) for m in MODELS}
    thr={m:np.quantile(clean[m]['b'],0.90) for m in MODELS}
    sd={m:clean[m]['b'].std() for m in MODELS}
    for m in MODELS:
        out.append(dict(seed=s,model=m,kind='none',K=0,flip=float((clean[m]['b'][targets]>=thr[m]).mean()),
            shift=0.0,sybil_rho=None,corr=float(np.corrcoef(clean[m]['b'],pop['beta'])[0,1]),cost=0))
    for kind in KINDS:
        for K in KS:
            arng=np.random.default_rng(1000*s+K+hash(kind)%97)
            Rn,Mn=build_attack(arng,pop,kind,K,H,targets)
            R2=np.vstack([R,Rn]); M2=np.vstack([M,Mn])
            for m in MODELS:
                f=fit(R2,M2,m)
                b=f['b'][:len(pop['beta'])]
                out.append(dict(seed=s,model=m,kind=kind,K=K,
                    flip=float((b[targets]>=thr[m]).mean()),
                    shift=float(((b[targets]-clean[m]['b'][targets])/sd[m]).mean()),
                    sybil_rho=float(f['rho'][len(R):].mean()),
                    corr=float(np.corrcoef(b,pop['beta'])[0,1]),
                    cost=int(K*(T+(0 if kind=='fresh' else H)))))
    print('seed',s,'done',round(time.time()-t0),'s',flush=True)
    json.dump(out,open('results.json','w'))
