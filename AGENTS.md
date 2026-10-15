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

## Current release: selectable pack v2.0.0 (2026-10-15)

The user approved a single selectable package and automated subset testing. New
candidate build inputs are under `source/configurable-pack/`, with tools under
`tools/configurable-pack/`; read `source/configurable-pack/BUILD.md` first. This
repository is the home for new selectable-pack work. The user accepted Rev3 and
requested v2.0.0 publication on2026-10-15. The old individual repo is repurposed
for standalone runtime/weapon projects, including Punisher Plasma. Preserve its
22earlier individual releases and all pack history. Current handoff is
`work/configurable-pack-20261015/continuation-20261015.md` relative to the HD2 Mods
workspace. The local automated checks do not replace fresh startup/gameplay gates.

Every new mod in this set, including Arc Thrower and Autocannon work, must follow the current startup contract in `source/startup-initialization/` and the companion gate in `source/scorcher-ar/runtime.lua`. Use bounded waits with named failures; retain exact supported peer-order checks, fail-closed shared-table validation, and rollback. Update supported peer values when a new mod edits a shared table.

Keep each mod's identity and private resource keys distinct. Shared resource keys must have byte-identical payloads in all individual packages that include them. Keep Shared Loader Lua in a pure-Lua archive. Check the new individual ZIP against the complete current set for differing resource collisions and relevant startup orders, and verify a fresh startup before release. Make the matching mega pack addition from the same sources. Startup evidence does not prove gameplay compatibility for every combination.

Keep deployment and Arsenal settings with the user. Verify a published replacement before removing only its superseded individual release. Preserve mega pack release history.

Public release descriptions and player-facing READMEs must explain the complete player-visible changes without implementation details, test history, failed prototypes, or statements about which tests were or were not run. Keep validation evidence in internal work notes.

## Latest local evidence: full Rev3 startup (2026-10-15)

Selectable v2.0.0 Rev3 full22 startup at16:16:44 Europe/Madrid is verified:
61loaded/0failed, all22final states,75exact deployed files, Flag300/150preset
loaded before Flag. Evidence under the workspace's
`work/configurable-pack-20261015/full-rev3-launch-20261015T141905Z/`.
The user subsequently accepted the result and requested publication. Keep the incremental policy;
no repeat of the exhaustive migration suite or rebuild is needed for this launch.
