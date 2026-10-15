"""Build a selectable package from immutable, accepted per-weapon payloads.

The initial import is explicit. Subsequent builds use only this repository's
catalog and payload store. No Arsenal profile or game directory is written.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import re
import struct
import sys
import zipfile

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO.parents[1]
CANON = REPO / 'source/configurable-pack'
OUT = ROOT / 'outputs/configurable-pack-20261015'
EVIDENCE = ROOT / 'work/configurable-pack-20261015'
LUA = 0xA14E8DFA2CD117E2
GUID = 'bf6cb345-73c0-5b9b-a16c-38d490155842'
sha = lambda b: hashlib.sha256(b).hexdigest().upper()

def resource_hash(name):
    data=name.encode();mask=(1<<64)-1;mix=0xC6A4A7935BD1E995
    value=len(data)*mix&mask;end=len(data)//8*8
    for (word,) in struct.iter_unpack('<Q',data[:end]):
        word=word*mix&mask;word^=word>>47;value=(value^(word*mix&mask))*mix&mask
    if data[end:]:value=(value^int.from_bytes(data[end:],'little'))*mix&mask
    value^=value>>47;value=value*mix&mask;return value^(value>>47)

def lua_archive(key,source):
    resource=struct.pack('<II',len(source),2)+source
    offset=192  # align header + one type + one entry to 16 bytes
    body=bytearray(offset)+resource
    body+=b'\0'*(-len(body)%16)
    body[:72]=struct.pack('<III20sQQ24s',0xF0000011,1,1,b'',len(body),0,b'')
    body[72:104]=struct.pack('<IIQIIII',0,0,LUA,1,0,16,16)
    body[104:184]=struct.pack('<7Q6I',key,LUA,offset,0,0,0,0,len(resource),0,0,16,16,0)
    assert resources(bytes(body))=={(key,LUA):resource}
    return bytes(body)


def resources(body):
    assert struct.unpack_from('<I', body)[0] == 0xF0000011
    types, count = struct.unpack_from('<II', body, 4)
    end = 72 + types * 32 + count * 80
    result = {}
    for i in range(count):
        pos = 72 + types * 32 + i * 80
        key, kind, offset = struct.unpack_from('<QQQ', body, pos)
        size = struct.unpack_from('<I', body, pos + 56)[0]
        assert end <= offset <= offset + size <= len(body)
        assert (key, kind) not in result
        result[key, kind] = body[offset:offset + size]
    return result


def import_baseline():
    assert not (CANON / 'catalog.json').exists(), 'Import is one-time; catalog already exists'
    CANON.mkdir(parents=True, exist_ok=True)
    packages = []
    source = ROOT / 'work/rapid-arc-thrower/release-repo/mods'
    zips = sorted(source.glob('*.zip'))
    assert len(zips) == 22 and not any('Punisher' in p.name for p in zips)
    for i, path in enumerate(zips):
        slug = re.sub(r'-v[\d.]+\.zip$', '', path.name).lower()
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None
            m = json.loads(z.read('manifest.json'))
            files = {}
            for name in z.namelist():
                if not name.endswith('/') and name.startswith(('Addon/', 'Settings/')):
                    data = z.read(name)
                    target = CANON / 'payloads' / slug / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
                    files[name] = sha(data)
            main = m['Options'][0]
            title = re.sub(r' v[\d.]+$', '', m['Name'])
            description = m['Description']
            if 'One-True-Flag' in path.name:
                description = ('Configurable normal damage from 0 to 9999, default 300. '
                               'Durable damage is half of normal (rounded down) or equal to normal; default 150.')
            packages.append(dict(index=i, id=slug, name=title, option='Enable ' + title,
                                 description=description, version=m['Version'], guid=m['Guid'],
                                 origin=path.name, origin_sha256=sha(path.read_bytes()),
                                 files=files, includes=main['Include']))
            if 'One-True-Flag' in path.name:
                flag_options = m['Options'][1:]
    catalog = dict(schema=1, guid=GUID, version='2.0.0', baseline='1.0.26',
                   packages=packages, flag_options=flag_options)
    (CANON / 'catalog.json').write_text(json.dumps(catalog, indent=2) + '\n', encoding='utf-8')


def selection_matrix(n=22):
    masks = {0, (1 << n) - 1}
    for k in (1, 2, 3):
        masks.update(sum(1 << i for i in ids) for ids in itertools.combinations(range(n), k))
    masks.update(((1 << n) - 1) ^ (1 << i) for i in range(n))
    assert len(masks) == 1817
    return sorted(masks)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--import-baseline', action='store_true')
    parser.add_argument('--release',action='store_true',help='Use the reviewed public descriptions; preserve all tested gameplay files')
    parser.add_argument('--incremental',action='store_true',help='Audit each option dependency closure without repeating the migration matrix')
    parser.add_argument('--output',type=Path,help='New immutable candidate path; required with --incremental')
    parser.add_argument('--evidence',type=Path,help='New evidence folder; required with --incremental')
    args = parser.parse_args()
    if args.import_baseline:
        import_baseline()
    catalog = json.loads((CANON / 'catalog.json').read_text(encoding='utf-8'))
    packages = catalog['packages']
    if args.incremental:
        assert args.output and args.evidence and not args.import_baseline
        assert (catalog['baseline'],catalog['version'])in {('2.0.0','2.1.0'),('2.1.0','2.1.1')}
        assert len(packages)==23 and catalog['expected_resources']==36
    else:
        assert not args.output and not args.evidence
        assert catalog['version']=='2.0.0', 'Use an explicit new incremental candidate for a changed catalog'
        assert len(packages)==22
    pack_version=catalog['version']
    files = {}
    inventory = {}
    owners = {}
    module_owners = {}
    option_resource_bits = []
    option_dependencies = []
    catalog_detail = []
    key_indexes = {}
    runtime = None
    sys.path.insert(0, str(ROOT / 'work/expanded-stat-editor'))
    from lua_runtime import Lua51
    runtime = Lua51()
    options = []
    assert len({p['guid'] for p in packages})==len(packages) and GUID not in {p['guid'] for p in packages}
    assert [p['index']for p in packages]==list(range(len(packages)))
    assert len({p['id']for p in packages})==len(packages)
    assert len({p['option']for p in packages})==len(packages)
    for p in packages:
        resource_bits = 0
        referenced=set();provided=set()
        for relative, checksum in p['files'].items():
            body = (CANON / 'payloads' / p['id'] / relative).read_bytes()
            assert sha(body) == checksum, relative
            # Legacy digit archives stay in the imported baseline store but are
            # superseded in this package by a single complete-preset selector.
            if not relative.startswith('Settings/'):
                files['Mods/' + p['id'] + '/' + relative] = body
            if not re.search(r'\.patch_\d+$', relative):
                continue
            entries = resources(body)
            kinds = {kind for key, kind in entries}
            assert LUA not in kinds or len(kinds) == 1, 'Mixed Lua/non-Lua archive'
            if not relative.startswith('Addon/'):
                continue
            for key, payload in entries.items():
                assert key not in inventory or inventory[key] == payload, 'Differing shared resource'
                inventory[key] = payload
                provided.add(key)
                owners.setdefault(key, []).append(p['id'])
                if key not in key_indexes:
                    key_indexes[key] = len(key_indexes)
                resource_bits |= 1 << key_indexes[key]
                if key[1] == LUA:
                    length, version = struct.unpack_from('<II', payload)
                    assert length + 8 == len(payload) and version == 2
                    runtime.compile(payload[8:], f'@{key[0]:016x}.lua')
                    referenced.update(name.decode() for name in re.findall(rb'mods/(?:codex|crife)/[A-Za-z0-9_]+',payload[8:]))
                    for mod in re.findall(rb'-- HD2-Addon:\s*([\w/.-]+)', payload[8:]):
                        name = mod.decode()
                        assert name not in module_owners or module_owners[name] == p['id']
                        module_owners[name] = p['id']
        option_resource_bits.append(resource_bits)
        optional={'mods/codex/sterilizer_armor_control'} if p['id']=='tenderizer-armor-softener' else set()
        required={(resource_hash(name),LUA) for name in referenced-optional}
        assert required<=provided, 'Missing dependency in '+p['id']+': '+str(required-provided)
        option_dependencies.append(sum(1<<key_indexes[key] for key in required))
        catalog_detail.append(dict(id=p['id'],option=p['option'],module_references=sorted(referenced),
             optional_peers=sorted(optional),resources=[f'{k:016X}:{t:016X}'for k,t in sorted(provided)]))
        options.append(dict(Name=p['option'], Description=p['description'],
                            Include=['Mods/' + p['id'] + '/' + d for d in p['includes']]))
    assert len(inventory) == catalog.get('expected_resources',34)
    assert (0x8CB98E0A56C28528, LUA) not in inventory
    assert not any(kind == 0xAD9C6D9ED1E5E77A for key, kind in inventory)
    flag = next(p for p in packages if p['id'] == 'one-true-flag')
    flag_option=next(o for o in options if o['Name']==flag['option'])
    flag_option['Description']='Choose normal damage and half or equal durable damage in one dropdown. Default: 300 normal / 150 durable.'
    flag_option['SubOptions']=[]
    template=(CANON/'flag-preset.lua').read_text(encoding='utf-8')
    preset_key=resource_hash('mods/codex/flag_settings/preset')
    assert (preset_key,LUA)not in inventory
    preset_payloads=[]
    for preset in catalog['flag_presets']:
        normal,ratio=preset['normal'],preset['durable_ratio']
        assert 0<=normal<=9999 and ratio in (50,100)
        values={'THOUSANDS':normal//1000*1000,'HUNDREDS':normal//100%10*100,
                'TENS':normal//10%10*10,'ONES':normal%10,'RATIO':ratio}
        source=template
        for token,value in values.items():source=source.replace('@'+token+'@',str(value))
        assert '@'not in source
        runtime.compile(source.encode(),'@flag-preset.lua')
        folder='Mods/one-true-flag/Settings/preset-'+str(normal)+'-'+str(ratio)
        stem=folder+'/9ba626afa44a3aa3.patch_0'
        archive=lua_archive(preset_key,source.encode())
        for suffix,body in [('',archive),('.stream',b''),('.gpu_resources',b'')]:files[stem+suffix]=body
        durable=normal*ratio//100
        label=f'{normal} normal / {durable} durable'+(' (default)'if not flag_option['SubOptions']else '')
        flag_option['SubOptions'].append(dict(Name=label,Description=f'Flag damage: {normal} normal and {durable} durable.',Include=[folder]))
        preset_payloads.append(dict(normal=normal,durable=durable,durable_ratio=ratio,folder=folder,
                                    resource=f'{preset_key:016X}',sha256=sha(archive)))
    assert preset_payloads[0]['normal']==300 and preset_payloads[0]['durable']==150
    manifest = dict(Version=pack_version, Guid=GUID, Name='Super Earth Arsenal Mod Pack',
                    Description=f'Choose any of the {len(packages)} weapon and equipment mods independently. '
                    'Includes configurable One True Flag damage.', Options=options)
    files['manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    # Player-visible behavior stays in the public copy; test evidence is separate.
    readme = ['# Super Earth Arsenal Mod Pack v'+pack_version, '',
              'Choose the weapon and equipment mods you want in Arsenal, then deploy the pack.', '',
              'Requires Bingus Shared Loader. Select each desired mod in the pack options. '
              'When importing or upgrading from v1, review the new switches before deploying. '
              'Use this pack in place of the corresponding individual mods.', '',
              'One True Flag has one damage dropdown, defaulting to 300 normal / 150 durable. '
              'Choose a normal-damage preset from 0 to 9999 with half or equal durable damage. '
              'Its dropdown is inside the One True Flag option.', '',
              'Gas Overhaul and Tenderizer extend the shared Acid Storm effect to 15 seconds, '
              'including Acid Storm weather. Autocannon and Epoch share their reload animation adjustment. '
              'Autocannon also changes the explosion shared with the JAR-5 Dominator.', '',
              '| Option | Changes |', '|---|---|']
    readme += ['| ' + p['name'] + ' | ' + (flag_option['Description'] if p['id']==flag['id']else p['description']).replace('|', '/') + ' |' for p in packages]
    files['README.md'] = ('\n'.join(readme) + '\n').encode('utf-8')
    if args.release or args.incremental:
        public=json.loads((CANON/'release-metadata.json').read_text(encoding='utf-8'))
        manifest['Description']=public['description']
        for option in manifest['Options']:
            option['Description']=public['option_descriptions'].get(option['Name'],option['Description']) if args.incremental and not args.release else public['option_descriptions'][option['Name']]
        if args.incremental and not args.release:
            manifest['Description']=catalog.get('candidate_description',f'Choose from {len(packages)} independently selectable weapon and equipment mods, including BR-14 Adjudicator Heavy Battle Rifle. One True Flag has one dropdown with 29 damage presets (default 300 normal / 150 durable).')
        files['manifest.json']=(json.dumps(manifest,indent=2)+'\n').encode()
        if args.release:files['README.md']=(REPO/'README.md').read_bytes()
    evidence=args.evidence if args.incremental else EVIDENCE
    evidence.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    zip_path = args.output if args.incremental else ((REPO/'Super-Earth-Arsenal-Modpack-v2.0.0.zip') if args.release else (OUT/'Super-Earth-Arsenal-Modpack-v2.0.0-Selectable-Rev3-Test.zip'))
    zip_path.parent.mkdir(parents=True,exist_ok=True)
    import io
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, body in sorted(files.items()):
            entry = zipfile.ZipInfo(name, (2026, 10, 15, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(entry, body)
    body = buffer.getvalue()
    if zip_path.exists():
        assert zip_path.read_bytes() == body, 'Immutable candidate differs; use a new revision'
    else:
        zip_path.write_bytes(body)
    with zipfile.ZipFile(zip_path) as z:
        assert z.testzip() is None
    assert not any('/' not in n and '.patch_' in n for n in files)
    # Each option contains its complete accepted dependency closure. Identical
    # overlaps were proven above. Enumerate every mask and construct its union.
    if args.incremental:
        # Each option supplies its own dependency closure; identical overlaps
        # above prove the same property for any union without mask enumeration.
        for available,required in zip(option_resource_bits,option_dependencies):
            assert available and available&required==required
        changed=catalog.get('changed_package_ids',[packages[-1]['id']])
        assert changed and set(changed)<={p['id']for p in packages}
        matrix=sorted({1<<p['index']for p in packages if p['id']in changed}|{(1<<len(packages))-1})
        checked_masks=None
    else:
        unions = [0] * (1 << len(packages))
        needed = [0] * (1 << len(packages))
        for mask in range(1, len(unions)):
            low = mask & -mask
            unions[mask] = unions[mask ^ low] | option_resource_bits[low.bit_length() - 1]
            needed[mask] = needed[mask ^ low] | option_dependencies[low.bit_length()-1]
            assert unions[mask] != 0
            assert unions[mask]&needed[mask]==needed[mask], 'Selection has an unresolved module dependency'
        matrix = selection_matrix()
        checked_masks=len(unions)
    (evidence / 'selections.json').write_text(json.dumps(matrix))
    detail = dict(result='PASS', artifact=str(zip_path), sha256=sha(body), bytes=len(body),
                  baseline=(str(22 if catalog['baseline']=='2.0.0'else 23)+' mods / v'+catalog['baseline']if args.incremental else '22 mods / v1.0.26'), package_guid=GUID, options=len(options),
                  mod_switches=len(packages), flag_controls=1, flag_dropdown_presets=preset_payloads,all_selection_masks=checked_masks,
                  runtime_selection_masks=len(matrix), resources=len(inventory),
                  differing_payload_collisions=0, unchanged_accepted_payloads=True,
                  dependency_check='Each option provides its full closure; shared overlaps byte-identical',
                  pure_lua_archives=True, root_patch_files=0,
                  removed_pack_only_resources=['8CB98E0A56C28528', '9BA626AFA44A3AA3:AD9C6D9ED1E5E77A'],
                  selection_dependencies=('Every option closure checked against referenced Lua resource keys; Tenderizer Gas peer is optional'if args.incremental else 'All masks checked against referenced Lua resource keys; Tenderizer Gas peer is optional'),
                  package_catalog=catalog_detail,
                  modules=module_owners,
                  resources_detail=[dict(key=f'{k:016X}', kind=f'{t:016X}', sha256=sha(v), owners=owners[k,t])
                                    for (k,t),v in sorted(inventory.items())])
    (evidence / ('composition.json'if args.incremental else ('release-composition-v2.0.0.json'if args.release else 'composition-rev3.json'))).write_text(json.dumps(detail, indent=2) + '\n')
    print(json.dumps({k:v for k,v in detail.items() if k not in ('resources_detail','modules','package_catalog','flag_dropdown_presets')}, indent=2))


if __name__ == '__main__':
    main()
