# Super-Earth Arsenal Pack — Complete

One Arsenal ZIP enables the complete Super-Earth Arsenal set: six core mods and nine supported SHODAN Preset 1 weapon/sentry profiles.

> **Staging build:** the corrected preset profiles have not yet been confirmed in a fresh live launch. The shared runtime and all nine profile entries loaded together in the previous ship session, but that session used an earlier timing build that did not reach the apply step. Keep this package as a local candidate until the fresh log confirms the profiles apply.

## Download

[Super-Earth Arsenal Pack v1.0.0](Super-Earth-Arsenal-Pack-v1.0.0.zip)

## Included mods

| Core mod | Version |
|---|---:|
| One True Flag — Adjustable Damage | v0.9 |
| SAI — Focus Precision | v0.4 |
| AR-11 Arbitrator — Tuned | v0.2 |
| R/40-K Hot-Shot — Magazine Tuning | v0.8 |
| TX-41 Sterilizer — Armor Control | local v0.8 |
| ARC-3 Rapid Arc Thrower | v0.9 |

| SHODAN Preset 1 profile | Fields |
|---|---:|
| ARC-12 Blitzer | 4 |
| CQC-20 Breaching Hammer | 6 |
| PLAS-39 Accelerator Rifle | 14 |
| P-34 Breacher | 1 |
| S-11 Speargun | 4 |
| APW-1 Anti-Materiel Rifle | 1 |
| 40-K Meltagun | 1 |
| A/GM-17 Gas Mortar Sentry | 1 |
| RS-422 Railgun | 1 |

The current separate packages, including each SHODAN profile, are maintained in the [Super-Earth Arsenal Pack repository](https://github.com/CristianiSNOThere/Super-Earth-Arsenal-Pack). The Commando cooldown was excluded because the current extracted game data has no exact source/stock record to validate it safely.

## Compatibility

- Helldivers 2 Steam build 25480438.
- Bingus Shared Loader v18 or newer.
- Sterilizer v0.8 is included in place of the published v0.7 package. It recognizes ARC-3 v0.9's known damage-table edits.
- The SHODAN profiles share one namespaced runtime. It waits 30 seconds for package initialization, then requires One True Flag, SAI, AR-11, Sterilizer, and ARC-3 to report `Applied`. It waits up to two more minutes; if a required companion fails, it writes no preset values.
- After the companion mods are ready, each profile is preflighted and applied as its own transaction. A conflict in one profile does not prevent other profiles from applying.

## Install

1. Import this ZIP into Arsenal and enable its single option.
2. Keep Bingus Shared Loader at its default last priority.
3. Purge and Deploy, then restart Helldivers 2.
4. On the ship, allow initialization to finish and check the logs under `%LOCALAPPDATA%\CowboyBingus\Helldivers2\Logs`.

For a custom selection, use the separate ZIPs from the linked repository. Do not enable this complete ZIP alongside its individual counterparts.

## Local package details

- Manifest: `Super-Earth Arsenal Pack - Complete`.
- ZIP SHA-256: `6495723189D9CA8678DA4A50395AEEA7A383D7A829AD66CA4A2AADE5DA3C1EB3`.
- The package has not been imported, deployed, or published from this staging repository.
