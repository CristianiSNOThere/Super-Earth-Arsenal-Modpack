"""Refresh full public descriptions while preserving the original README table."""
from pathlib import Path
import json
import re

REPO = Path(__file__).resolve().parents[2]
CANON = REPO / 'source/configurable-pack'

def main():
    guide = json.loads((CANON / 'player-guide.json').read_text(encoding='utf-8'))
    catalog = json.loads((CANON / 'catalog.json').read_text(encoding='utf-8'))
    public = json.loads((CANON / 'release-metadata.json').read_text(encoding='utf-8'))
    assert set(guide) == {p['option'] for p in catalog['packages']}
    for package in catalog['packages']:
        text = guide[package['option']]
        assert isinstance(text,str) and text and '|' not in text
        public['option_descriptions'][package['option']] = text
        package['description'] = text
    public['description'] = ('Choose any of 24 Helldivers 2 weapon and equipment mods independently in Arsenal, '
        'including SG-8P Punisher Plasma with Normal and Shotgun modes. One True Flag offers 29 damage presets, '
        'defaulting to 300 normal damage and 150 against durable parts. Gas Overhaul supports Health Rework Normal and Casual.')
    for name,data in [('catalog.json',catalog),('release-metadata.json',public)]:
        (CANON/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    path = REPO/'README.md'
    readme = path.read_text(encoding='utf-8')
    start,end = readme.index('## Gameplay changes\n'),readme.index('## Shared effects\n')
    section = ('## Gameplay changes\n\n'
        'Normal damage and damage against durable parts are listed separately; durable damage is the value used by the game\'s durability system, not extra damage added on top. '
        'Timings and awkward decimals are rounded for readability.\n\n'
        '| Mod | Gameplay settings |\n|---|---|\n')
    order = ['SG-8P Punisher Plasma','BR-14 Adjudicator Heavy Battle Rifle','Tenderizer Armor Softener','Sickle Laser AR',
        'VG-70 Variable Portable Maxigun Rework','PLAS-45 Epoch Highest-Charge Rework','AR-32 Pacifier Tuning',
        'AC-8 Autocannon Backpackless Rework','PLAS-1 Scorcher AR','One True Flag','SAI Focus Precision',
        'AR-11 Arbitrator','R/40-K Hot-Shot','Gas Overhaul','ARC-3 Rapid/Supercharge','ARC-12 Blitzer',
        'CQC-20 Breaching Hammer','PLAS-39 Accelerator Rifle','P-34 Breacher','S-11 Speargun',
        'APW-1 Anti-Materiel Rifle','40-K Meltagun','A/GM-17 Gas Mortar Sentry','RS-422 Railgun']
    assert set('Enable '+n for n in order) == set(guide)
    labels = {'PLAS-45 Epoch Highest-Charge Rework':'PLAS-45 Epoch','AR-32 Pacifier Tuning':'AR-32 Pacifier',
        'AC-8 Autocannon Backpackless Rework':'AC-8 Autocannon'}
    for name in order:
        text = guide['Enable '+name].replace('\n\n','<br><br>')
        section += '| '+labels.get(name,name)+' | '+text+' |\n'
    readme = readme[:start]+section+'\n'+readme[end:]
    version = catalog['version']
    readme = re.sub(r'^# Super Earth Arsenal Mod Pack v\d+\.\d+\.\d+', '# Super Earth Arsenal Mod Pack v'+version, readme, count=1)
    readme = re.sub(r'\[Download v\d+\.\d+\.\d+\]\(https://github.com/CristianiSNOThere/Super-Earth-Arsenal-Modpack/releases/download/v[\d.]+/Super-Earth-Arsenal-Modpack-v[\d.]+\.zip\)',
        '[Download v'+version+'](https://github.com/CristianiSNOThere/Super-Earth-Arsenal-Modpack/releases/download/v'+version+'/Super-Earth-Arsenal-Modpack-v'+version+'.zip)',readme)
    path.write_text(readme,encoding='utf-8')
    print('Refreshed full prose for 24 mods in the original README table and Arsenal.')

if __name__ == '__main__':
    main()
