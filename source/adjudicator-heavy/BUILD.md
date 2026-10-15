# Adjudicator Heavy v0.1.1 release source

Included as the23rd selectable option in packv2.1.0. User accepts final480RPM
Rev2 after the full23 launch and requests publication. Package/module identities
are stable inidentity.json. No separate legacy individual package is created.

## Compiler input

entry.lua is the complete readable compiler input, assembled fromwindows.lua,
profile.lua,transaction.lua andstartup.lua. Compile using the game's isolated
LuaJIT with chunk name `@mods/codex/adjudicator_heavy_impl.lua`. loader-entry.lua
declares mods/codex/adjudicator_heavy and requires the compiled implementation.
Resources are enveloped with little-endian u32payload length,u32version2 and
packed into a pure-Lua archive. The catalog stores its accepted payload hash.

## Guarded data scope

Owner5FECAB819F96A3E8 uniquely owns magazine row216,WeaponData row285 and fire
row207. Capacity+136 changes30->48. WeaponData+0/+4 drift17/35->16.5/57.5,
+104sway1->0.6. Fire row+8 changes550->480RPM. Camera climb6/50,spread1/1,
ergonomics40 and spare magazine counts6/8/8 are retained.

Two retained data copies preserve native IDs: damage134 changes95/23->115/30,
stagger15->25,push12->10; projectile135 changes820->1000m/s and penetration
slowdown0.25->0.15. AP3/3/3/1,demolition,statusslots,mass11g,diameter8mm,drag0.3,
gravity and all other row fields stay exact. Typed census over269componentgroups,
entitydeltas and damage/projectile/explosion/beam/arc settings finds only BR-14
referencingprojectile135 and onlyprojectile135 referencingdamage134.

Only native registry slotsgame+0x37C64F0 (damage134) andgame+0x37C7AA8
(projectile135) are writable. Originalserialized arrays are unchanged. Exact
EXE/DLL fingerprints, savedconsumer bytepins, complete rowhashes, uniqueowner
maps, snapshots andreadback guard the transaction. Copies remain retained for
process lifetime. Partial component/registry writes roll back only owned values;
foreign changes are preserved. No executable allocation,codepatch or hook.

Startup follows the canonicalTenderizer/Sickle contract without the unrelated
Gas dependency. It checks versions, delays the first attempt, uses8bounded retries
for missing/changing data, refusesunknown data and preserves theupdatechain.
Final state/log:AdjudicatorHeavyV1 / AdjudicatorHeavy.log.

## Evidence

Work scripts and reports: `work/adjudicator-heavy-20261015-rev2/`.
30actual isolated transactions,9bounded startupcases,2savedx64 penetrationcases,
fullresource/closure audit,focusedalone/fullstartupchecks inbothorders,
7source-bytecode matches and6realArsenal0.36.2 deployment/import/purge cases pass.
The penetration code appliesvelocity_after=velocity_before*(1-slowdown):75%
stock retention becomes85% perpenetration. Saved-code emulation uses a1.0constant
fixture; there was no newgameprocess access.

Accepted Rev2 full23 launch18:59:51 Europe/Madrid:62loaded/0failed,allmodfinalstates,
exact480RPM status,installedmanifest and78deployedfile matches. User then accepts
and requests repo update. Evidence:
`work/adjudicator-heavy-20261015-rev2/full-adjudicator-rev2-launch-20261015T170057Z/`.
Startup/fileidentity is distinct from independent loaded-resource or exact
numerical gameplay measurements. The earlier flashreport was withdrawn by the
user; bothrifles' visuals remain unchanged. No further flashcapture is required.

Publication records/download verification are underwork/release-adjudicator-20261015.
Allother22modpayloads and29Flagpresets remain exact. Deployment/settings stay
withuser; retain published history and immutable testZIPs.
