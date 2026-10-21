# Selectable pack v2.4.1 build

The current catalog contains 25 independent mod switches and 29 One True Flag
damage presets. The default Flag preset is 300 normal and 150 durable damage.
The pack GUID is `bf6cb345-73c0-5b9b-a16c-38d490155842`.

## Inputs

- `catalog.json` defines ordered options, identities, Include paths and hashes.
- `payloads/<id>/` contains the release archives.
- `player-guide.json` supplies complete player descriptions.
- `release-metadata.json` contains public package metadata.
- The repository README supplies the README included in the release ZIP.
- Readable runtime source is under `source/`.

Run from the HD2 Mods development workspace with Python 3:

```powershell
python work/super-earth-arsenal-modpack-repo/tools/configurable-pack/build.py --release --incremental --output work/super-earth-arsenal-modpack-repo/Super-Earth-Arsenal-Modpack-v2.4.1.zip --evidence work/release-hellforge-20261021/pack
```

Existing outputs with different bytes are refused. Use a fresh output path for
changed candidates. Historical catalogs are available through release tags;
historical preparation scripts must not overwrite current accepted sources.

## Resource and startup contracts

Follow `REGRESSION-POLICY.md` for incremental changes. Audit the full resource
inventory, dependency closure, pure-Lua archives, contiguous FileData type
groups and complete CPU/GPU/STREAM payloads. The loader implementation and
non-Lua assets belong in separate archives.

Keep shared resource payloads identical across every carrier. The common
runtime is carried by nine options. Preserve stable module names, resource
keys, package GUIDs, option names, order and Include paths. Private damage and
projectile profiles require ownership checks in the active native registries
as well as serialized tables. Refuse foreign pointers and unknown row values;
rollback must preserve changes made by other owners.

Use canonical startup sources under `source/startup-initialization/` and
`source/scorcher-ar/runtime.lua`. Companion waits must be bounded and report
named failures. Shared-table validators must recognize exact supported peers.
The Punisher source must initialize before companion completion, then perform
the existing post-companion validation; retain its scheduling regressions.

## Current release details

AC-8 accepts the stock or Foliage Pass Through projectile query field on rows
115, 206 and 284, preserving the field while checking all other bytes. Variable
does the same for donor rows 336 and 338 and its owned profiles; registry ownership
checks remain required. The foliage provider initializes before the Lua runtime.
Keep the three bundled HellForge gameplay mods disabled as described in the README.


GL-52 retains the AP4 Rev3 payload. Meltagun range is 20 m and its Fire_Panic
slot is cleared while FlamerSlowed remains. AMR capacity and maximum spare
magazines are both 10; starting and resupply counts remain 5 and 4.
Preserve complete row checks, ownership, readback and rollback in these changes.

Variable uses private damage IDs 585, 586 and 587 with native registry ownership
checks. Its Auto, Volley and Total profiles use AP3; stock Total self-injury and
knockdown remain. Gas accepts only stock or the two complete known Casual and
Normal health profiles, using full normalized checksum validation while
preserving actual health bytes. Unknown, partial and mixed profiles refuse.

Gas and Tenderizer share the 15-second Acid Storm duration, including weather.
AC-8 and Epoch share animation resources; AC-8 and JAR-5 share a FLAK explosion.
These are relevant shared consumers when choosing regression coverage.

## Public descriptions and upgrades

Run `tools/configurable-pack/refresh_public_copy.py` after editing
`player-guide.json`. Preserve the two-column gameplay table and complete prose,
including concrete before-and-after values where known. The compatibility
warning remains prominent. Explain every changed behavior and stat in plain
language; keep internal development records out of player descriptions.

Check Arsenal import, defaults, saved selections, migration and purge with
isolated folders. Enable-all off initially selects the first option; enable-all
on selects the complete set and first Flag preset. Disabling Flag suppresses
its preset. Preserve unrelated gameplay payloads for metadata changes.

Keep offline fixtures, startup, loaded resources, gameplay and multiplayer
evidence distinct. Retain
release history and immutable candidates. Switch to another primary before
replacing or removing Punisher packages.
