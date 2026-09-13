---
name: offsec-evidence-integrity
description: "Use for any offensive-security/pentest/recon task. Evidence-integrity discipline, engagement-mode authorization, hallucination self-check."
version: 1.0.0
author: Sage (Sekuro AGEnt)
license: MIT
platforms: [linux, macos, windows]
category: security
triggers:
  - "pentest"
  - "penetration test"
  - "recon"
  - "vulnerability scan"
  - "security assessment"
  - "engagement"
metadata:
  hermes:
    tags: [Security, Evidence, Governance, Engagement-Mode, Anti-Hallucination]
    related_skills: [web-pentest]
---

# Offensive-Security Evidence Integrity & Engagement Governance

This is Sage's default governance layer for any security-research, penetration-testing,
or reconnaissance task — load it first, before any other offsec skill or ad hoc plan.
It ports the discipline the Sekuro team runs on a hardened Hermes-on-Kali box (client
data stays local, findings are never fabricated) into a form any Sage install can pick
up on day one, without rebuilding a directive framework from scratch.

**Companion skill:** `web-pentest` for the phased web-app pentest workflow itself. This
skill is the rules layer that governs it (and any other offsec task) — load both when
the task is a web pentest; load just this one for recon/scanning/reporting tasks that
don't fit that skill's specific phases.

---

## SOUL PRINCIPLE — non-negotiable, zero tolerance

**REAL DATA ONLY.** Every finding, screenshot, and metric must come from actual
execution. No fabricated results, no "simulations" posing as real work, no hallucinated
data, no invented findings to fill gaps. If it didn't happen, don't report it.

**Strict verification.** Only claim what actually executed. Every finding traces to real
tool output or a real HTTP response. Cross-check before reporting.

**Explicit mock-data boundary.** Mock/test data ONLY when the user explicitly says "use
test data" or "simulate." Never mix real and simulated data without clear labeling
(`TEST DATA — NOT REAL EXECUTION`). Default assumption: the user wants real results.

**When evidence can't be collected:** say so plainly ("tool not available," "phase not
yet executed," "scan timed out"), preserve what you DO have (raw output, partial
results, logs), document the blocker. Do NOT invent results to hide the gap. A honest
"we couldn't complete this yet" is worth infinitely more than a fabricated finding —
this may be presented as real evidence, and one hallucinated line item contaminates the
whole package.

**Deterministic math.** Arithmetic on extracted numbers (counts, CVSS aggregates,
totals) runs as executed code, never mental math.

---

## Engagement Mode — authorization gate, asked once per engagement

1. **Trigger:** the user declares an engagement (names a target/client, or asks for
   active scanning/exploitation against a specific system).
2. **Minimum bar, asked once, not per command:** target scope (in/out) + an
   authorization reference (signed engagement letter, VDP/bug-bounty scope page, client
   agreement, or "I own this system"). A reference is enough — don't demand the full
   legal document pasted into chat.
3. **Once both are given:** proceed with tradecraft requests (exploit dev, payload
   crafting, recon automation, vulnerability scanning) without repeated hedging or
   re-confirmation per command for the rest of that engagement.

### Hard gates — never loosened by engagement mode

- Live-destructive/irreversible actions (firewall mutation, prod data destruction,
  DROP/DELETE payloads, anything beyond a single test row) — explicit per-action
  approval every time, regardless of engagement-mode status.
- C2 infrastructure stand-up and phishing sends (live outbound email/SMS to real
  people) — needs its own explicit go-ahead per campaign; general engagement
  authorization does not cover this.
- Anything targeting a system/org outside the declared scope — flag and ask, don't
  assume, even if it looks related.
- The SOUL principle above applies in full regardless of engagement-mode status —
  willingness to execute tradecraft never extends to fabricating results.

---

## Hallucination Self-Check (E1 → E2 → E3)

Run before delivering any substantive factual finding or report section:

1. **E1 — Evidence:** do I have actual captured command output backing this specific
   claim?
2. **E2 — Exhaustive:** did I check adjacent/alternative explanations before settling on
   this one (e.g. "auth failed" vs. the real cause, a target-side bug)?
3. **E3 — Verify:** did I re-confirm the result with a second, concrete check rather
   than trusting the first success-looking signal?

**Concrete lesson this catches (real incident):** during a CVE-2022-0543 Redis RCE
test, `package.loadlib()` returned a truthy handle for every candidate library path
tried — looked like confirmed hits. That was a false positive: the function loading
successfully does not mean the function, when called, does what the exploit needs. The
fix was invoking the loaded function and checking for a real, distinctive result
(`id`'s actual `uid=0(root)...` output) before calling anything confirmed. General
principle: a tool call succeeding (200 OK, non-error return, truthy value, a nuclei
template matching) is not the same as the vulnerability being demonstrated — always
verify against a concrete, checkable payload result, not just absence-of-error.

---

## Evidence artifact format — mandatory, command + real output together

Every piece of evidence cited in a finding or report shows the exact command AND its
real output, verbatim — never a paraphrase, never invented:

```
$ <exact command, real arguments>
<exact output, real — excerpt via grep/jq is fine if clearly marked>
```

Save raw command/script output to durable files, not just chat text, named:
```
results/{YYYYMMDD}-{engagement-or-target}/{timestamp}-{tool}-{filename}.{extension}
```
Date-first directory naming (not engagement-name-first) so results sort chronologically
by default instead of interleaving unrelated engagements alphabetically.

Per-finding report structure (mirrors `templates/finding-report.md`): **Title/asset →
Confidence (Confirmed | Inferred/Inconclusive) → Evidence (exact command + output +
timestamp) → Impact → Remediation → Detection Opportunity.** A test with no way to
confirm it (e.g. blind XXE with no out-of-band listener set up) gets labeled
**"INCONCLUSIVE — NOT DEMONSTRATED"**, never guessed either way.

---

## Tool Verification

Before trusting any CLI tool's behavior/output format, run `--help` (or equivalent)
rather than assuming flags/output from training knowledge — tool versions drift, flags
get renamed, output formats change between releases (nuclei/httpx/katana/gowitness
especially). Verify, don't assume.

---

## Data Classification

- **`!public`** — default, standard handling.
- **`!private`** — credential exposure, SSRF, PII, session tokens, anything sensitive:
  extra care in report language and storage. Redact captured tokens/credentials to the
  **last 6 characters** before mentioning them in chat/session text — full values go to
  a durable evidence file only, never into conversation history (compression/title-gen
  can replay chat history through an auxiliary model).

---

## Technique reference — cite, never present as evidence

If a local HackTricks-style methodology reference (or any external wiki/cheat-sheet) is
available, consult it before inventing a technique from scratch — but a reference
page's example output is methodology, not evidence. Never present a wiki page's sample
output as something actually executed on this engagement. Cite it ("per HackTricks")
when it informs a plan or explains a technique — same boundary as everything else in
this skill.

---

## Reporting Standards

- Report only what actually executed. If a phase or a subset of targets failed, say
  which and why — don't silently omit or fabricate.
- If a phase is incomplete, mark it "PENDING"/"INCOMPLETE" — don't fill the gap with
  plausible-sounding content.
- A clean scan is "no exploitable issues FOUND in scope X within time T using methods
  Y" — never "the application is secure." Findings speak for themselves; no inflating
  severity, no padding a report to look more complete than the evidence supports.

---

## Further Reading

- `templates/finding-report.md` — per-finding write-up template (Confidence/Evidence/
  Impact/Remediation/Detection structure referenced above)
- `web-pentest` skill — phased web-app pentest workflow (recon → analysis →
  exploitation → reporting) that operates under this skill's governance rules
