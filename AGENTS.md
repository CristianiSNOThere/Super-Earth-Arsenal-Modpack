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

## Current release: selectable pack v2.1.0 (2026-10-15)

Current set:23 independently selectable mods, including BR-14 Adjudicator Heavy
Battle Rifle at480RPM, and the unchanged29-preset Flag dropdown. User accepts
Rev2 and explicitly requests publication. Canonical authored Adjudicator source
is under `source/adjudicator-heavy/`; catalog/payloads and build tools remain
under `source/configurable-pack/` and `tools/configurable-pack/`. Read BUILD.md
and REGRESSION-POLICY.md before changes. The former individual repository hosts
standalone runtime projects; keep its22legacy releases and all pack history.
No need to build a new individual package for a selectable-pack-only addition.

Every new mod in this set, including Arc Thrower and Autocannon work, must follow the current startup contract in `source/startup-initialization/` and the companion gate in `source/scorcher-ar/runtime.lua`. Use bounded waits with named failures; retain exact supported peer-order checks, fail-closed shared-table validation, and rollback. Update supported peer values when a new mod edits a shared table.

Keep each mod's identity and private resource keys distinct. Shared resource keys must have byte-identical payloads in all individual packages that include them. Keep Shared Loader Lua in a pure-Lua archive. Check the new individual ZIP against the complete current set for differing resource collisions and relevant startup orders, and verify a fresh startup before release. Make the matching mega pack addition from the same sources. Startup evidence does not prove gameplay compatibility for every combination.

Keep deployment and Arsenal settings with the user. Verify a published replacement before removing only its superseded individual release. Preserve mega pack release history.

Public release descriptions and player-facing READMEs must explain the complete player-visible changes without implementation details, test history, failed prototypes, or statements about which tests were or were not run. Keep validation evidence in internal work notes.

## Latest accepted startup

Rev2 full23 launch18:59:51 Europe/Madrid:62loaded/0failed, all23final mod states,
Adjudicator480RPM,78exact deployed files and installedmanifest. Workspace evidence:
`work/adjudicator-heavy-20261015-rev2/full-adjudicator-rev2-launch-20261015T170057Z/`.
User subsequently says "Perfect. Let us update the repo.", accepting the result
and authorizing publication. The earlier muzzle-flash report was withdrawn by
the user as a fluke; no visual changes were made. Keep offline/startup/loaded/
gameplay evidence distinct. Publication evidence/latest handoff is under
`work/release-adjudicator-20261015/` in the HD2 Mods workspace.
