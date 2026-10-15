# VG-70 Variable v0.1.1 release source

Current local fix remaps the three colliding damage IDs542/543/544 to585/586/587.
Damage remains 75/20 Auto1000, 40/11 Volley and 28/8 Total. All modes now use AP3/3/3/0; Total changes from AP4 to AP3 at user request. Auto550
and750 still use540/541. Projectile IDs333/335/336/337/338 remain stable.

The current implementation.lua is the exact readable compiler input. Compile
with the game isolated LuaJIT chunk name@vg70_variable_runtime.lua. entry.lua
requires the compiled module. Preserve module/resource hashesEDC85A4997E8A37B
andF157B721BA21CD57,typeA14E8DFA2CD117E2,GUIDf73eda09-32a6-5db8-b941-ab7992a936d4.
profile-specs.json contains exact source components and before/after targetrows;
id-reservations.json records numeric ownership. The catalog payload is built from
this compiler input; old one-time builders must not overwrite it.

runtime.lua validates native registry pointers against serialized target rows
before edits and before/after instance transactions. It validates expected row
contents continuously. Source-table correctness alone is insufficient: the
captured original instance used damage542->15/15AP9 despite serialized75/20AP3.
Unknown lookup owners refuse; no foreign row or registry pointer is overwritten.
transaction-profile.lua adds a postwrite validation inside the existing protected
transaction so a midtransaction redirect rolls back owned changes. Logs now
report a refusal rather than claimingApplied if an instance update is blocked.

No change to stockTotal selfdamage/knockdown,nativecode,allocation,injuryhandler,
barrelmaps,rate/mode logic,spread,recoil,ammo,reload orsounds. No executablehook.

Workspace work/variable-auto-damage-20261015 containsprepare_fix.py,verify_fix.py,
census.py,package_fix.py,oneauthorizedcapture,oldsource andregression evidence.
Ten actual synthetic runtime scenarios include the captured originalfailure,
all9mode/rate pairs withtwoowners,collisionguards,partialwrites androllback.
Fresh Rev2 startup passed 62/0 at 22:03:07. User accepts gameplay and authorizes v2.1.1 publication; prior v2.1.0 remains in release history. Keepdeployment/settingswithuser andpreserveallhistory.
