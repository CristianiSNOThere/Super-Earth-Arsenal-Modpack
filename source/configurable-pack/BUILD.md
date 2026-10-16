# Selectable pack v2.2.2 source

Current source set: 24 independent switches and One True Flag's 29 damage presets,
defaulting to 300 normal / 150 durable. Stable pack GUID:
`bf6cb345-73c0-5b9b-a16c-38d490155842`.

## Inputs and build

`catalog.json` records ordered options, identities, Include paths and payload
hashes. `payloads/<id>/` holds accepted archives. `release-metadata.json` holds
public descriptions; repository README.md supplies the release ZIP README.
Canonical readable sources are under source/, including vg70-variable/.

From the HD2 Mods workspace root:

```powershell
python work/super-earth-arsenal-modpack-repo/tools/configurable-pack/build.py --release --incremental --output work/super-earth-arsenal-modpack-repo/Super-Earth-Arsenal-Modpack-v2.2.2.zip --evidence work/readability-correction-20261016/pack
```

Outputs are immutable; different bytes at an existing path are refused. Retain
all older releases/ZIPs. Use tagged historical catalogs to reproduce old versions.
Do not run old one-time prepare/import builders against the current source.

## v2.2.2 full-description correction

The user explicitly wants the original two-column README table and complete
prose, including before-and-after values wherever known. Simplify wording and
display precision only. Do not replace the structure with summaries, expanders
or lists of final values. player-guide.json now maps each of24option names to
its full prose description; refresh_public_copy.py refreshes catalog, public
metadata and the table consistently. It preserves all24row names and their
original order. The warning stays prominent. Gameplay files, option identities,
Includes and29Flag presets remain exact. Evidence and latest handoff:
work/readability-correction-20261016/. Reuse v2.2.0 gameplay acceptance and the
unchanged dependency/transaction baseline; only copy/import checks are needed.

Final v2.2.2 ZIP SHA256:
C5C87FE35A99813779DDA0C41CB55FEEFA988ADE92D9C8FA4433A25CC5B218B0,
29029191bytes. Only README.md and manifest.json differ from v2.2.1; all174other
entries are byte-exact. Manifest differs only in Version and descriptions.
The original24table row names/order, full prose and concrete before/after
comparisons pass. Eight real isolated Arsenal deploy/purge cases and actual
import/migration checks pass, preserving24selections and the Flag preset.

## Historical v2.2.1 public readability revision

source/configurable-pack/player-guide.json is the editable player-copy source.
Run tools/configurable-pack/refresh_public_copy.py before building after a copy
edit. This refreshes all24 catalog/Arsenal descriptions and the README gameplay
section together. The README uses short summaries, a glossary and24 expandable
stat lists. Arsenal receives the same plain-language bullets and explained values.
Display decimals are rounded and marked approximate; equivalent percentages and
degree conversions preserve the meaning. Every prior described stat remains
covered. The warning, option names/identities/Include paths and29Flag presets stay.

FinalZIP SHA256 E48C20A886A7183832EA6B187AAD446F8C57529540FCFFA09262141B81F85CE3,
29030823bytes. Independent old/new ZIP comparison proves only README.md and
manifest.json change; the manifest differs only in Version and descriptions.
All174other ZIP entries are byte-exact v2.2.0. Full49resource/dependency/type-order/
pureLua/collision audit passes. Eight real isolated Arsenal deploy/purge cases
pass, plus actual importer checks of all24 new multiline descriptions, both
enable-all preferences, all24 saved selections and a nondefault Flag choice
migrating from v2.2.0. No real user settings or deployment changed.

Evidence: work/readability-20261016/release-validation.json, pack/composition.json,
arsenal/incremental-arsenal.json and copy-import/public-copy-arsenal.json.
Reuse the exact v2.2.0 source/native/startup/user-gameplay baseline below. This
copy-only change does not require another mission or old combination matrix.

The builder checks the full resource inventory, pure-Lua archives and dependency
closure per option, contiguous FileData type groups, and all CPU/GPU/STREAM
payloads. The base union has 49 resources. A full selection with Flag
uses 30 main archives and 60 companions. Shared identical resources and complete
option closures establish static union compatibility; gameplay is a separate gate.

## Variable v0.1.1 delta and accepted evidence

Only Variable's gameplay archive changes from v2.1.0. Damage IDs542/543/544 move
to585/586/587. Ownership checks cover active native registry pointers and expected
row contents before/after transactions. Unknown owners refuse; rollback preserves
foreign rows/pointers. All modes use AP3/3/3/0; Total drops from AP4 to AP3.
Damage, rate, handling, stock Total self-injury and knockdown remain unchanged.

Workspace evidence under work/variable-auto-damage-20261015/ includes the
original read-only collision capture, typed consumer census, ten actual Lua
runtime scenarios with nine mode/rate pairs and two owners, collision refusals,
late/midtransaction changes and partial-write rollback. Focused pack checks cover
seven source/bytecode matches, four control cases in two orders and six isolated
real-Arsenal deployments plus preferences, old-option migration, slots and purge.
The old exhaustive migration matrix is reused, not repeated.

Fresh Rev2 startup 2026-10-15 22:03:07 Europe/Madrid: 62 modules loaded, zero failed,
Variable v0.1.1 Applied with 146 guarded fields, 13 dedicated Applied logs, and
26 exact main archive matches. Evidence: work/variable-auto-damage-20261015/
rev2-launch-20261015T200447Z/. User then says "yep udate repos", accepting gameplay
and authorizing publication. No new external process reads were used. Keep
startup, deployed-file/loader, gameplay and host/client evidence distinct.

Release changes only README and manifest Description fields from accepted Rev2.
Publication evidence is under work/release-variable-fix-20261015/ in the workspace.
Public metadata is checked through isolated Arsenal0.36.2 imports. Deployment
and settings remain user-controlled.

## Future changes and shared effects

Follow REGRESSION-POLICY.md. Test changed modules and actual shared consumers;
reuse exact baselines and broaden only for concrete affected paths. Numeric
profile IDs require native ownership checks and redirected-registry fixtures.

Existing named option selections survive upgrades; review selections on import.
Enable-all off initially selects the first option; enable-all on selects all24
and the first Flag preset. Disabled Flag suppresses its preset. Stable names,
GUID, order and Include paths remain unchanged.

Gas/Tenderizer share15-second Acid Storm duration, including weather. AC-8/Epoch
share animation resources; AC-8/JAR-5 share a FLAK explosion. Keep the former
individual repository's legacy releases and all pack release history intact.

## v2.2.0 Punisher addition — accepted Rev3

Append Punisher as option24, keeping all23 existing option definitions and162
baseline payload files exact. Readable accepted runtime and its source/planner/
registry tests are under source/punisher-plasma/. All12 nonimplementation resource
payloads match the user-accepted Rev10 individual. Only prepare/start scheduling
and exact post-companion validation change in the implementation Lua. Its two Lua resources use one pure-Lua
archive; the unchanged boot/loadout resource uses a separate non-Lua archive.
Both visual triplets remain byte-exact Rev10. No gameplay/native changes.

The user accepts Rev10 colour and both modes. Offline evidence under workspace
work/punisher-pack-integration-20261016/rev3/:58 actual source/native/prepare/registry/startup
cases, four actual startup-control cases (alone/full, forward/reverse; patch
adapters mocked), eight actual isolated Arsenal import/deploy/purge cases,
preferences/migration/profile-library/occupied-slot checks and full inventory.
Source helper execution occurs only in disposable fixture-owned allocations.
These fixture tests make no game-process or real deployment/settings changes.
Rev1's actual full-pack equipped launch failed before ship because source
installation was delayed behind companion readiness. Rev3 completes the guarded
source install first, retains bounded named waits for companion completion,
then revalidates epoch/registry/source/protected records with exact known peer
variants. Saved code and the dump identify game.dll+78861A with invalidFFFFFFFF
child-owner lookup. Native helper, guards, tuning, visuals and old23 payloads
remain intact. Its scheduling fixtures cover early7s/late30s initialization,
failed/never-ready peers and unknown/foreign/source/epoch drift after installation.

Run targeted tests from the workspace root:

```powershell
python work/super-earth-arsenal-modpack-repo/tools/configurable-pack/test_punisher.py outputs/punisher-pack-20261016/Super-Earth-Arsenal-Modpack-v2.2.0-Punisher-Rev3-Test.zip work/punisher-pack-integration-20261016/rev3/integration
python work/super-earth-arsenal-modpack-repo/tools/configurable-pack/test_runtime.py --incremental --focus-id punisher-plasma --evidence work/punisher-pack-integration-20261016/rev3/runtime
node work/super-earth-arsenal-modpack-repo/tools/configurable-pack/test_punisher_arsenal.cjs work/configurable-pack-20261015/arsenal-backend work/punisher-pack-integration-20261016/rev3/arsenal outputs/punisher-pack-20261016/Super-Earth-Arsenal-Modpack-v2.2.0-Punisher-Rev3-Test.zip
```

Fresh full24 Rev3 startup20:51:22local passes63loaded0failed/allselected modules,
13dedicatedApplied,33common values/0refused0errors,14Scorcher values,PunisherReady
and90exact imported/deployed files. Evidence:
work/punisher-pack-integration-20261016/launch-20261016T185252Z/report.json.
This first launch used another primary. Unchanged Rev3 equipped restart20:54:07
also passes63loaded0failed/13Applied/33common14Scorcher/all90exact with native
child20loaded60spares. Evidence: launch-20261016T185537Z/. User confirms ship and
both modes firing/reloading in a mission; required release gates are complete.
Release ZIP differs from accepted Rev3 only in README.md, adding the prominent
weapon/stat-editor compatibility warning requested by the user. All gameplay
files and the complete manifest are byte-exact Rev3; no new gameplay gate is
needed for this documentation-only change. Release SHA256:
9069B423C2118D9EF080123BE95284C04DFE4C4446C745FB1B6ACFA9C3434AD7.
Documentation delta/build/publication evidence: work/release-punisher-pack-20261016/.
Standalone remains disabled with the pack option. Switch primary before changing
Punisher packages. Preserve immutable candidates and all release history.

## v2.1.2 health compatibility

Gas Overhaul's exact health-profile recognition is shared by
source/startup-initialization/e54e34210bac937e.lua and source/gas-overhaul/sterilizer-entry.lua.
The sole gameplay archive delta is gas-overhaul/Addon/9ba626afa44a3aa3.patch_0.
Recognizes the complete eight-field health profile of export0182f499 with
fingerprint528db86c82f7bc91a8be; validates the complete normalized stock checksum
and preserves actual peer bytes for commit/rollback. Unknown/partial profiles
refuse. This is not arbitrary stat-editor support.

Offline28targeted actual validator/transaction cases cover both consumer orders,
unknown fields, partial writes, rollback and foreign mutations. Accepted startup
2026-10-16 11:47:47 Europe/Madrid:60loaded/0failed,13fresh dedicated Applied,
33common values/0refused/0errors,14Scorcher values,health export active13changes.
User then authorized repository publication. Full evidence under workspace
work/runtime-editor-compat-20261016/health-compat-rev1/ and
health-compat-launch-20261016T094940Z/. No independent live-memory read.
Historical gas-overhaul/build.py predates the canonical startup contract;
do not use it to regenerate this release. Use the selectable-pack builder.

## v2.1.3 Normal and Casual health profiles

Recognize only stock or either complete supplied eight-field health profile.
Normalize only for full stock checksum validation; retain actual transaction
bytes and disjoint Gas writes. Reject mixed, partial and unknown profiles.
The canonical Gas files remain identical; only its Lua archive changes.
58 actual health cases cover both export PATCH consumers in both orders,
rollback/foreign mutations/guards, plus a v2.1.2 Normal refusal reproduction.
Current Gas/SAI 45 and Gas validator 69 cases pass, including 16 peer subsets.
Unchanged startup/consumer contracts reuse baseline evidence.

Fresh Arsenal launch13:37:36local has62loaded/0failed,13fresh dedicated Applied,
33common values/0errors,14Scorcher values and78matching candidate gameplay files.
Neither Health Rework variant was present in that launch. It does not establish
fresh Normal-loaded or health gameplay acceptance. User was told this and then
explicitly authorized publication. Keep this limitation in internal evidence.
Workspace: work/runtime-editor-compat-20261016/health-normal-compat-rev1/,
health-normal-arsenal-launch-20261016T113941Z/ and work/release-health-normal-20261016/.
