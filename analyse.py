import json, numpy as np, collections
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':8,'axes.spines.top':False,'axes.spines.right':False})
r=json.load(open('results.json')); rh=json.load(open('results_h.json'))
KS=[10,20,40,80,160]; MOD=['base','qs','qs_cap','qs_zero']
NAME={'base':'Baseline MF','qs':'QS-MF','qs_cap':'QS-MF, rho<=1','qs_zero':'QS-MF, zero-prior'}
COL={'base':'#444','qs':'#d62728','qs_cap':'#ff9896','qs_zero':'#1f77b4'}
def get(kind,m,K,key='shift'):
    return np.array([x[key] for x in sorted([x for x in r if x['kind']==kind and x['model']==m and x['K']==K],key=lambda z:z['seed'])])
def se(a): return a.std(ddof=1)/np.sqrt(len(a))
# ---- Fig 1: displacement vs K, three attacks
fig,ax=plt.subplots(1,3,figsize=(7.2,2.3),sharey=True)
for a,kind,t in zip(ax,['fresh','mimic','sleeper'],['Fresh accounts (H=0)','Mimic: history by ideology only','Sleeper: history rated carefully']):
    for m in MOD:
        mu=np.array([get(kind,m,K).mean() for K in KS]); s=np.array([se(get(kind,m,K)) for K in KS])
        a.plot(KS,mu,'-o',ms=3,color=COL[m],label=NAME[m]); a.fill_between(KS,mu-1.96*s,mu+1.96*s,color=COL[m],alpha=.15,lw=0)
    a.set_title(t,fontsize=8); a.set_xscale('log'); a.set_xticks(KS); a.set_xticklabels(KS); a.set_xlabel('sybil accounts K')
    a.axhline(1,color='k',lw=.5,ls=':')
ax[0].set_ylabel('target-note displacement (clean SDs)'); ax[0].legend(fontsize=6,frameon=False)
plt.tight_layout(); plt.savefig('fig1.png',dpi=220); plt.close()
# ---- cost to reach displacement 1.0 SD
def cost_to(shifts):  # shifts: dict K->array over seeds ; per-seed interpolation
    res=[];cens=0
    for i in range(len(shifts[KS[0]])):
        pts=[(0,0.0)]+[(K,shifts[K][i]) for K in KS]; c=None
        for (k0,v0),(k1,v1) in zip(pts[:-1],pts[1:]):
            if v1>=1.0>v0 : c=k0+(1.0-v0)/(v1-v0)*(k1-k0); break
        if c is None: c=np.nan
        res.append(c)
    return np.array(res)
rows=[]
for kind in ['fresh','mimic','sleeper']:
    for m in MOD:
        sh={K:get(kind,m,K) for K in KS}; c=cost_to(sh)
        n_c=int(np.isnan(c).sum()); med=np.nanmedian(c) if n_c<len(c) else np.nan
        rows.append((kind,m,med,n_c))
        print(f'{kind:8s} {m:8s} K@1SD median={med:.0f} censored={n_c}/6   ratings={med*(8+(0 if kind=="fresh" else 20)):.0f}')
# protection
print('\nprotection vs baseline (mean over seeds of 1-qs/base displacement):')
for kind in ['mimic','sleeper']:
    for m in ['qs','qs_cap','qs_zero']:
        pr=[]
        for K in KS:
            p=1-get(kind,m,K)/get(kind,'base',K); pr.append((K,p.mean(),se(p)))
        print(kind,m,' '.join(f'K={K}:{p*100:.0f}%±{1.96*s*100:.0f}' for K,p,s in pr))
# ---- Fig 2 : H sweep
HS=[0,5,10,20,40]
def geth(kind,m,H,key):
    return np.array([x[key] for x in rh if x['kind']==kind and x['model']==m and x['H']==H])
fig,ax=plt.subplots(1,2,figsize=(6.2,2.3))
for kind,ls in [('sleeper','-'),('mimic','--')]:
    for m in ['base','qs','qs_zero']:
        mu=np.array([geth(kind,m,H,'shift').mean() for H in HS]); s=np.array([se(geth(kind,m,H,'shift')) for H in HS])
        ax[0].plot(HS,mu,ls,marker='o',ms=3,color=COL[m],label=f'{NAME[m]} / {kind}')
        ax[0].fill_between(HS,mu-1.96*s,mu+1.96*s,color=COL[m],alpha=.1,lw=0)
    if kind=='sleeper':
        for m in ['qs','qs_zero']:
            ax[1].plot(HS,[geth(kind,m,H,'sybil_rho').mean() for H in HS],'-o',ms=3,color=COL[m],label=f'{NAME[m]} sleeper')
    else:
        for m in ['qs']:
            ax[1].plot(HS,[geth(kind,m,H,'sybil_rho').mean() for H in HS],'--o',ms=3,color=COL[m],label=f'{NAME[m]} mimic')
ax[0].set_xlabel('honest-looking history ratings per sybil, H'); ax[0].set_ylabel('displacement at K=40 (clean SDs)'); ax[0].legend(fontsize=5,frameon=False)
ax[1].set_xlabel('history ratings per sybil, H'); ax[1].set_ylabel('mean sybil reputation  rho-hat'); ax[1].legend(fontsize=6,frameon=False)
plt.tight_layout(); plt.savefig('fig2.png',dpi=220); plt.close()
print('\nH sweep (K=40) displacement / sybil rho:')
for kind in ['sleeper','mimic']:
    for m in ['base','qs','qs_zero']:
        print(kind,m,' '.join(f'H={H}:{geth(kind,m,H,"shift").mean():.2f}/{geth(kind,m,H,"sybil_rho").mean():.2f}' for H in HS))
# clean-run corr
cl=collections.defaultdict(list)
for x in r:
    if x['kind']=='none': cl[x['model']].append(x['corr'])
print('\nclean corr(b, truth):',{m:round(float(np.mean(v)),3) for m,v in cl.items()})
