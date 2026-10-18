# Adjudicator Heavy v0.1.1 release source

Added as the 23rd selectable option in pack v2.1.0 with the final 480 RPM profile. Package/module identities
are stable inidentity.json. No separate legacy individual package is created.

## Compiler input

entry.lua is the complete readable compiler input, assembled fromwindows.lua,
profile.lua,transaction.lua andstartup.lua. Compile using the game's isolated
LuaJIT, using the implementation identity in `identity.json` as the chunk
name with an `@` prefix and `.lua` suffix. `loader-entry.lua` declares the entry
module and requires the compiled implementation.
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

## Validation

The release baseline includes 30 isolated transactions, nine startup cases,
two captured-code penetration cases, source/bytecode checks, resource closure
and six isolated Arsenal import/deployment/purge cases. The accepted 23-option
startup loaded 62 modules without loader failures and matched 78 deployed files.
Penetration velocity retention changes from 75% to 85% per penetration.
These checks establish their stated scope; they do not establish every gameplay
combination. Preserve existing payloads and historical releases.
