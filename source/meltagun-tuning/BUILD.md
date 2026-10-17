# Meltagun and AMR tuning

Embed source-guard.lua after the shared runtime's fields/defaults declarations,
and resolve-fields.lua after add_hidden_part. The current runtime already has
these exact fragments and the guarded resolver/transaction hooks. Preserve the
stock beam 18 and damage 509 signatures and runtime-owned-value recognition.
The only added stock exception is beam 18's 15 m length. Its accepted target is
20 m; damage 509's second effect type and buildup are both zero. The first effect
(FlamerSlowed 67, strength 2) and every other row byte remain unchanged.

The existing Meltagun profile also retains handling 40. The existing AMR profile
retains handling 40 and sets capacity 10 and mags_max 10; starting 5 and supply 4
are untouched. Profile source mirrors live in source/startup-initialization/.

Workspace work/melt-amr-tuning-20261017/prepare.py patches the current accepted
runtime snapshot and propagates the common resource to all nine carriers, with
catalog hashes. Do not use historical startup generators. verify.py runs actual
shipped field resolution and the transaction manager in local fixture buffers,
including rollback and preservation of foreign changes. No game process access.
Follow REGRESSION-POLICY.md; fresh user startup/gameplay remains required.
