"""Punisher incremental integration: shipped functions, payload and baseline audit."""
from pathlib import Path
import argparse, hashlib, json, re, struct, sys, zipfile
import build as b
sys.path.insert(0,str(b.ROOT/'work/expanded-stat-editor'))
from lua_runtime import Lua51

ap=argparse.ArgumentParser();ap.add_argument('candidate',type=Path);ap.add_argument('evidence',type=Path)
args=ap.parse_args();args.evidence.mkdir(parents=True,exist_ok=True)
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
source=b.REPO/'source/punisher-plasma'
runtime=(source/'runtime.lua').read_text()
tail='start(make_api,bridge,prepare,D,modules,helper)'
assert runtime.rstrip().endswith(tail)
prefix=runtime.rstrip()[:-len(tail)]
actual=Lua51();actual.compile(runtime.encode(),'@punisher-pack-accepted.lua')
fixture_results=[]
for name,filename,expected in [('source-native','source-fixture.lua',27),('prepare-registry','prepare-registry-fixture.lua',31)]:
    output=args.evidence/(name+'-cases.txt')
    text=(source/filename).read_text().replace('REPORT_PATH','[====['+output.resolve().as_posix()+']====]')
    script='print=function()end\n'+prefix+text
    (args.evidence/(name+'.lua')).write_text(script)
    actual.run(script.encode(),'@punisher-'+name+'.lua')
    cases=output.read_text().splitlines();assert len(cases)==expected
    fixture_results.append(dict(name=name,cases=len(cases),fixture_sha256=sha(script.encode()),checks=cases))

baseline=b.REPO/'Super-Earth-Arsenal-Modpack-v2.1.3.zip'
origin=b.ROOT/'outputs/punisher-stability-20261016/Punisher-Plasma-StA11-White-Tone-Rev10-Test.zip'
assert sha(origin.read_bytes())=='2C8EA29E61E0FBEDB604C9763634EF478A9368DA8C3DA5F1608C3E9AE6F1FF7C'
def parsed(z,n):
    c=z.read(n);nt,nf=struct.unpack_from('<II',c,4);result={}
    companions=[z.read(n+s) if n+s in z.namelist() else b'' for s in ('','.gpu_resources','.stream')]
    for i in range(nf):
        row=struct.unpack_from('<7Q6I',c,72+nt*32+i*80)
        result[row[:2]]=tuple(blob[row[o]:row[o]+row[l]] for blob,o,l in zip(companions,(2,4,3),(7,9,8)))
    return result
with zipfile.ZipFile(baseline) as old,zipfile.ZipFile(args.candidate) as new,zipfile.ZipFile(origin) as accepted:
    assert new.testzip() is None
    om,nm=(json.loads(z.read('manifest.json')) for z in (old,new))
    assert nm['Version']=='2.2.0' and nm['Guid']==om['Guid'] and nm['Options'][:23]==om['Options']
    assert len(nm['Options'])==24 and nm['Options'][-1]['Name']=='Enable SG-8P Punisher Plasma'
    unchanged=0
    for n in old.namelist():
        if n.startswith('Mods/'):
            assert old.read(n)==new.read(n),n;unchanged+=1
    folder='Mods/punisher-plasma/'
    names=[n for n in new.namelist() if n.startswith(folder)]
    assert len(names)==12
    orig={};pack={}
    for n in accepted.namelist():
        if n.startswith('Addon/') and re.search(r'\.patch_\d+$',n):
            for key,payloads in parsed(accepted,n).items():
                if key in orig:assert orig[key]==payloads
                orig[key]=payloads
    for n in names:
        if re.search(r'\.patch_\d+$',n):
            rs=parsed(new,n);kinds={key[1] for key in rs}
            assert b.LUA not in kinds or kinds=={b.LUA}
            b.resources(new.read(n)) # native type-contiguity/indices/count guards
            for key,payloads in rs.items():
                if key in pack:assert pack[key]==payloads
                pack[key]=payloads
    changed={key for key in orig if orig[key]!=pack.get(key)}
    assert set(orig)==set(pack) and len(pack)==13
    assert changed=={(0x277CD8333685B69C,b.LUA)},changed
    # Data, retained native helper, visuals, entry shim and package stay exact.
    origin_runtime=orig[0x277CD8333685B69C,b.LUA][0][8:].decode().replace('\r\n','\n')
    normalized=runtime
    for name in ('prepare','start'):
        marker=f'local {name}=(function()\n'
        a=normalized.index(marker)+len(marker);end=normalized.index('\nend)()',a)
        oa=origin_runtime.index(marker)+len(marker);oe=origin_runtime.index('\nend)()',oa)
        normalized=normalized[:a]+origin_runtime[oa:oe]+normalized[end:]
    assert normalized==origin_runtime
    assert pack[0xED8FBEEDAAFFC494,b.LUA]==orig[0xED8FBEEDAAFFC494,b.LUA]
    assert b'-- HD2-Addon: mods/codex/punisher_plasma_first_test' in pack[0xED8FBEEDAAFFC494,b.LUA][0]
    implementation=next(parts[0][8:] for (key,kind),parts in pack.items() if kind==b.LUA and len(parts[0])>1000)
    assert implementation==runtime.encode()
    boot=pack[0x9ba626afa44a3aa3,0xad9c6d9ed1e5e77a][0]
    count=struct.unpack_from('<I',boot,8)[0];assert count==4130 and len(boot)==16+count*16
    entries={struct.unpack_from('<QQ',boot,16+i*16) for i in range(count)}
    visual={key for n in ('49f1972458f7ccec','e16e0aa7740716a2') for key in parsed(new,folder+'Addon/'+n+'.patch_0')}
    assert {(kind,key) for key,kind in visual}<=entries
    for stem in ('49f1972458f7ccec','e16e0aa7740716a2'):
        for suffix in ('','.gpu_resources','.stream'):
            path='Addon/'+stem+'.patch_0'+suffix
            assert accepted.read(path)==new.read(folder+path)

# The previous faulty file order must fail the new shared builder guard.
faulty=b.ROOT/'outputs/punisher-stability-20261016/Punisher-Plasma-StA11-Boot-Dependencies-Rev8-Test.zip'
with zipfile.ZipFile(faulty) as z:
    try:b.resources(z.read('Addon/e16e0aa7740716a2.patch_0'))
    except AssertionError as error:assert 'Non-contiguous' in str(error)
    else:raise AssertionError('Historical native-overflow archive accepted')
report=dict(result='PASS',candidate=str(args.candidate),sha256=sha(args.candidate.read_bytes()),
    unchanged_baseline_gameplay_files=unchanged,existing_23_options_exact=True,
    punisher_12_nonimplementation_payloads_exact_accepted_rev10=True,
    only_prepare_start_scheduling_and_exact_post_companion_checks_changed=True,
    both_visual_triplets_byte_exact=True,lua_and_boot_archives_separate=True,
    boot_visual_dependency_closure=True,native_type_order_regression_rejected=True,
    actual_current_fixture_cases=sum(r['cases'] for r in fixture_results),fixtures=fixture_results,
    process_scope='Own disposable fixture process only for native source helper; no game access',
    fresh_combined_startup='NOT RUN',combined_gameplay='NOT RUN')
(args.evidence/'punisher-integration.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='fixtures'},indent=2))
