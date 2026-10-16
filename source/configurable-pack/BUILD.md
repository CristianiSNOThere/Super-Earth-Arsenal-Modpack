# Selectable pack v2.1.3 release source

Current set: 23 independent switches and One True Flag's 29 damage presets,
defaulting to 300 normal / 150 durable. Stable pack GUID:
`bf6cb345-73c0-5b9b-a16c-38d490155842`.

## Inputs and build

`catalog.json` records ordered options, identities, Include paths and payload
hashes. `payloads/<id>/` holds accepted archives. `release-metadata.json` holds
public descriptions; repository README.md supplies the release ZIP README.
Canonical readable sources are under source/, including vg70-variable/.

From the HD2 Mods workspace root:

```powershell
python work/super-earth-arsenal-modpack-repo/tools/configurable-pack/build.py --release --incremental --output work/super-earth-arsenal-modpack-repo/Super-Earth-Arsenal-Modpack-v2.1.3.zip --evidence work/release-health-normal-20261016/pack
```

Outputs are immutable; different bytes at an existing path are refused. Retain
all older releases/ZIPs. Use tagged historical catalogs to reproduce old versions.
Do not run old one-time prepare/import builders against the current source.

The builder checks the full resource inventory, pure-Lua archives and dependency
closure per option. The base union has 36 resources. A full selection with Flag
uses 26 main archives and 52 companions. Shared identical resources and complete
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
Enable-all off initially selects the first option; enable-all on selects all23
and the first Flag preset. Disabled Flag suppresses its preset. Stable names,
GUID, order and Include paths remain unchanged.

Gas/Tenderizer share15-second Acid Storm duration, including weather. AC-8/Epoch
share animation resources; AC-8/JAR-5 share a FLAK explosion. Keep the former
individual repository's legacy releases and all pack release history intact.

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
