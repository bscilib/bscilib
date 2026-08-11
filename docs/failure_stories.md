# MIABS failure-story dossier

This is a living document. Its purpose is to record, for each checklist item,
the failure mode that justifies the item's presence.

The admission test for a checklist item is that its absence has demonstrably
produced a replication failure, a hidden confound, or an uninterpretable result.
One entry per item follows. The entries below are stubs, to be filled in with
citations and cases during the week-1 audit of three papers.

| Item | Failure mode | Exhibit |
|---|---|---|
| A2, E2 | A parameter confound is discovered only during fitting, so that estimates wander along a ridge while the fits themselves look stable | Exhibit needed. `python/bscilib/identifiability/poc.py` model 4 reproduces the structure synthetically, but a real published case would be stronger |
| A3 | A latent construct is smuggled into a prediction, so that claims are stated in unmeasurable quantities | The response-strength literature serves as the historical exhibit |
| B1, C2 | Hand-rolled VI implementations diverge at timer-response coincidences and at the arranged-versus-obtained distinction | Cross-laboratory simulation disagreement; to be documented in the audit |
| C1 | Time-step sensitivity is presented as a theoretical effect | To be documented in the audit |
| D2, D3 | Figures cannot be regenerated from the deposited materials | To be quantified by the retrospective audit paper |
| F3 | Tuned results are presented as emergent discoveries | To be documented in the audit |
