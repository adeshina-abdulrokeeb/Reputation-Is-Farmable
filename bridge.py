"""Sleeper-attack simulator for bridging-based note ranking.
Models: baseline MF (Community-Notes style), QS-MF (per-rater quality sensitivity rho),
and two defence variants. Sums-of-squares ALS on a dense masked matrix.
"""
import numpy as np

# ---------------- regularisation (sum-of-squares loss; see report Sec. 3) -------------
LAM_A, LAM_B, LAM_G, LAM_D, LAM_RHO = 2.0, 2.0, 0.4, 0.4, 1.0


def make_population(rng, n_raters=800, n_notes=400, density=0.08, bad_frac=0.10):
    """Ground-truth world. rating = 1[mu + a_i + rho_i*beta_j + g_i*d_j + eps > 0.5]."""
    side = rng.choice([-1.0, 1.0], n_raters)
    g = side * np.clip(rng.normal(0.6, 0.2, n_raters), 0.1, None)
    a = rng.normal(0, 0.1, n_raters)
    rho = np.clip(rng.normal(1.0, 0.25, n_raters), 0.3, None)
    bad = rng.random(n_raters) < bad_frac       # background noisy/partisan raters
    rho[bad] = 0.0
    beta = rng.normal(0, 0.35, n_notes)
    d = rng.normal(0, 0.7, n_notes)
    mask = rng.random((n_raters, n_notes)) < density
    return dict(g=g, a=a, rho=rho, beta=beta, d=d, mask=mask, mu=0.45, side=side)


def draw_ratings(rng, mu, a, rho, g, beta, d, mask, noise=0.25):
    lin = mu + a[:, None] + rho[:, None] * beta[None, :] + g[:, None] * d[None, :]
    return ((lin + rng.normal(0, noise, lin.shape)) > 0.5).astype(float) * mask


def fit(R, M, model="base", iters=30, seed=0):
    """model in {base, qs, qs_cap, qs_zero}. Returns dict with b (note intercepts), rho, d, g."""
    n, m = R.shape
    rng = np.random.default_rng(seed)
    mu = (R * M).sum() / M.sum()
    # init factors from top singular vector of mean-imputed centred matrix
    C = np.where(M > 0, R - mu, 0.0)
    U, S, Vt = np.linalg.svd(C, full_matrices=False)
    g = U[:, 0] * np.sqrt(S[0]) * 0.1
    d = Vt[0] * np.sqrt(S[0]) * 0.1
    a = np.zeros(n); b = np.zeros(m)
    rho0 = 0.0 if model == "qs_zero" else 1.0
    rho = np.full(n, rho0 if model != "qs_zero" else 1.0)
    lam_rho = 1e9 if model == "base" else LAM_RHO
    if model == "base":
        rho = np.ones(n)
    for it in range(iters):
        # ---- note step: (b_j, d_j)
        y = (R - mu - a[:, None]) * M
        X = np.stack([rho, g], 1)                       # n x 2
        A = np.einsum('ij,ik,il->jkl', M, X, X) + np.diag([LAM_B, LAM_D])[None]
        rhs = np.einsum('ij,ik->jk', y, X)
        sol = np.linalg.solve(A, rhs[..., None])[..., 0]
        b, d = sol[:, 0], sol[:, 1]
        # ---- rater step: (a_i, rho_i, g_i)
        y = (R - mu) * M
        Xn = np.stack([np.ones(m), b, d], 1)            # m x 3
        A = np.einsum('ij,jk,jl->ikl', M, Xn, Xn)
        A = A + np.diag([LAM_A, lam_rho, LAM_G])[None]
        rhs = np.einsum('ij,jk->ik', y, Xn)
        prior = np.array([0.0, rho0 if model != "base" else 1.0, 0.0])
        rhs = rhs + np.array([LAM_A, lam_rho, LAM_G]) * prior * np.array([0, 1, 0])
        sol = np.linalg.solve(A, rhs[..., None])[..., 0]
        a, rho, g = sol[:, 0], sol[:, 1], sol[:, 2]
        if model == "base":
            rho = np.ones(n)
        else:
            rho = np.clip(rho, 0.0, None)
            if model == "qs_cap":
                rho = np.minimum(rho, 1.0)
        # ---- global intercept
        pred = a[:, None] + rho[:, None] * b[None] + g[:, None] * d[None]
        mu = ((R - pred) * M).sum() / M.sum()
    if model != "base":
        rb = rho.mean()
        if rb > 1e-6:
            rho = rho / rb; b = b * rb
    return dict(b=b, rho=rho, d=d, g=g, mu=mu)


# ----------------------------- attacks ------------------------------------------------
def build_attack(rng, pop, kind, K, H, targets):
    """Return (Rn, Mn) extra rows for K sybils.
    kind: 'fresh'  - rate only the targets 'helpful'
          'mimic'  - H history notes rated by ideology only (rho=0), then targets
          'sleeper'- H history notes rated like a careful honest rater (rho=1), then targets
    Half the sybils take each ideological side (so the attack looks cross-viewpoint)."""
    n_notes = len(pop["beta"])
    Rn = np.zeros((K, n_notes)); Mn = np.zeros((K, n_notes))
    side = np.where(np.arange(K) % 2 == 0, 1.0, -1.0)
    gs = side * 0.6
    if kind in ("mimic", "sleeper") and H > 0:
        non_t = np.setdiff1d(np.arange(n_notes), targets)
        for k in range(K):
            hist = rng.choice(non_t, size=H, replace=False)
            Mn[k, hist] = 1
        rho_s = np.zeros(K) if kind == "mimic" else np.ones(K)
        Rn = draw_ratings(rng, pop["mu"], np.zeros(K), rho_s, gs, pop["beta"], pop["d"], Mn)
    Mn[:, targets] = 1
    Rn[:, targets] = 1.0
    return Rn, Mn
