# Selectable pack v2.0.0 release source

The user accepted the full Rev3 startup and explicitly requested the repository
update/publication on2026-10-15. The v2.0.0 release contains the exact tested
Rev3 Addon and preset files. Only README.md and manifest Description fields are
updated for publication. The former individual repository is repurposed for
standalone runtime/weapon projects; all22earlier individual releases remain.

The public release is built with `tools/configurable-pack/build.py --release`.
It reads reviewed metadata from `release-metadata.json` and public README.md;
GUID/version/option names, folders, presets and gameplay bytes remain exact.
Without `--release`, the builder still reproduces the immutable Rev3 test ZIP.
Publication evidence is under `work/release-selectable-pack-20261015/` in the
HD2 Mods workspace. Do not rerun that one-time release preparation over a later
baseline. The release SHA differs from Rev3 only because the public copy changes.

## Build inputs

`catalog.json` is the ordered list of 22 mod switches and the Flag damage presets.
Current Rev3 has one 29-choice dropdown inside the One True Flag option;
300 normal /150 durable is first and remains the default. Normal presets are
0,100,200,300,400,500,600,750,1000,1500,2000,3000,5000,7500 and9999; each offers half
or equal durable damage (zero has one equivalent 0/0 choice). User approved one
dropdown. The old five independent digit controls are retained as baseline data
only and are omitted from the Rev3 ZIP. It no longer offers every custom integer.
`payloads/<id>/` contains exact accepted Addon and Flag Settings files, imported
once from the 22 published individual ZIPs. Origin ZIP names, versions, GUIDs,
SHA256 and every imported file hash are recorded. Subsequent builds read this
repository's catalog/payloads only. The individual repository is not a build input
unless explicitly running the one-time `--import-baseline` migration again in a
new empty catalog directory.

Canonical authored Lua is under this repository's existing source directories.
Preserve the catalog's payload hashes until deliberately updating a mod. Rebuild
all carriers of a changed shared Lua resource together, update their catalog
hashes, then rerun the composition/startup/transaction checks. A mismatching
resource hash fails the builder. This migration changes packaging and public
copy only; every accepted gameplay resource is byte-identical.

The candidate uses the existing pack GUID bf6cb345-73c0-5b9b-a16c-38d490155842.
It omits the old unconditional five-peer pack entrypoint and redundant legacy
bootstrap. Bingus Shared Loader remains required. Each enabled option includes
its complete accepted archive; identical shared library duplicates resolve under
the loader's existing resource and require cache. Animation archives remain
separate from pure-Lua archives. There are no patch files at the ZIP root, so
Arsenal's empty-selection fallback installs no weapon archive.

## Commands from the HD2 Mods workspace root

```powershell
& 'C:\Users\crife\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'work/super-earth-arsenal-modpack-repo/tools/configurable-pack/build.py'
& 'C:\Program Files\nodejs\node.exe' 'work/super-earth-arsenal-modpack-repo/tools/configurable-pack/test_flag_dropdown.cjs' 'work/configurable-pack-20261015/arsenal-backend' 'work/configurable-pack-20261015' 'outputs/configurable-pack-20261015/Super-Earth-Arsenal-Modpack-v2.0.0-Selectable-Rev3-Test.zip'
& 'C:\Users\crife\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'work/super-earth-arsenal-modpack-repo/tools/configurable-pack/test_flag_presets.py'
```

The Lua tests require the local supported lua51.dll and extracted stock tables
already used by this workspace. The focused guards reuse existing fixture data
only after proving that their embedded transaction/module source matches the
current accepted code. Reports and generated fixtures go under
`work/configurable-pack-20261015/`, outside this repository. Do not run legacy
builder entrypoints: they can regenerate older gameplay or initialization code.

The Arsenal fixture uses a read-only copy of the installed 0.36.2 backend from
app.asar. Its config, library, game/data and game/bin directories are fresh local
fixtures, with no access to the actual user's profile. The extraction helper is
`work/configurable-pack-20261015/probe.py`; it copies JS/JSON backend dependencies
without starting Arsenal. Backend logs are retained in each UUID fixture folder.

## Evidence and limits

Follow `REGRESSION-POLICY.md` for future changes; do not repeat the initial
exhaustive migration suites by default. Rev3 is a packaging/settings change.
It passes64focused installed-Arsenal deployments, all29actual Flag writes
with current SAI/Gas guards, two actual discovery-order cases, and exact
previous gameplay-resource equality. The builder saves `composition-rev3.json`;
the initial `composition.json` and other Rev2 reports remain unchanged.

The Rev2 four-mod launch at16:02:19 local is confirmed:41loaded/0failed,
APW-1+CQC-20+P-34+Railgun,4profiles/9values applied,12exact file matches.
Rev3 full22startup at16:16:44 local is now confirmed:61loaded/0failed,
all22mods final,75exact deployed file matches,Flag300/150preset loaded before
Flag and applied. Saved evidence is
`work/configurable-pack-20261015/full-rev3-launch-20261015T141905Z/report.json`.
The user subsequently accepted the result and requested publication. This is
release acceptance, not independent numerical gameplay or host/client evidence;
independent loaded resources were not inspected.

Latest evidence: `work/configurable-pack-20261015/README.md` and JSON reports.
Composition checks enumerate all 4,194,304 selections and verify dependency
closures and exact shared payloads. Real Arsenal import/deploy/purge covers
1,817 selections plus eight edge cases. Real Shared Loader discovery runs on
all 1,817 selected archive sets. The 7,268 Lua startup-control cases execute the
shipped controllers, profile registration and peer readiness in four orders.
Patch and native adapters in that matrix are fixtures; it is not 7,268 live
startups or full transaction executions. The separate guard/transaction suite
executes current transaction code in isolated memory, including partial writes,
foreign edits and rollback. Full Variable synthetic runtime is also exercised.

Actual game startup, loaded-resource inspection, gameplay and host/client
behavior remain separate gates. No real deployment/settings were changed.
Before publication, use a few representative user launches, inspect fresh
expected-module final states and exact deployed candidate bytes, and obtain
gameplay acceptance. Do not request manual testing of every combination.

## Upgrade behavior

Arsenal0.36.2 does not map the old v1 option name to the22new names. Import
with its global enable-all preference on enables all22switches and the first
Flag preset. With that preference off it still enables the first mod option;
Flag starts disabled with no preset radio selected. Flag's internal fallback
remains300/150 when enabled without a preset. Rev2 had27options; Rev3 has22.
Users must review switches on import/upgrade; do not modify their profile to
silently choose a subset. Flag's disabled parent suppresses its preset archive
even if a stored child radio remains selected. Each selected preset sets all
five internal values; it does not inherit stale digits from an earlier preset.

Gas/Tenderizer retain the shared 15-second Acid Storm duration. AC-8/Epoch retain
the shared animation resource; AC-8's JAR-5 shared explosion remains. Turning off
a weapon option does not undo shared effects supplied by another selected mod.

## Repository migration

Keep new selectable-pack work in this repository. Keep v1.0.26 and all earlier
pack releases plus the22individual release history intact. The old repository
is repurposed as Helldivers2RuntimeMods; it is not archived or renamed. Its old
Arsenal packages are retained, and its new landing page directs weapon-pack
users here. Do not add new pack weapons to that legacy release pipeline.
