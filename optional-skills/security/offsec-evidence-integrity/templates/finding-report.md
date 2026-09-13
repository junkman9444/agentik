# Finding Report Template

## Title / Affected Asset

`<short vulnerability title>` — `<endpoint / hostname / asset>`

## Confidence

`Confirmed` | `Inferred / Inconclusive — NOT DEMONSTRATED`

Confirmed requires an actual observed behavior change (data extracted, code executed,
access escalated, or a clean binary-choice payload comparison like `' AND 1=1--` vs.
`' AND 1=2--` with a differing, reproducible response). A template match with no
observed behavior change is Inferred at best.

## Evidence

```
$ <exact command, real arguments>
<exact real output — full or a clearly-marked excerpt (grep/jq), never invented>
```

Timestamp: `<UTC timestamp of the actual run>`
Raw output file (if too large to inline): `results/<path>`

## Impact

Plain statement of what this actually allows an attacker to do, grounded in the
evidence above — not a generic CWE description.

## Remediation

Concrete fix guidance for this specific finding (not just "sanitize input").

## Detection Opportunity

What a defender's logging/monitoring/WAF rule could have caught this attempt, if
relevant to the engagement's reporting requirements.
