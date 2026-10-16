# Compatibility rule for future mods

## Incremental regression rule

For future selectable-pack changes, follow
`source/configurable-pack/REGRESSION-POLICY.md`. Test changed code/options and
actual shared consumers, reuse exact baseline results, and expand only for a
concrete affected path or baseline change. Do not rerun the full migration
combination matrix or ask for manual testing of every existing weapon. Keep
resource/dependency audits, exact guards/rollback and fresh startup/gameplay
gates. Build individual ZIPs only when separately maintaining legacy individual
releases; a selectable-pack-only change does not require 22 individual builds.

## Current release: selectable pack v2.1.2 (2026-10-16)

Current set: 23 independent mod switches and 29 Flag presets. Variable v0.1.1
fixes redirected damage profiles and uses AP3 in Auto, Volley and Total.
Canonical Variable source is under `source/vg70-variable/`. Keep private numeric
ID ownership checks against native lookups as well as serialized tables; refuse
redirected lookups and preserve foreign pointers/rows. Include registry collision
and rollback fixtures. Read source/configurable-pack/BUILD.md and REGRESSION-POLICY.md.
The former individual repository hosts standalone runtime projects; retain all
legacy releases and ZIPs. This is a selectable-pack update only.

Every new mod in this set, including Arc Thrower and Autocannon work, must follow the current startup contract in `source/startup-initialization/` and the companion gate in `source/scorcher-ar/runtime.lua`. Use bounded waits with named failures; retain exact supported peer-order checks, fail-closed shared-table validation, and rollback. Update supported peer values when a new mod edits a shared table.

Keep each mod's identity and private resource keys distinct. Shared resource keys must have byte-identical payloads in all individual packages that include them. Keep Shared Loader Lua in a pure-Lua archive. Check the new individual ZIP against the complete current set for differing resource collisions and relevant startup orders, and verify a fresh startup before release. Make the matching mega pack addition from the same sources. Startup evidence does not prove gameplay compatibility for every combination.

Keep deployment and Arsenal settings with the user. Verify a published replacement before removing only its superseded individual release. Preserve mega pack release history.

Public release descriptions and player-facing READMEs must explain the complete player-visible changes without implementation details, test history, failed prototypes, or statements about which tests were or were not run. Keep validation evidence in internal work notes.

## Latest accepted startup

Variable Rev2 launch 2026-10-15 22:03:07 Europe/Madrid: 62 loaded, zero failed.
Variable v0.1.1 Applied with 146 guarded fields; 13 dedicated Applied logs and
26 exact main archives. Workspace evidence:
`work/variable-auto-damage-20261015/rev2-launch-20261015T200447Z/`.
User subsequently says "yep udate repos", accepting gameplay and authorizing
publication. No additional external process capture was performed. Offline,
startup, deployed-file/loader selection and user gameplay evidence are distinct.
Publication and continuation evidence: `work/release-variable-fix-20261015/`.

## v2.1.2 health-profile compatibility

Preserve the exact known health-export profile and full normalized stock checksum;
unknown/partial profiles must refuse. Only Gas's validator changes from v2.1.1.
Canonical Gas text matches source/startup-initialization/e54e34210bac937e.lua and
source/gas-overhaul/sterilizer-entry.lua. Keep native Gas write targets and peer
readiness statuses unchanged. Historical Gas builders are not current pack builders.
Fresh accepted startup11:47:47local passes60loaded/0failed and13dedicated Applied
with health export active. User explicitly authorizes publication afterwards.
