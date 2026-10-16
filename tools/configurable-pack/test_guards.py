"""Run current shipped validators and transactions on local fixture memory."""
from pathlib import Path
import ast
import json
import re
import sys

import build as b
from test_runtime import literal
sys.path.insert(0, str(b.ROOT / 'work/expanded-stat-editor'))
from lua_runtime import Lua51

def text(path):
    return Path(path).read_text(encoding='utf-8').replace('\r\n','\n')

def constant(path, name):
    for node in ast.parse(text(path)).body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets):
            return ast.literal_eval(node.value)
    raise KeyError(name)

def patch_source(src):
    start=src.index('local patch=(function()')
    return src[start:src.index('\nlocal start=(function()',start)].rstrip()+'\n'

def main():
    runtime=Lua51()
    evidence=b.EVIDENCE
    resource_dir=evidence/'resources'
    # Extract current accepted text directly from the canonical archives.
    current={}
    catalog=json.loads((b.CANON/'catalog.json').read_text())
    for p in catalog['packages']:
        for rel in p['files']:
            if rel.startswith('Addon/') and re.search(r'\.patch_\d+$',rel):
                for (key,kind),body in b.resources((b.CANON/'payloads'/p['id']/rel).read_bytes()).items():
                    if kind==b.LUA and not body[8:].startswith(b'\x1bLJ'):
                        current[key]=body[8:].decode().replace('\r\n','\n')
    results=[]
    def run(name, source, detail):
        path=evidence/(name+'.lua');path.write_text(source,encoding='utf-8')
        runtime.run(source.encode(), '@configurable-'+name+'.lua')
        results.append(dict(name=name,result='PASS',fixture_sha256=b.sha(source.encode()),**detail))
        print('PASS:',name,flush=True)

    flag=current[0x729D8C8BF0D51D90]
    flagpatch=patch_source(flag)
    oldtest=constant(b.ROOT/'work/compatibility-candidates-20261007/test_flag_order.py','test')
    flag_fixture=(b.ROOT/'work/flag-mod/fixture.bin').as_posix()
    run('flag-peer-subsets',flagpatch+oldtest.replace('FIXTURE',literal(flag_fixture)),
        dict(accepted_subsets=8,unknown_byte_refusals=1,unsupported_status_refusals=1))
    flag_settings=flagpatch+r'''
for n=0,9999 do
 local opts={thousands=math.floor(n/1000)*1000,hundreds=math.floor(n/100)%10*100,
  tens=math.floor(n/10)%10*10,ones=n%10}
 local normal,durable=patch.damage_values(opts);assert(normal==n and durable==math.floor(n/2))
 opts.durable_ratio=100;normal,durable=patch.damage_values(opts);assert(normal==n and durable==n)
end
local normal,durable=patch.damage_values(nil);assert(normal==300 and durable==150)
for _,opts in ipairs({{ones=-1},{ones=10},{tens=1},{hundreds=1000},{durable_ratio=75}})do
 assert(not pcall(patch.damage_values,opts),'Invalid Flag settings accepted')
end
'''
    # The settings resources are configuration only. Execute every selector
    # without the Flag entrypoint and ensure none installs an update callback.
    settings=[]
    p=next(p for p in catalog['packages'] if p['id']=='one-true-flag')
    for rel in p['files']:
        if rel.startswith('Settings/') and re.search(r'\.patch_\d+$',rel):
            for (key,kind),body in b.resources((b.CANON/'payloads'/p['id']/rel).read_bytes()).items():
                assert kind==b.LUA
                settings.append(body[8:].decode())
    flag_settings+='local settings='+literal(settings)+r'''
for _,source in ipairs(settings)do
 _G.FlagDamagePrototypeV1=nil;_G.FlagDamageOptionsV1=nil
 local previous=update;assert(loadstring(source))()
 assert(update==previous and FlagDamagePrototypeV1==nil,'Disabled Flag settings installed gameplay logic')
end
'''
    run('flag-settings',flag_settings,dict(valid_damage_cases=20001,invalid_settings=5,disabled_flag_selectors=len(settings)))

    sai=current[0x8BA5FD7BC87570D8]
    gas=current[0xE54E34210BAC937E]
    saved=text(b.ROOT/'work/sai-rebalance-20261014/transaction-fixture-final.lua')
    # Saved harness is reusable only after exact equality with the shipped
    # transaction bodies; the sole change exposes private guard functions.
    sai_prefix=sai[:sai.index('local start=(function()')]
    assert saved.startswith(sai_prefix),'Saved SAI fixture is stale'
    gaspatch=patch_source(gas).replace('local patch=(function()','local gas=(function()',1)
    gaspatch=gaspatch.replace('return patch','patch.validate_damage=validate_damage;patch.peer_damage=peer_damage;return patch',1)
    if gaspatch.strip() not in saved:
        # v2.1.2 changes the health validator; retain the archived SAI harness.
        import zipfile
        with zipfile.ZipFile(b.REPO/'Super-Earth-Arsenal-Modpack-v2.1.1.zip') as old_zip:
            body=old_zip.read('Mods/gas-overhaul/Addon/9ba626afa44a3aa3.patch_0')
        old_gas=b.resources(body)[(0xE54E34210BAC937E,b.LUA)][8:].decode().replace('\r\n','\n')
        old_patch=patch_source(old_gas).replace('local patch=(function()','local gas=(function()',1)
        old_patch=old_patch.replace('return patch','patch.validate_damage=validate_damage;patch.peer_damage=peer_damage;return patch',1)
        assert saved.count(old_patch.strip())==1,'Archived Gas fixture is stale'
        saved=saved.replace(old_patch.strip(),gaspatch.strip())
    assert gaspatch.strip() in saved,'Saved Gas fixture is stale'
    run('sai-gas-transactions',saved,dict(actual_transactions_and_refusals=45,
        covers='Current 70/37.5 MRAD, recoil/heat, prior peer orders, unknown rows/statuses, partial writes, rollback and original protection'))

    # Reuse the test data and assertions, executing the CURRENT Gas validator.
    gas_old=text(b.REPO/'source/gas-overhaul/validator-fixture.lua')
    harness=gas_old[gas_old.index('local path=[====['):]
    harness=harness.replace('local function case(version,status,n,d,reject,offset,extra)',
        'local CASES=0\nlocal function case(version,status,n,d,reject,offset,extra)\n CASES=CASES+1')
    extra=constant(b.ROOT/'work/compatibility-candidates-20261007/test_gas_subsets.py','extra')
    current_status=re.findall(r"return '(Applied:[^'\n]+)'",sai)[-1]
    extra=re.sub(r"local sai_status='[^']+'",'local sai_status='+literal(current_status),extra)
    extra=extra.replace('_G.SaiFocusModV1={active=true,status=sai_status}',"_G.SaiFocusModV1={active=true,version='0.10',status=sai_status}")
    harness+='\n'+extra+'\nlocal f=assert(io.open('+literal((evidence/'gas-guard-count.txt').as_posix())+",'w'));f:write(CASES);f:close()\n"
    api=gas[:gas.index('local patch=(function()')]
    validators=patch_source(gas).replace('local patch=(function()','local validate,acid=(function()',1)
    validators=validators.replace('return patch','return validate_damage,validate_acid_status',1)
    run('gas-current-peer-subsets',api+validators+harness,dict(current_peer_subsets=16,
        covers='Exact current SAI, Flag, AR-11 and ARC subsets; ARC Heavy/light rows; absent/mismatched peers and altered bytes refuse'))
    results[-1]['total_validator_cases']=int((evidence/'gas-guard-count.txt').read_text())

    for name,source_folder,fixture_folder in [
        ('sickle','sickle-laser-ar','sickle-double-edge-20261015'),
        ('tenderizer','tenderizer-armor','tenderizer-armor-20261015-rev3'),
    ]:
        src=text(b.REPO/'source'/source_folder/'entry.lua')
        fixture=constant(b.ROOT/'work'/fixture_folder/'verify.py','FIXTURE')
        prefix='local data_path='+literal((b.ROOT/'work/flag-mod/filediver-master/datalibrary').as_posix())+'\n'
        prefix+='local report_path='+literal((evidence/(name+'-transaction-count.txt')).as_posix())+'\n'
        prefix+="local function unhex(s)return(s:gsub('..',function(h)return string.char(tonumber(h,16))end))end\n"
        prefix+=src[:src.index('local start=(function()')]
        run(name+'-transactions',prefix+fixture,dict(covers='Shipped clone transactions, stock-only changes, peer state, partial writes, foreign mutations, reverse rollback, own-process memory adapter'))
        results[-1]['actual_fixture_cases']=int((evidence/(name+'-transaction-count.txt')).read_text())

    # All embedded Variable modules must match before reusing its complete
    # synthetic native-manager fixture. There is no executable hook allocation.
    saved=text(b.ROOT/'work/vg70-variable-20261013/runtime-offline-fixture-rev12.lua')
    for filename in ['native.lua','component-profile.lua','mode-profile.lua','compatibility-profile.lua','transaction-profile.lua','runtime.lua']:
        src=text(b.REPO/'source/vg70-variable'/filename).strip()
        assert src in saved,'Variable fixture differs from shipped '+filename
    run('variable-full-runtime',saved,dict(covers='Actual startup/discovery/transactions, two isolated owners, nine mode/rate cases, ownership refusal, compaction and new pickup'))

    report=dict(result='PASS',groups=results,external_process_access=False,
                game_directory_changed=False,profile_changed=False,
                scope='Actual current code in local synthetic buffers; no live startup, resource inspection or gameplay assertion')
    (evidence/'guard-transactions.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
