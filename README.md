# Super Earth Arsenal Mod Pack v2.2.1

## 🚨 COMPATIBILITY WARNING — READ BEFORE PLAYING 🚨

> [!CAUTION]
> **IN CASE OF CRASHES OR MODS NOT LOADING PROPERLY, REMOVE ANY OTHER WEAPON MODS OR STAT EDITOR MODS.**

Choose the weapon and equipment changes you want from one package. Each of the **24 mods has its own switch in Arsenal**: enable a single weapon, a smaller selection, or the complete set.

**One True Flag has one damage dropdown with 29 presets**, defaulting to **300 regular damage and 150 against durable parts**. Its settings are inside the Flag option.

**Added in v2.2.0:** SG-8P Punisher Plasma with Normal and Shotgun modes, separate ammunition pools and a magazine-shaped undergrip.

[Download v2.2.1](https://github.com/CristianiSNOThere/Super-Earth-Arsenal-Modpack/releases/download/v2.2.1/Super-Earth-Arsenal-Modpack-v2.2.1.zip) | [All releases](https://github.com/CristianiSNOThere/Super-Earth-Arsenal-Modpack/releases) | [Standalone runtime projects](https://github.com/CristianiSNOThere/Super-Earth-Arsenal-Pack)

## Choose your mods

- Turn each weapon or equipment mod on or off independently in Arsenal.
- Expand **One True Flag** to choose its normal/durable damage preset. Half durable damage rounds down; equal durable damage matches normal damage.
- Changing selections takes effect after **Purge and Deploy**, followed by a game restart.
- When importing or upgrading from v1, review all switches before deploying. Arsenal's enable-all preference can select the complete set automatically; with that preference off, Arsenal initially selects the first mod option.
- Use this package in place of the matching individual weapon mods or older Arsenal modpacks.

For Punisher Plasma, switch to another primary before disabling, replacing or removing its option or the pack. Disable its separate individual mod when using the pack option.

## Gameplay changes

Each entry starts with a short summary. Expand it for the complete settings in plain language.

### A quick guide to the numbers

- **Regular damage** is the usual damage value. **Damage against durable parts** is the separate value the game uses for its durability system; it is not bonus damage added on top.
- **Rounds per minute** is firing speed. **Metres per second** is how fast the projectile travels.
- **Armor penetration** determines which armor a hit can damage. Level 3 is medium penetration; higher levels can penetrate tougher armor. Hit angle still matters.
- **Handling rating** is the ergonomics stat: how readily the weapon follows your aim. **Aim sway** is weapon wobble; a lower sway setting means less wobble.
- **Stagger** is the strength used to interrupt an enemy; **knockback** is the strength used to push it. Actual reactions depend on the target.
- **Full-damage radius** is the area receiving the blast's full damage. Damage falls toward the **outer damage radius**; the **shockwave radius** describes its force area.
- Timings and awkward decimals are rounded and marked as approximate. The weapon settings themselves are unchanged.

### SG-8P Punisher Plasma

Switch between a powerful plasma blast and a nine-pellet plasma shotgun, with separate ammunition supplies.

<details>
<summary>All changes and stats</summary>

- Hold R and use the left-side Normal / Shotgun selector. Adds a magazine-shaped undergrip with a matching white finish.
- Normal: 60 rounds per minute. Explosion damage is 350 regular and 225 against durable parts; hits apply burning.
- Normal blast: full damage out to 3.5 metres, outer damage radius 6.5 metres and shockwave radius 8 metres.
- Normal ammo: 17 loaded rounds and one spare 17-round magazine. Aim sway is reduced by 50%, and the projectile follows a flatter path.
- Normal hit strength: demolition rating 30 for destructible objects, stagger strength 25 and knockback strength 30.
- Shotgun: 100 rounds per minute. Each shot spends one round to fire nine explosive plasma pellets.
- Each pellet: 25 regular damage and 9 against durable parts on impact, plus another 25 and 9 from the explosion. Medium armor penetration (level 3) at every impact angle.
- Shotgun blasts: full-damage, outer damage and shockwave radii are all 0.5 metres. Stagger and knockback strength are both 25.
- Shotgun ammo: a separate pool of 20 loaded rounds and 60 reserve rounds. Reloads twice as fast, with a broad pellet pattern that is slightly wider side to side.
- Shared effect: this option also changes the original behavior of the Loyalist and One-Two.

**Additional values explained**

- Shotgun spread angle settings: roughly 5.7 degrees side to side and 5.2 degrees up and down (100 and 90 milliradians). These describe the spread settings, not a guaranteed group size.

</details>

### BR-14 Adjudicator Heavy Battle Rifle

A harder-hitting 48-round battle rifle with a slower fire rate and heavier vertical recoil.

<details>
<summary>All changes and stats</summary>

- Damage per bullet: 115 regular and 30 against durable parts, up from 95 and 23.
- Magazine: 48 rounds instead of 30. Fire rate: 480 rounds per minute instead of 550.
- Hit reaction: stagger strength 25 instead of 15; knockback strength 10 instead of 12.
- Bullet speed: 1,000 metres per second instead of 820. Bullets lose 15% speed each time they penetrate, instead of 25%, retaining more speed after passing through a target.
- Recoil movement: side-to-side setting 16.5 instead of 17, vertical setting 57.5 instead of 35. Base aim sway falls by 40%, from setting 1 to 0.6.
- Armor penetration, camera kick, spread, drag and spare-magazine counts stay the same.

</details>

### Tenderizer Armor Softener

A 70-round rifle whose bullets temporarily weaken enemy armor.

<details>
<summary>All changes and stats</summary>

- Damage per bullet: 90 regular and 30 against durable parts. Keeps its 600 and 850 rounds-per-minute settings.
- Magazine: 70 rounds instead of 35. Bullet speed: 1,000 metres per second instead of 820.
- Penetration: medium armor (level 3 instead of 2) on direct and slightly angled hits. Other impact-angle penetration settings are unchanged.
- Bullets apply Acid Storm, reducing enemy armor effectiveness for 15 seconds.
- Base aim sway: setting 0.9. Recoil and spread stay the same.
- Shared effect: the 15-second Acid Storm duration also applies to the weather effect after exposure ends.

</details>

### Sickle Laser AR

Accurate laser assault rifles with faster projectiles, medium penetration and no damage loss over distance.

<details>
<summary>All changes and stats</summary>

- LAS-16 Sickle: 70 regular damage and 10 against durable parts. Heat generated per shot is halved, so it can fire longer before overheating.
- LAS-17 Double-Edge Sickle: cold and warm shots deal 65 regular damage and 10 against durable parts; hot and maximum-heat shots deal 83 and 14.
- Both rifles: base fire rate 700 rounds per minute, zero spread and projectile speed 2,000 metres per second at every heat level. No damage loss over distance.
- Both have at least medium armor penetration (level 3). Double-Edge reaches level 4 at maximum heat.
- Double-Edge heat self-damage is reduced by 25%. Its bullet heat buildup, cooling and maximum-heat ignition stay the same; general fire damage is unchanged.

**Additional values explained**

- Normal Sickle heat per shot: about 0.58 instead of 1.15, a 50% reduction.

</details>

### VG-70 Variable Portable Maxigun Rework

A mobile 150-round primary with three firing modes, medium penetration and 15% less recoil.

<details>
<summary>All changes and stats</summary>

- Magazine: 150 rounds. Remains a primary weapon, needs no backpack and can reload while moving.
- Auto at 550 rounds per minute: 110 regular damage and 29 against durable parts per bullet.
- Auto at 750 rounds per minute: 90 regular damage and 24 against durable parts per bullet.
- Auto at 1,000 rounds per minute: 75 regular damage and 20 against durable parts per bullet.
- Volley: fires 15 bullets together. Each deals 40 regular damage and 11 against durable parts. Uses the selected 550, 750 or 1,000 rounds-per-minute setting.
- Total: fires every remaining round at once. Each bullet deals 28 regular damage and 8 against durable parts, with a tighter spread setting of 0.75 in both directions.
- All modes: medium armor penetration (level 3) and 15% less recoil.
- Spare magazines: 6 at the start, 7 maximum and 7 from resupply. Handling rating: 40. Base aim sway: setting 0.9.
- Total still injures your right arm and knocks you down. Muzzle flashes stay aligned during sustained Auto fire. Reload timing, projectile speed and sounds stay the same.

**Additional values explained**

- Recoil movement settings, side to side / up and down: 4.25 / 8.5 instead of 5 / 10. Camera kick: 3.4 / 6.8 instead of 4 / 8. These are the same 15% reductions described above.

</details>

### PLAS-45 Epoch Highest-Charge Rework

Stronger highest-charge shots, a larger magazine and a reload you can perform while walking.

<details>
<summary>All changes and stats</summary>

- Highest-charge shots: 30% more regular and durable-part damage on both the direct hit and explosion. Explosion hits also apply burning.
- Highest-charge base damage: direct hit 520 regular and 260 against durable parts; explosion 1,040 regular and 1,040 against durable parts. The existing charge damage multiplier still applies.
- Blast: full damage out to 5 metres, outer damage radius 6 metres and shockwave radius 7 metres.
- Magazine: 4 rounds instead of 3. Maximum spare magazines: 5 instead of 4. Start with 2 spare magazines and receive 2 from resupply.
- Reload while walking, using the existing reload animation.
- Charge thresholds stay at 1, 2.5 and 2.6 seconds. Lower-charge shots retain their damage.

</details>

### AR-32 Pacifier Tuning

More damage, stronger stun buildup, a 65-round magazine and 40% less aim sway.

<details>
<summary>All changes and stats</summary>

- Damage per bullet: 75 regular and 15 against durable parts, up from 55 and 10.
- Stun buildup per hit: 3 instead of 2, a 50% increase. This uses the weapon's medium-stun effect.
- Default magazine: 65 rounds instead of 40.
- Aim sway: 40% lower; the sway setting changes from 1 to 0.6.

</details>

### AC-8 Autocannon Backpackless Rework

A backpack-free Autocannon with more ammunition, a walking reload and 25% less recoil.

<details>
<summary>All changes and stats</summary>

- Ammo: 10 rounds loaded and 60 in reserve. The call-in supplies only the weapon, leaving your backpack slot free.
- Reload: about 20% faster, using the familiar five-round top reload while walking. Resupply refills up to 60 reserve rounds.
- Handling rating: 30 instead of 17. Recoil and the camera kick from firing are both reduced by 25%.
- APHET shells: 375 regular damage and 340 damage against durable parts on a direct hit; heavy armor penetration (level 5). The impact explosion deals 180 regular damage.
- FLAK shells: 210 explosion damage with an 8-metre outer damage radius. Direct-hit damage and shrapnel stay the same.
- Shared effect: JAR-5 Dominator High Explosive ammunition gets the same explosion buff.

**Additional values explained**

- Recoil movement settings, side to side / up and down: 150 / 337.5, previously 200 / 450.
- Camera kick settings, side to side / up and down: 1.5 / 75, previously 2 / 100. These are the same 25% reductions described above.

</details>

### PLAS-1 Scorcher AR

A 50-round automatic Scorcher with lower damage per shot, a wider blast and 25% less recoil.

<details>
<summary>All changes and stats</summary>

- Magazine: 50 rounds instead of 20. Fire rate: 540 rounds per minute instead of 350.
- Fire modes: select Semi or Auto in Weapon Functions. Auto empties a full magazine in about 5.6 seconds of continuous fire.
- Regular damage: 150 total instead of 200, made up of 75 from the impact and 75 from the explosion, before armor, hit location and distance.
- Damage against durable parts: 38 from the impact and 75 from the explosion, or 113 combined against a fully durable part.
- Blast: full damage out to 1.25 metres instead of 1; outer damage radius 2.5 metres instead of 2.
- Spare magazines: 4 at the start instead of 3, maximum 6 instead of 5, and 5 from resupply.
- Recoil: 25% less weapon movement and camera kick per shot.

**Additional values explained**

- Recoil movement: 15 in both directions, previously 20. Camera kick: 1.5 side to side and 15 vertically, previously 2 and 20.

</details>

### One True Flag

Choose a damage preset from one dropdown; the default is 300 regular damage and 150 against durable parts.

<details>
<summary>All changes and stats</summary>

- 29 presets. Regular-damage choices: 0, 100, 200, 300, 400, 500, 600, 750, 1,000, 1,500, 2,000, 3,000, 5,000, 7,500 or 9,999.
- Damage against durable parts can be half the regular damage, rounded down, or equal to it. The zero-damage preset uses zero for both.
- Default: 300 regular damage and 150 against durable parts. The dropdown is inside the One True Flag option.

</details>

### SAI Focus Precision

A fast laser SMG with tighter spread, less recoil and less heat per shot.

<details>
<summary>All changes and stats</summary>

- Both lenses: 90 regular damage and 21 against durable parts when the shot leaves the muzzle. Fire rate: 900 rounds per minute.
- Spread: 50% tighter than stock for each lens. Focus remains more accurate than Standard.
- Projectile speed: 1,300 metres per second. Damage decreases over distance.
- Recoil and heat generated by each shot are both reduced by one-third with either lens.

**Additional values explained**

- Spread angle settings are about 4 degrees in each direction for Standard and 2.1 degrees for Focus (70 and 37.5 milliradians). These describe the spread settings, not a guaranteed group size.
- Distance drag setting: about 1.24. A higher drag setting slows projectiles more and affects damage retention over distance.
- Heat per shot: about 1.33 instead of 2 with Standard or cooldown heatsinks; 1 instead of 1.5 with the heat-capacity heatsink.

</details>

### AR-11 Arbitrator

An 80-damage rifle with a 65-round magazine and more underbarrel shotgun ammunition.

<details>
<summary>All changes and stats</summary>

- Rifle damage: 80. Magazine: 65 rounds.
- Underbarrel shotgun: 4 shells loaded, 30 starting reserve shells and a maximum of 30. Resupply provides 20 shells.
- Hit reaction: stagger strength 25 and knockback strength 20.
- Handling rating: 41 before attachments, or 40 with the default optic.

</details>

### R/40-K Hot-Shot

A 20-round magazine, five spare magazines and a handling rating of 45.

<details>
<summary>All changes and stats</summary>

- Magazine: 20 rounds. Spare magazines: 5 at the start, 5 maximum and 5 from resupply.
- Handling rating: 45. Uses standard magazine reloads.

</details>

### Gas Overhaul

Gas temporarily weakens enemy armor, deals more damage and hurts Helldivers less.

<details>
<summary>All changes and stats</summary>

- Armor weakening: supported gas hits apply Acid Storm for 15 seconds. Armor plates are not permanently destroyed.
- Gas damage over time: 45 regular damage and 45 against durable parts per second, up from 25 each. This also affects other sources that use the same gas damage.
- Sterilizer tank: 175 rounds instead of 125. Gas and confusion build up 50% faster per hit, with both buildup values rising from 0.5 to 0.75.
- Helldivers take about 44% less gas damage than with the stock gas-damage multiplier. This applies to gas from all sources, including hazards.
- Supported sources include Sterilizer, Dog Breath, Re-Educator, Speargun, gas grenades, gas mines, Gas Mortar Sentry, Eagle Gas Airstrike and Orbital Gas Strike.
- Shared effect: Acid Storm lasts 15 seconds instead of 1, including the weather effect after exposure ends.
- Supports Health Rework Normal (150 health, 2.8 regeneration) or Casual (160 health, 3 regeneration), keeping the chosen preset's health, regeneration and stim settings. Use one health preset at a time.

**Additional values explained**

- The incoming gas-damage multiplier falls from 1.3 to about 0.73; the reduction relative to stock is about 43.6%.

</details>

### ARC-3 Rapid/Supercharge

Choose quick, weaker shots or a slow, powerful charge that hits one enemy.

<details>
<summary>All changes and stats</summary>

- Hold R and select Auto for Rapid or Semi for Supercharge.
- Rapid: charges in roughly one-third of a second. Each pulse deals about 192 regular damage and 77 against durable parts, 15% below its base pulse damage.
- Supercharge: charges in roughly 3.4 to 3.75 seconds. Deals 2,325 regular damage and 2,325 against durable parts. Hits one enemy without chaining or splitting, and cannot explode from overcharging.
- Both modes: heavy armor penetration (level 7), 45-metre reach and the original Arc Thrower sounds.

**Additional values explained**

- Rapid charge thresholds, rounded: 0.31, 0.34 and 0.37 seconds. Supercharge thresholds: 3.4, 3.5 and 3.75 seconds.
- Rapid base pulse damage is 226 regular and 90 against durable parts. After its 15% reduction, this is about 192.1 and 76.5.

</details>

### ARC-12 Blitzer

Sets damage to 100, range to 30 metres and fire rate to 80 rounds per minute.

<details>
<summary>All changes and stats</summary>

- Damage: 100 regular and 45 against durable parts.
- Arc reach: 30 metres. Fire rate: 80 rounds per minute.

</details>

### CQC-20 Breaching Hammer

Gives direct hits and both blast areas penetration level 7, with 21 ammo refills.

<details>
<summary>All changes and stats</summary>

- Armor penetration: level 7 for the direct hit, smaller blast and larger blast.
- Ammo supply counts: 21 at the start, 21 from resupply and 21 maximum.

</details>

### PLAS-39 Accelerator Rifle

A precise 21-round plasma rifle with quick single shots and a charged three-round burst.

<details>
<summary>All changes and stats</summary>

- Magazine: 21 rounds.
- Semi: fires a single shot with almost no charge delay. Base fire rate is 200 rounds per minute; the normal fire-rate modifier can make the interval a little longer.
- Burst: charges for 0.45 seconds, then fires three rounds about 0.12 seconds apart. Use the left-side Weapon Functions selector to switch modes.
- Armor penetration: level 4 for both the direct hit and explosion. Stagger strength: 25.
- Recoil movement and camera kick: setting 2 in each direction. Aim sway: setting 0.4. Spread: setting 0.3 in each direction; lower values mean a steadier aim and tighter grouping.
- Explosion outer damage radius and shockwave radius: 2.5 metres. Original firing sounds are retained.

**Additional values explained**

- Semi minimum charge is 0.01 seconds. Base time between shots is 0.30 seconds, or about 0.33 seconds with the supported normal fire-rate modifier. Burst minimum charge is 0.45 seconds.

</details>

### P-34 Breacher

Resupply provides 2 magazines.

<details>
<summary>All changes and stats</summary>

- Magazines received from resupply: 2.

</details>

### S-11 Speargun

More spare ammunition and a handling rating of 40.

<details>
<summary>All changes and stats</summary>

- Spare magazines: 16 at the start, 10 from resupply and 20 maximum.
- Handling rating: 40.

</details>

### APW-1 Anti-Materiel Rifle

Sets the weapon handling rating to 40.

<details>
<summary>All changes and stats</summary>

- Handling rating: 40. This is the ergonomics stat that controls how readily the weapon follows your aim.

</details>

### 40-K Meltagun

Sets the weapon handling rating to 40.

<details>
<summary>All changes and stats</summary>

- Handling rating: 40. This is the ergonomics stat that controls how readily the weapon follows your aim.

</details>

### A/GM-17 Gas Mortar Sentry

Gives the sentry 600 health.

<details>
<summary>All changes and stats</summary>

- Sentry health: 600.

</details>

### RS-422 Railgun

Sets damage against durable enemy parts to 240.

<details>
<summary>All changes and stats</summary>

- Damage against durable parts: 240.

</details>

## Shared effects

Gas Overhaul and Tenderizer both use a 15-second Acid Storm effect; the shared duration also affects Acid Storm weather. AC-8's FLAK explosion changes also affect JAR-5 Dominator High Explosive ammunition. AC-8 and Epoch share their mobile reload animation adjustment. These shared changes remain active when supplied by another enabled mod.

## Install

1. Close Helldivers 2. If replacing an older pack that changes Punisher Plasma, equip a different primary before closing the game.
2. Import the ZIP into Arsenal and select the mods you want. Choose a Flag preset if enabling One True Flag.
3. Disable matching individual weapon mods and older Arsenal modpacks. Keep Bingus Shared Loader at its documented priority.
4. Run **Purge and Deploy**, then start the game. Allow up to about two minutes after reaching the ship for the weapon changes to take effect.

Requires Helldivers 2 Steam build 25480438 and Bingus Shared Loader v19.

## Weapon selectors

- **Punisher Plasma:** hold R and use the left-side Normal / Shotgun selector.

- **AC-8:** choose APHET or FLAK in the stock Weapon Functions selector.
- **ARC-3:** hold R and choose Auto/Rapid or Semi/Supercharge.
- **Scorcher:** select Auto in Weapon Functions for continuous fire.
- **PLAS-39:** hold R and use the left-side Weapon Functions selector. Semi is the quick single shot; Burst charges for about half a second and fires three rounds. Full timings are listed above.

## Changes in v2.2.1

- Clearer descriptions for all 24 mods in this README and Arsenal.
- Short summaries, explained stats and rounded timings make it easier to compare weapons.
- All weapon and equipment settings stay the same as v2.2.0.

## Changes in v2.2.0

- Adds SG-8P Punisher Plasma as the 24th independent option.
- Switch between Normal plasma blasts and a nine-pellet Shotgun mode, each with its own ammunition supply.
- Adds the magazine-shaped undergrip with a matching white finish.

## Changes in v2.1.3

- Adds compatibility with Health Rework Normal (150 HP, 2.8 regeneration).
- Retains compatibility with Health Rework Casual (160 HP, 3 regeneration).
- Keeps the selected preset's health, regeneration and stim settings. Enable one health preset at a time.
- Retains all 23 independent mod switches and One True Flag's 29 damage presets.

## Changes in v2.1.2


- Use Gas Overhaul and the complete weapon collection alongside Health Rework (Casual, 160 hp, 3 regen).
- Keeps that preset's health, regeneration and stim settings, including armor bonuses to stim capacity.
- Retains the 23 independent mod switches and One True Flag's 29 damage presets.

## Changes in v2.1.1


- Restores VG-70 Variable damage in Auto, Volley and Total.
- Auto at 550 rounds per minute deals 110 regular damage and 29 against durable parts; at 750, it deals 90 and 24; at 1,000, it deals 75 and 20.
- Volley deals 40 regular damage and 11 against durable parts per bullet. Total deals 28 and 8.
- All Variable modes have medium armor penetration (level 3). Total changes from level 4 to level 3.
- Keeps the 23 independent mod switches and One True Flag's 29 damage presets.
