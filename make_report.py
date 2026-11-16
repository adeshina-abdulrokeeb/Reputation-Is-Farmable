import os, matplotlib
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

fd = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data/fonts/ttf')
for n, f in [('S', 'DejaVuSerif.ttf'), ('S-B', 'DejaVuSerif-Bold.ttf'), ('S-I', 'DejaVuSerif-Italic.ttf'), ('S-BI', 'DejaVuSerif-BoldItalic.ttf')]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(fd, f)))
pdfmetrics.registerFontFamily('S', normal='S', bold='S-B', italic='S-I', boldItalic='S-BI')

body = ParagraphStyle('b', fontName='S', fontSize=8.6, leading=11.6, alignment=TA_JUSTIFY, spaceAfter=4.5)
h1 = ParagraphStyle('h1', fontName='S-B', fontSize=10.5, leading=13, spaceBefore=8, spaceAfter=3)
h2 = ParagraphStyle('h2', fontName='S-BI', fontSize=9, leading=11, spaceBefore=4, spaceAfter=2)
title = ParagraphStyle('t', fontName='S-B', fontSize=15, leading=19, alignment=TA_CENTER, spaceAfter=4)
auth = ParagraphStyle('a', fontName='S', fontSize=9, leading=12, alignment=TA_CENTER, spaceAfter=8)
abs_ = ParagraphStyle('abs', parent=body, leftIndent=18, rightIndent=18, fontSize=8.4, leading=11.2)
cap = ParagraphStyle('c', fontName='S-I', fontSize=7.6, leading=9.6, alignment=TA_JUSTIFY, spaceAfter=7)
ref = ParagraphStyle('r', fontName='S', fontSize=7.6, leading=9.6, leftIndent=10, firstLineIndent=-10, spaceAfter=2)
small = ParagraphStyle('s', fontName='S', fontSize=7.8, leading=10, alignment=TA_CENTER)

P = lambda t, s=body: Paragraph(t, s)
S = []

S.append(P('Reputation Is Farmable: What Sleeper Accounts Cost Against Reputation-Weighted Bridging Rankers', title))
S.append(P('[Author name] &nbsp;·&nbsp; [Affiliation / independent researcher] &nbsp;·&nbsp; Solo entry<br/>'
           'AI x Epistemics Research Sprint (Apart Research), Track 2: Trust Infrastructure (with Track 4 elements)', auth))

S.append(P('<b>Abstract.</b> Bridging-based ranking systems such as X\u2019s Community Notes decide which context labels the public sees by '
           'requiring agreement from raters who usually disagree. A recent extension, Quality-Sensitive Matrix Factorization (QS-MF), '
           'also learns a per-rater reputation and is reported to resist coordinated attacks, but its authors note that reputation itself can be farmed. '
           'We test that concern directly. In a controlled simulation (800 honest raters, 400 notes, 6 seeds) we measure how many fake accounts and fake ratings '
           'it takes to push low-quality notes up the ranking under four scoring rules and three attacker strategies. QS-MF removes 81% of the displacement '
           'caused by 40 accounts that rate by ideology alone, but only 6% when the same 40 accounts first rate 20 notes carefully (\u201csleeper\u201d accounts). '
           'The fake-rating budget needed to move a note one standard deviation rises from about 977 (baseline) to 1,050 (QS-MF): +7%. '
           'A zero-prior variant that makes raters earn influence is immune to fresh and ideology-only accounts, yet shows a sharp threshold: '
           'with 10 history ratings per account the displacement is 0.09 SD, with 20 it is 0.82 SD. With 80 or more sleepers every variant gives no protection. '
           'We release the simulator and propose a cheap reputation-farming audit that platforms can run on public data.', abs_))

S.append(P('1. Introduction', h1))
S.append(P('Community Notes-style systems are the most visible deployed attempt at \u201ctrust infrastructure\u201d for claims: a note is shown only when raters who '
           'normally disagree both call it helpful. The design assumption is that agreement across the divide is expensive to fake. '
           'AI agents weaken that assumption. One operator can now run hundreds of accounts, each with a plausible, diverse rating history, at close to zero marginal cost. '
           'The question the Trust Infrastructure track poses, <i>which scoring techniques are hardest to cheat and easiest to audit?</i>, therefore needs a price tag: '
           'how many fake ratings does a given defence buy the attacker?'))
S.append(P('The most direct defence proposed so far is to weight raters by demonstrated quality tracking. QS-MF (Goyal, Arora &amp; Goel, 2026) adds one scalar per rater '
           'and reports attenuated displacement under coordinated attacks on real data. Its authors also state the obvious counter-move: an adversary could rate honestly on many notes to build reputation and then spend it on a few targets, '
           'and they list time-decayed reputation as future work. <b>We quantify that counter-move.</b> '
           'Our contributions: (i) a reproducible simulator of baseline and reputation-weighted bridging rankers; '
           '(ii) three attacker strategies (fresh, mimic, sleeper) and a cost-of-manipulation metric in fake ratings; '
           '(iii) evidence that reputation weighting is strongly protective against crude attackers but nearly neutral against sleepers, with a threshold effect in history length; '
           '(iv) an \u201cearn-it\u201d variant that raises the price but fails at scale, and a short list of defences this result motivates.'))

S.append(P('2. Related Work', h1))
S.append(P('Birdwatch/Community Notes ranks notes with a matrix factorization in which each rating is predicted from a global intercept, rater and note intercepts, and a product of one-dimensional rater and note viewpoint factors; a note\u2019s intercept is its score, with intercept regularization five times stronger than factor regularization, and a note is rated helpful at an intercept of at least 0.40 (Wojcik et al., 2022; open-source documentation). '
           'Displayed notes reduce reposting (Chuai et al., 2024; Slaughter et al., 2025). Vulnerability work includes rater bias and manipulation (Truong et al., 2025), estimate instability under rating surges (Chuai et al., 2026), outsized influence of hyperactive minorities (Nudo et al., 2026) and rater effort aversion (Wack et al., 2026). '
           'QS-MF replaces the additive note-quality term with &rho;<sub>i</sub>&beta;<sub>j</sub> and reports, on 45M real ratings, 26\u201340% fewer ratings needed for equal accuracy and 8\u201339% less displacement in semi-synthetic coordinated attacks, '
           'with attackers modelled as partisan, random or constant raters. <b>What is new here:</b> attackers that <i>spend effort on reputation</i> and a price in fake ratings. '
           'To our knowledge, from the sources we searched during the sprint, this has not been measured; we may have missed concurrent work. '
           'The Forethought essay \u201cAI for AI for Epistemics\u201d argues early epistemic tools accumulate trust whether or not they deserve it, which is why auditability must be a design requirement; our audit proposal in Section 5 follows that line.'))

S.append(P('3. Method', h1))
S.append(P('<b>World.</b> Ground truth: rating<sub>ij</sub> = 1[&mu; + a<sub>i</sub> + &rho;<sub>i</sub>&beta;<sub>j</sub> + &gamma;<sub>i</sub>&delta;<sub>j</sub> + &epsilon; &gt; 0.5], &mu;=0.45, &epsilon;~N(0, 0.25<super>2</super>). '
           '800 raters take one of two viewpoint sides (|&gamma;|~N(0.6, 0.2)); honest quality sensitivity &rho;~N(1, 0.25) clipped at 0.3; 10% of raters are noisy background raters with &rho;=0. '
           '400 notes with true quality &beta;~N(0, 0.35<super>2</super>) and viewpoint &delta;~N(0, 0.7<super>2</super>); each rater rates a random 8% of notes (about 64 ratings per note).'))
S.append(P('<b>Scoring rules.</b> All are alternating-least-squares fits of the same model with (a) <i>Baseline MF</i>: &rho;<sub>i</sub> fixed at 1 (the Community Notes structure); '
           '(b) <i>QS-MF</i>: &rho;<sub>i</sub> free with a ridge prior centred at 1; (c) <i>QS-MF, &rho;\u22641</i>: reputation cannot amplify; '
           '(d) <i>QS-MF, zero-prior</i>: prior centred at 0, so every account must earn influence. Regularization (sum-of-squares loss): note/rater intercepts 2.0, factors 0.4, &rho; 1.0. '
           'This matches the intercept-to-factor ratio of the production system but is not its exact scale (Appendix A). In clean data all four rules recover true quality with correlation 0.90\u20130.91.'))
S.append(P('<b>Attackers.</b> The attacker controls K sybil accounts, half on each viewpoint side so the attack looks cross-partisan, and wants 8 low-quality notes (true quality in the bottom quartile) to rank as helpful. '
           'Every sybil rates all 8 targets \u201chelpful\u201d. Three strategies differ only in history: <i>fresh</i> (no other ratings); '
           '<i>mimic</i> (H=20 history ratings by viewpoint only, i.e. &rho;=0: cheap fake diversity); <i>sleeper</i> (H=20 history ratings like a careful honest rater, &rho;=1). '
           'Cost = K \u00d7 (H + 8) fake ratings.'))
S.append(P('<b>Metrics.</b> Displacement = mean change of a target\u2019s note score, in standard deviations of that rule\u2019s clean note-score distribution. '
           'Protection = 1 \u2212 displacement(QS variant) / displacement(baseline). Cost-to-1SD = the K (and fake ratings) at which per-seed displacement first reaches 1.0, linearly interpolated, median over seeds. '
           '<b>Deviation from plan:</b> we first defined success as crossing the clean 90th-percentile note score (mirroring the system\u2019s roughly 10% helpful rate); '
           'across K\u2264160 this was almost never reached (flip rates 0\u201315%), so displacement is the primary metric. K \u2208 {10, 20, 40, 80, 160}, 6 seeds, 95% bands are \u00b11.96 SE across seeds. '
           'A second sweep fixes K=40 and varies H \u2208 {0, 5, 10, 20, 40}.'))

S.append(P('4. Results', h1))
S.append(Image('fig1.png', width=6.9 * inch, height=6.9 * inch * 0.318))
S.append(P('<b>Figure 1.</b> Displacement of target notes against number of sybil accounts, three attacker strategies (H=20 for mimic and sleeper). Dotted line: 1 SD. Bands: 95% across 6 seeds.', cap))

S.append(P('<b>R1. Crude attackers: reputation weighting works.</b> Against mimic accounts QS-MF protection is 89%, 86% and 81% at K=10, 20, 40 (\u00b14 to \u00b19), '
           'and the cost to reach 1 SD rises from 950 to 2,338 fake ratings (about 2.5\u00d7). Mimic accounts end with low reputation (mean &rho; 0.13\u20130.19 for K\u226440). '
           'Fresh accounts barely move any rule (at most 0.99 SD at K=160), so \u201cjust create accounts\u201d is not the threat.'))
S.append(P('<b>R2. Sleepers erase most of the protection.</b> The same 40 accounts with 20 careful history ratings each reach 1.07 SD under QS-MF against 1.14 under baseline: protection falls to 6% (\u00b15). '
           'At K=10 and 20 protection is 43% and 33%; at K\u226580 it is \u22124% to 1%. Cost to 1 SD: 977 fake ratings (baseline), 1,050 (QS-MF), 1,007 (\u03c1\u22641). '
           'Capping reputation does not help (Table 1).'))

rows = [['Attacker', 'Scoring rule', 'K for 1 SD', 'Fake ratings', 'Protection at K=40'],
        ['Mimic', 'Baseline MF', '34', '950', '\u2014'],
        ['Mimic', 'QS-MF', '83', '2,338', '81%'],
        ['Mimic', 'QS-MF, \u03c1\u22641', '85', '2,378', '84%'],
        ['Mimic', 'QS-MF, zero-prior', '>160', '>4,480', '100%'],
        ['Sleeper', 'Baseline MF', '35', '977', '\u2014'],
        ['Sleeper', 'QS-MF', '37', '1,050', '6%'],
        ['Sleeper', 'QS-MF, \u03c1\u22641', '36', '1,007', '3%'],
        ['Sleeper', 'QS-MF, zero-prior', '52', '1,442', '46% (\u00b127)']]
t = Table(rows, colWidths=[0.9 * inch, 1.6 * inch, 0.9 * inch, 1.0 * inch, 1.5 * inch])
t.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'S', 7.6), ('FONT', (0, 0), (-1, 0), 'S-B', 7.6),
                       ('LINEABOVE', (0, 0), (-1, 0), 0.8, colors.black), ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
                       ('LINEBELOW', (0, -1), (-1, -1), 0.8, colors.black), ('LINEBELOW', (0, 4), (-1, 4), 0.3, colors.grey),
                       ('ALIGN', (2, 0), (-1, -1), 'CENTER'), ('TOPPADDING', (0, 0), (-1, -1), 1.6), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.6)]))
S.append(KeepTogether([t, P('<b>Table 1.</b> Cost of moving target notes 1 SD (median over 6 seeds; K interpolated; fake ratings = K \u00d7 (H+8), H=20). Zero-prior under mimic never reached 1 SD for K\u2264160 (all 6 seeds censored). Fresh-account rows omitted: no rule except \u03c1\u22641 reached 1 SD (it reached it at K\u2248151 in 2 of 6 seeds).', cap)]))

S.append(Image('fig2.png', width=5.6 * inch, height=5.6 * inch * 0.37))
S.append(P('<b>Figure 2.</b> K=40 sybils, varying history length H. Left: displacement. Right: mean fitted reputation of the sybils. Solid: sleeper; dashed: mimic.', cap))

S.append(P('<b>R3. A reputation cliff.</b> For the zero-prior rule, sleeper reputation and displacement are near zero up to H=10 (displacement 0.09 SD, &rho;=0.10) and then jump: H=20 gives 0.82 SD (&rho;=0.79) and H=40 gives 1.32 SD (&rho;=1.23, above the baseline\u2019s 1.25). '
           'Standard QS-MF has no cliff, only a ramp: 0.25, 0.52, 0.79, 1.10, 1.26 SD for H=0, 5, 10, 20, 40. For mimic accounts under QS-MF the opposite holds: more ideology-only history makes them worse (displacement 0.32 \u2192 0.14 SD, &rho; 0.49 \u2192 0.10 for H=5 \u2192 40), '
           'so honest-looking effort, not mere account age, is what unlocks influence.'))
S.append(P('<b>R4. Consensus capture at scale.</b> Protection collapses as K grows even without sleeping: mimic protection falls 81% \u2192 52% \u2192 6% at K=40, 80, 160, and mimic reputation climbs from 0.19 to 0.87 (QS-MF). '
           'Our interpretation, not tested here, is that when sybils supply a large share of the ratings on the targets, their ratings agree with the (shifted) consensus, which the model reads as quality tracking. '
           'Zero-prior is the only rule that stays protected against mimic accounts at every K (98% at K=160), but against sleepers it is <i>worse</i> than baseline at K\u226580 (\u22129% at K=80), a side effect of fitting the sybil block as a high-reputation majority.'))

S.append(P('5. Discussion', h1))
S.append(P('<b>What the numbers say.</b> Reputation weighting prices out attackers who are lazy about reputation (R1) and barely taxes those who are not (R2): the sleeper pays about 20 history ratings per account, a one-off cost that an automated agent can amortise across many campaigns. '
           'The honest framing is a <i>price</i>, not a verdict: 1,050 fake ratings against 977 is cheap for a software agent. '
           '<b>Implications for platform design.</b> (1) Evaluate reputation defences against sleepers, not only partisan, random or constant raters. '
           '(2) Reputation should be measured on notes whose scores had stabilised <i>before</i> the account touched the target, so attackers cannot grade themselves; R4 suggests this matters at scale. '
           '(3) Zero-prior designs trade early-note speed for a cliff, so an audit should probe the cliff location (here between 10 and 20 history ratings) rather than average over it. '
           '(4) Since the data and code of such systems are public, a platform can run a <b>reputation-farming audit</b> continuously: inject synthetic sleeper blocks of increasing size into a replay of recent ratings, and publish the resulting cost-to-1SD curve as a trust signal that outsiders can re-run. '
           'Our simulator is a working prototype of that audit.'))

S.append(P('6. Limitations and Dual-Use / Ethical Considerations (summary; full appendix follows references)', h1))
S.append(P('This is a simulation of a simplified model, not an attack on any platform; it establishes relative costs under stated assumptions, not real-world rates. '
           'The main limits are: dense synthetic data with uniform participation, no rater-targeting by the platform\u2019s routing, no verification filters used in production, ratings in {0,1}, only 6 seeds, one population size, and an attacker who knows the model. See Appendix A.'))

S.append(P('References', h1))
refs = [
    'Chuai, Y., et al. (2024). Did the roll-out of Community Notes reduce engagement with misinformation? <i>CSCW</i>.',
    'Chuai, Y., Lenzini, G., Pr\u00f6llochs, N. (2026). Consensus stability of Community Notes on X. arXiv:2601.14002.',
    'Cotton-Barratt, O., Finnveden, L. (2026). AI for AI for Epistemics. Forethought.',
    'Goyal, M., Arora, N., Goel, A. (2026). Quality-Sensitive Matrix Factorization for Community Notes: Towards Sample Efficiency and Manipulation Resistance. arXiv:2604.11224.',
    'Nudo, J., Nemmi, E. N., Loru, E., Mei, A., Quattrociocchi, W., Cinelli, M. (2026). Hyperactive minority alter the stability of Community Notes. (As cited in Goyal et al., 2026.)',
    'Slaughter, I., Peytavin, A., Ugander, J., Saveski, M. (2025). Community Notes on X reduces engagement with misleading posts. <i>PNAS</i> 122(38).',
    'Truong, B. T., Wu, S., Flammini, A., Menczer, F., Stewart, A. J. (2025). Community notes are vulnerable to rater bias and manipulation. arXiv:2511.02615. (Cited as listed in Goyal et al., 2026; not independently read.)',
    'Wack, M., Warren, P., Alam, M. (2026). The laziness of the crowd: Effort aversion among raters risks undermining the efficacy of X\u2019s Community Notes program. arXiv:2603.11120. (As cited in Goyal et al., 2026.)',
    'Wojcik, S., Hilgard, S., Judd, N., et al. (2022). Birdwatch: Crowd wisdom and bridging algorithms can inform understanding and reduce the spread of misinformation. arXiv:2210.15723.',
    'X Corp. Community Notes: Note ranking algorithm (open-source documentation). github.com/twitter/communitynotes.',
]
for r_ in refs:
    S.append(P(r_, ref))

S.append(PageBreak())
S.append(P('Appendix A. Limitations and Dual-Use / Ethical Considerations (required)', h1))
S.append(P('<b>What the result establishes.</b> In a controlled model where ratings follow the factorization the scorers assume, reputation weighting changes the attacker\u2019s required fake-rating budget by a factor of about 2.5 for ideology-only accounts and about 1.07 for accounts that rate carefully first, at 40 accounts and 20 history ratings. '
           'The qualitative ordering (mimic \u226b sleeper in cost under QS-MF; cliff under zero-prior; loss of protection at large K) held in every aggregate we report.'))
S.append(P('<b>What it does not establish.</b> (1) Real raters are not generated from the model; real QS-MF gains on 45M ratings were reported by its authors and we did not replicate them. '
           '(2) Our scale (800 raters, 400 notes, ~64 ratings/note) is orders of magnitude below production; K=40 here is 5% of raters, which is a very different share from 40 accounts among hundreds of thousands. '
           'The K-dependence should be read as a share, not an absolute number. (3) We use sum-of-squares regularization chosen to match the production intercept-to-factor ratio, not its exact scale. '
           '(4) Production systems add filters (minimum rating counts, rater-eligibility rules, pseudo-rating sensitivity checks, tag outlier thresholds) not simulated here and which may raise attacker cost. '
           '(5) The 90th-percentile \u201chelpful\u201d criterion was nearly never met; conclusions rest on displacement, not on label flips. '
           '(6) Six seeds with one parameter setting; bands are standard errors across seeds, and some cells (e.g. zero-prior at K=40, \u00b127 points) are noisy. '
           '(7) Attacker knowledge: we assume the attacker knows the scoring rule and rating mix; this is realistic for open-source systems but is a worst case. '
           '(8) The consensus-capture explanation in R4 is a hypothesis. (9) We did not run LLM agents as raters; \u201csleeper\u201d here is a scripted rating policy, so claims about LLM-driven sybils are motivation, not a finding.'))
S.append(P('<b>Dual-use.</b> The result could guide an attacker toward reputation farming. We judge the risk low and the defensive value higher: the idea is explicitly flagged as an open concern by the QS-MF authors, the scoring code and data of the studied platform are public, our model is a toy that does not transfer into an operational recipe, and we did not touch any live platform. '
           'We pair every attack result with design implications and a defender-side audit. We do not publish account-creation or evasion tooling.'))
S.append(P('<b>Personal data.</b> None. All data is synthetic; no real users, ratings or accounts were used.'))
S.append(P('<b>Disclosure of prior work and AI assistance.</b> All simulator code and experiments were written during the sprint. Prior work used: the published Community Notes model structure, and the QS-MF model idea from Goyal et al. (2026), reimplemented independently. '
           'AI tools assisted with code, analysis scripts and drafting; the numbers reported are outputs of the released scripts.'))
S.append(P('Appendix B. Reproducibility', h1))
S.append(P('Files: bridge.py (population, ALS fits for four scoring rules, attack builder), run.py (main experiment), run_h.py (history sweep), analyse.py (tables and figures). '
           'Seeds 100\u2013105 for populations; attack seeds are deterministic functions of seed and K. Runtime about 10 minutes on one CPU core. Python 3.12, numpy 2.5.4. '
           'Key hyperparameters: 30 ALS iterations; regularization LAM_A=LAM_B=2.0, LAM_G=LAM_D=0.4, LAM_RHO=1.0; rho normalised to mean 1 after fitting for QS variants (as in Goyal et al., 2026); '
           'rho clipped at 0 for all QS rules and at 1 for the capped rule. Sybils: K/2 per side, viewpoint factor \u00b10.6 when generating history ratings.'))

def foot(c, d):
    c.setFont('S', 7); c.drawCentredString(letter[0] / 2, 0.45 * inch, str(d.page))

doc = SimpleDocTemplate('report.pdf', pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch, topMargin=0.7 * inch, bottomMargin=0.75 * inch,
                        title='Reputation Is Farmable', author='[Author name]')
doc.build(S, onFirstPage=foot, onLaterPages=foot)
