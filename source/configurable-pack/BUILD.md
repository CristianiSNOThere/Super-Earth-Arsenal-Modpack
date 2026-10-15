# Selectable pack v2.1.0 release source

Current baseline:23 independent mod switches, including BR-14 Adjudicator Heavy
Battle Rifle, and One True Flag's single29-choice damage dropdown. DefaultFlag
damage remains300normal/150durable. User accepts the final480RPM Rev2 candidate
and requests repository update/publication on2026-10-15.

## Inputs and build

`catalog.json` records ordered stable option names, package identities, Include
paths and payload hashes. `payloads/<id>/` contains the accepted archives.
`release-metadata.json` holds the reviewed main/option descriptions; repository
README.md supplies the release ZIP README. Canonical readable implementations
are under this repository's source directories, including `adjudicator-heavy/`.
The former individual repository is not an input for routine builds.

Use the workspace's bundled Python executable from the HD2 Mods root:

```powershell
python work/super-earth-arsenal-modpack-repo/tools/configurable-pack/build.py --release --incremental --output work/super-earth-arsenal-modpack-repo/Super-Earth-Arsenal-Modpack-v2.1.0.zip --evidence work/release-adjudicator-20261015/pack
```

The explicit output is immutable: a different byte stream at an existing path
is refused. Use a new version/revision for gameplay changes. Historical v2.0.0
and earlier ZIPs remain intact. The legacy no-incremental builder mode requires
the historical22-option catalog; obtain it from the v2.0.0 tag to reproduce that
version. Do not run old one-time prepare/import scripts against current inputs.

Incremental mode checks every resource/hash, pure-Lua archive and each option's
complete dependency closure. Identical shared overlaps plus a complete closure
per option establish static union compatibility without enumerating millions
of masks. This is a resource/dependency property, not universal runtime/gameplay
proof. New BR-14 resources are private; all22earlier gameplay archives and all29
Flag preset archives remain byte-identical to v2.0.0.

The stable packGUID remainsbf6cb345-73c0-5b9b-a16c-38d490155842. There are no root
patches, so all-off deploys no weapon archive. Lua and animation archives remain
separate. Current base resource union36; selectedFlag adds its mutually exclusive
preset resource. Full23 selection with aFlagpreset deploys26mainarchives and52
empty companions,78files total. Existing duplicate animation resources are exact.

## Focused regression

Follow REGRESSION-POLICY.md. Do not rerun all prior pairs/triples or ask the user
to test every old weapon. Reuse exact baseline code/data/dependency hashes.

```powershell
python work/super-earth-arsenal-modpack-repo/tools/configurable-pack/test_runtime.py --incremental --evidence work/adjudicator-heavy-20261015-rev2/pack
node work/super-earth-arsenal-modpack-repo/tools/configurable-pack/test_incremental.cjs work/configurable-pack-20261015/arsenal-backend work/adjudicator-heavy-20261015-rev2/pack outputs/adjudicator-heavy-20261015/Super-Earth-Arsenal-Modpack-v2.1.0-Adjudicator-Rev2-RPM480-Test.zip
```

The Arsenal backend fixture uses a read-only extraction of installed0.36.2 and
fresh local profile/library/game directories; it never controls the real profile.
The runtime harness exercises actual discovery/controllers/registration/peer
gates with patch/native adapters. Real transaction checks are separate:
`work/adjudicator-heavy-20261015-rev2/verify.py` runs30cases in isolated LuaJIT
buffers, including unknown data, owner checks, partial writes, readback failure,
rollback, foreign edits and actual local Windows memory protection restoration.
`verify_startup.py` covers9bounded startup cases and2saved-code penetration cases.
The canonical7source implementations recompile exactly to shipped bytecode.

The initial selectable migration's exhaustive composition,1825Arsenal deployments,
7268startup simulations and old transaction suites remain in
`work/configurable-pack-20261015/`; no migration matrix was repeated for BR-14.

## Accepted live evidence and release delta

Fresh Rev2 full23 startup18:59:51 Europe/Madrid:62loaded/0failed; all23expected
final mod states; exactAdjudicator480RPM status;13dedicated Applied logs,
9profiles/33values with0refused/0panelerrors,Scorcher14fields andPLAS39native
selector final. Installedmanifest and78selected deployed files match Rev2.
Evidence: `work/adjudicator-heavy-20261015-rev2/full-adjudicator-rev2-launch-20261015T170057Z/`.
User subsequently accepts the result and authorizes publication. Independent
loaded-resource inspection, per-target numerical measurements and universal
host/client behavior are not claimed. User's earlier muzzle-flash report was
withdrawn as a fluke; no visual change was implemented.

Public v2.1.0 changes only README.md and manifest Description fields from accepted
Rev2. Gameplay/preset files, version, GUID, names, paths, order and defaults remain
exact. Publication evidence is under `work/release-adjudicator-20261015/`.

## Import behavior and shared effects

Arsenal0.36.2 preserves existing named22-option selections on upgrade; the appended
BR-14 option follows the manager's import defaults. Review selections on import.
With enable-all off, Arsenal still enables its first option; with enable-all on,
all23parents and the firstFlagpreset are enabled. A disabledFlag parent suppresses
its preset. Preset archive numbering preserves discovery before theFlag module.

Gas/Tenderizer retain shared15-second AcidStorm duration, includingweather.
AC-8/Epoch share their animation resource; AC-8/JAR-5 share aFLAK explosion.
Existing whole-table validators remain supported because BR-14's original
serialized damage/projectile arrays are not modified. Deployment, settings and
gameplay remain with the user. Keep all pack release history and the former
individual repository's22legacy releases.
