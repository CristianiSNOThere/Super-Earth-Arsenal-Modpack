# GL-52 accepted AP4 source

Canonical source for v2.3.0, accepted after AP4 gameplay testing. Compile entry.lua as-is and package the resulting pure-Lua archive. Preserve the accepted source line metadata; the historical work/gl52-de-escalator-20261017/prepare.py may reformat the entry and requires fresh source/bytecode verification before use. Packaging is in package.py in that work directory.
Exact component ownership and whole-row guards, supported game hashes and native damage-consumer pins. Damage201 is a retained copy published transactionally; original bytes remain untouched. Only the existing ID201 is used. Stun Large39 is checked by current native name, type and duration; global status data is never modified.

GL-52 rows and damage201 have no other serialized consumers in the pinned census. Other mods may edit other rows of these component groups, which are preserved. No companion completion is required, so unrelated absent/failed peers cannot block it.

Keep 100 normal and 100 durable damage with stock AP4/4/4/0. AP4 is the release setting. Keep handling 35, reserve/start/resupply 70, reload speed 1.15x, and Stun Large 39 with stock buildup 1.75. The requested roughly three-grenade heavy stun remains a design target, not a measured universal breakpoint.

Release gates passed: 34 actual transaction cases, 11 focused controller cases, 56 startup-order simulations including GL-52 with each of the other 24 options, eight isolated Arsenal cases, and a 51-resource dependency/collision audit. The fresh full-pack AP4 startup loaded 64 modules with zero failures; AP4 gameplay was accepted. Evidence: workspace work/release-gl52-20261017/ and work/gl52-de-escalator-20261017/launch-20261017T185351Z/. These checks do not prove every possible gameplay combination.
