"""Test every new preset with the real Flag transaction and SAI/Gas guards."""
import json
import re
import sys
import zipfile
import build as b
from test_runtime import literal
from test_guards import patch_source
sys.path.insert(0,str(b.ROOT/'work/expanded-stat-editor'))
from lua_runtime import Lua51

def main():
    report=json.loads((b.EVIDENCE/'composition-rev3.json').read_text())
    old=json.loads((b.EVIDENCE/'composition.json').read_text())
    assert report['resources_detail']==old['resources_detail'],'Gameplay resource changed'
    bodies={}
    with zipfile.ZipFile(report['artifact'])as z:
        for name in z.namelist():
            if '/Addon/'in name and re.search(r'\.patch_\d+$',name):
                for (key,kind),data in b.resources(z.read(name)).items():
                    if kind==b.LUA and not data[8:].startswith(b'\x1bLJ'):
                        bodies[key]=data[8:].decode().replace('\r\n','\n')
        presets=[]
        for preset in report['flag_dropdown_presets']:
            data=z.read(preset['folder']+'/9ba626afa44a3aa3.patch_0')
            assert b.sha(data)==preset['sha256']
            entries=b.resources(data);assert len(entries)==1
            presets.append(dict(**preset,source=next(iter(entries.values()))[8:].decode()))
    gas=bodies[0xE54E34210BAC937E]
    source=gas[:gas.index('local patch=(function()')]
    source+=patch_source(bodies[0x729D8C8BF0D51D90]).replace('local patch=(function()','local flag=(function()',1)
    source+=patch_source(bodies[0x8BA5FD7BC87570D8]).replace('local patch=(function()','local sai=(function()',1).replace('return patch','patch.validate_damage=damage;return patch',1)
    source+=patch_source(gas).replace('local patch=(function()','local gas=(function()',1).replace('return patch','patch.validate_damage=validate_damage;return patch',1)
    source+='local presets='+literal(presets)+'\n'
    source+='local fixture_path='+literal((b.ROOT/'work/flag-mod/fixture.bin').as_posix())+'\n'
    source+=r'''
local ffi=require('ffi')
local f=assert(io.open(fixture_path,'rb'));local original=f:read('*a');f:close()
for _,preset in ipairs(presets)do
 _G.FlagDamagePrototypeV1=nil;_G.SaiFocusModV1=nil
 _G.AR11ArbitratorModV1=nil;_G.RapidArcThrowerV1=nil
 _G.FlagDamageOptionsV1={thousands=9000,hundreds=900,tens=90,ones=9,durable_ratio=100}
 local previous_update=update
 assert(loadstring(preset.source))()
 assert(update==previous_update and FlagDamagePrototypeV1==nil,'Settings installed gameplay handler')
 local n,d=flag.damage_values(FlagDamageOptionsV1)
 assert(n==preset.normal and d==preset.durable,'Preset did not replace every field')
 local allocation=ffi.new('uint8_t[?]',#original);local p=ffi.cast('uint8_t *',allocation)
 ffi.copy(p,original,#original);ffi.cast('uintptr_t *',p+84)[0]=ffi.cast('uintptr_t',p+100)
 local api=make_api();api.candidates=function()return{p}end
 local ok,status=flag.apply(api,0);assert(ok,status)
 assert(tonumber(ffi.cast('uint32_t *',p+41980)[0])==n)
 assert(tonumber(ffi.cast('uint32_t *',p+41984)[0])==d)
 _G.FlagDamagePrototypeV1={active=true,version='0.9',status=status}
 assert(sai.validate_damage(api,p),'SAI guard rejected preset '..n..'/'..d)
 assert(gas.validate_damage(api,p),'Gas guard rejected preset '..n..'/'..d)
end
'''
    fixture=b.EVIDENCE/'flag-presets-rev3.lua';fixture.write_text(source,encoding='utf-8')
    Lua51().run(source.encode(),'@flag-preset-transactions.lua')
    discovery=(b.ROOT/'work/flag-mod/BingusSharedLoader-main/src/discover.lua').as_posix()
    loader_cases=0
    for folder in (b.EVIDENCE/'flag-loader-rev3').iterdir():
        paths=sorted(p.as_posix()for p in folder.glob('*.patch_*'))
        assert len(paths)==2
        test='local d=dofile('+literal(discovery)+')\n'
        test+='local paths='+literal(paths)+'\n'
        test+="local entries,warnings=d.scan(paths,d.hasher(require('ffi'),require('bit')),io.open)\n"
        test+="assert(#warnings==0 and #entries==2);assert(entries[1]=='mods/codex/flag_settings/preset'and entries[2]=='mods/codex/flag_damage_prototype')\n"
        Lua51().run(test.encode(),'@actual-flag-loader-order.lua');loader_cases+=1
    result=dict(result='PASS',presets=len(presets),actual_flag_transactions=len(presets),
                actual_sai_guard_checks=len(presets),actual_gas_guard_checks=len(presets),
                previous_gameplay_resources_exact=True,configuration_only=True,
                actual_loader_order_cases=loader_cases,
                external_game_process_access=False,fixture_sha256=b.sha(source.encode()))
    (b.EVIDENCE/'flag-presets-transactions-rev3.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
