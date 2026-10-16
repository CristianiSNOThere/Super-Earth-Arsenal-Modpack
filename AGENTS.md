# Compatibility rule for future mods

## Accepted v2.2.0 Punisher addition

Rev1 failed before ship with Punisher equipped: game.dll+78861A used an invalid
FFFFFFFF child-owner lookup while source installation waited for companions.
Rev3 installs the fully guarded source before companion completion, then waits
with the same named/bounded peer checks and revalidates exact protected variants.
No native helper, gameplay data, visual resources or old23 payloads change.
58 focused cases and eight isolated Arsenal cases pass. Fresh full24 Rev3 startup
20:51:22 local passes63loaded/0failed,13Applied,33common/14Scorcher values,
PunisherReady and all90files exact. Equipped restart20:54:07 also passes the same
full-set gates, with child20loaded/60spares. User explicitly confirms ship and
both mission modes fire/reload correctly and authorizes publication after gates.
Evidence: work/punisher-pack-integration-20261016/launch-20261016T185252Z/ and
launch-20261016T185537Z/. Release differs from accepted Rev3 only in README.md,
which adds the user-requested prominent weapon/stat-editor compatibility warning.
Every gameplay file and the manifest remain byte-exact Rev3.

Source contains24 options. Preserve the separate offline, startup and user
gameplay evidence; a selected-set startup is not universal gameplay proof.
Workspace handoff: work/punisher-pack-integration-20261016/continuation.md.
Keep all old23 option definitions and162 payload files exact. Punisher Lua and
boot/loadout resources are separate archives;12nonimplementation resource payloads
match acceptedRev10; the initialization change is described above. FileData type groups must remain contiguous, counts/indices exact,
and resource collision checks include CPU/GPU/STREAM. The native constructor
overflows on interleaved types. Preserve the Rev9 fix and its regression fixture.

## Incremental regression rule

For future selectable-pack changes, follow
`source/configurable-pack/REGRESSION-POLICY.md`. Test changed code/options and
actual shared consumers, reuse exact baseline results, and expand only for a
concrete affected path or baseline change. Do not rerun the full migration
combination matrix or ask for manual testing of every existing weapon. Keep
resource/dependency audits, exact guards/rollback and fresh startup/gameplay
gates. Build individual ZIPs only when separately maintaining legacy individual
releases; a selectable-pack-only change does not require 22 individual builds.

## Current release: selectable pack v2.2.0 (2026-10-16)

Current set:24 independent mod switches including Punisher Plasma and29Flag presets.
The previous v2.1.3 baseline has23 switches. Variable v0.1.1
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

## v2.1.3 exact Normal and Casual health compatibility

Preserve the two complete known profiles and the full normalized stock checksum.
Unknown/partial/mixed profiles refuse; health bytes and transaction contracts stay
unchanged. Only Gas validation changes from v2.1.2. Canonical Gas source mirrors
and archived payload must match. 58 targeted health cases and45/69shared cases pass.
Latest startup13:37:36local is62loaded/0failed/13Applied with the candidate but no
Health Rework installed in that Arsenal profile. Normal-loaded startup/gameplay
remain untested. User was informed, then authorized repository publication.
