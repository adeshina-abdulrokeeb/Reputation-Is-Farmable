import numpy as np, json, time
from bridge import *
MODELS=['base','qs','qs_zero']; KINDS=['mimic','sleeper']
HS=[0,5,10,20,40]; K=40; T=8; out=[]
for s in range(6):
    rng=np.random.default_rng(100+s)
    pop=make_population(rng); M=pop['mask'].astype(float)
    R=draw_ratings(rng,pop['mu'],pop['a'],pop['rho'],pop['g'],pop['beta'],pop['d'],pop['mask'])
    cand=np.where(pop['beta']<np.quantile(pop['beta'],0.25))[0]
    targets=rng.choice(cand,T,replace=False)
    clean={m:fit(R,M,m) for m in MODELS}; sd={m:clean[m]['b'].std() for m in MODELS}
    for kind in KINDS:
        for H in HS:
            arng=np.random.default_rng(5000*s+H+(7 if kind=='mimic' else 13))
            Rn,Mn=build_attack(arng,pop,kind,K,H,targets)
            R2=np.vstack([R,Rn]); M2=np.vstack([M,Mn])
            for m in MODELS:
                f=fit(R2,M2,m); b=f['b'][:len(pop['beta'])]
                out.append(dict(seed=s,model=m,kind=kind,H=H,K=K,
                  shift=float(((b[targets]-clean[m]['b'][targets])/sd[m]).mean()),
                  sybil_rho=float(f['rho'][len(R):].mean())))
    print('seed',s,flush=True); json.dump(out,open('results_h.json','w'))
