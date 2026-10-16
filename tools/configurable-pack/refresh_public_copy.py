"""Refresh player-facing descriptions and README; never changes gameplay payloads."""
from pathlib import Path
import json

REPO = Path(__file__).resolve().parents[2]
CANON = REPO / 'source/configurable-pack'

def main():
    guide = json.loads((CANON / 'player-guide.json').read_text(encoding='utf-8'))
    catalog = json.loads((CANON / 'catalog.json').read_text(encoding='utf-8'))
    public = json.loads((CANON / 'release-metadata.json').read_text(encoding='utf-8'))
    assert set(guide) == {p['option'] for p in catalog['packages']}
    for package in catalog['packages']:
        entry = guide[package['option']]
        text = entry['summary'] + '\n\n' + '\n'.join('- ' + line for line in entry['bullets'])
        if entry['extra']:
            text += '\n\nAdditional values explained:\n' + '\n'.join('- ' + line for line in entry['extra'])
        public['option_descriptions'][package['option']] = text
        package['description'] = text
    public['description'] = ('Choose any of 24 weapon and equipment mods in Arsenal. Each has a plain-language summary and an explained stat list. '
        'Includes Punisher Plasma Normal and Shotgun modes, 29 One True Flag damage presets, and Gas Overhaul support for Health Rework Normal or Casual.')
    for name, data in [('catalog.json', catalog), ('release-metadata.json', public)]:
        (CANON / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    path = REPO / 'README.md'
    readme = path.read_text(encoding='utf-8')
    start = readme.index('## Gameplay changes\n')
    end = readme.index('## Shared effects\n')
    section = '''## Gameplay changes

Each entry starts with a short summary. Expand it for the complete settings in plain language.

### A quick guide to the numbers

- **Regular damage** is the usual damage value. **Damage against durable parts** is the separate value the game uses for its durability system; it is not bonus damage added on top.
- **Rounds per minute** is firing speed. **Metres per second** is how fast the projectile travels.
- **Armor penetration** determines which armor a hit can damage. Level 3 is medium penetration; higher levels can penetrate tougher armor. Hit angle still matters.
- **Handling rating** is the ergonomics stat: how readily the weapon follows your aim. **Aim sway** is weapon wobble; a lower sway setting means less wobble.
- **Stagger** is the strength used to interrupt an enemy; **knockback** is the strength used to push it. Actual reactions depend on the target.
- **Full-damage radius** is the area receiving the blast's full damage. Damage falls toward the **outer damage radius**; the **shockwave radius** describes its force area.
- Timings and awkward decimals are rounded and marked as approximate. The weapon settings themselves are unchanged.

'''
    # Preserve the familiar player-facing display order from the previous README.
    order = ['SG-8P Punisher Plasma', 'BR-14 Adjudicator Heavy Battle Rifle', 'Tenderizer Armor Softener', 'Sickle Laser AR',
        'VG-70 Variable Portable Maxigun Rework', 'PLAS-45 Epoch Highest-Charge Rework', 'AR-32 Pacifier Tuning',
        'AC-8 Autocannon Backpackless Rework', 'PLAS-1 Scorcher AR', 'One True Flag', 'SAI Focus Precision',
        'AR-11 Arbitrator', 'R/40-K Hot-Shot', 'Gas Overhaul', 'ARC-3 Rapid/Supercharge', 'ARC-12 Blitzer',
        'CQC-20 Breaching Hammer', 'PLAS-39 Accelerator Rifle', 'P-34 Breacher', 'S-11 Speargun',
        'APW-1 Anti-Materiel Rifle', '40-K Meltagun', 'A/GM-17 Gas Mortar Sentry', 'RS-422 Railgun']
    assert set('Enable ' + n for n in order) == set(guide)
    for name in order:
        entry = guide['Enable ' + name]
        section += '### ' + name + '\n\n' + entry['summary'] + '\n\n<details>\n<summary>All changes and stats</summary>\n\n'
        section += '\n'.join('- ' + line for line in entry['bullets']) + '\n'
        if entry['extra']:
            section += '\n**Additional values explained**\n\n' + '\n'.join('- ' + line for line in entry['extra']) + '\n'
        section += '\n</details>\n\n'
    readme = readme[:start] + section + readme[end:]
    version = catalog['version']
    readme = readme.replace('# Super Earth Arsenal Mod Pack v2.2.0', '# Super Earth Arsenal Mod Pack v' + version, 1)
    readme = readme.replace('[Download v2.2.0](https://github.com/CristianiSNOThere/Super-Earth-Arsenal-Modpack/releases/download/v2.2.0/Super-Earth-Arsenal-Modpack-v2.2.0.zip)',
        '[Download v' + version + '](https://github.com/CristianiSNOThere/Super-Earth-Arsenal-Modpack/releases/download/v' + version + '/Super-Earth-Arsenal-Modpack-v' + version + '.zip)')
    old = '- **PLAS-39:** hold R and use the left-side Weapon Functions selector. Semi fires one round with a 0.01-second minimum charge and a base 0.30-second interval; the native fire-rate modifier can increase that interval to approximately 0.333 seconds. Burst fires three rounds spaced 0.12 seconds apart with a 0.45-second minimum charge. Both modes keep normal firing audio and the game\'s fire-rate modifier.'
    new = '- **PLAS-39:** hold R and use the left-side Weapon Functions selector. Semi is the quick single shot; Burst charges for about half a second and fires three rounds. Full timings are listed above.'
    readme = readme.replace(old, new)
    path.write_text(readme, encoding='utf-8')
    print('Updated 24 Arsenal descriptions, catalog copy and README from player-guide.json.')

if __name__ == '__main__':
    main()
