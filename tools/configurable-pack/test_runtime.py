"""Actual Lua startup controllers and loader discovery, isolated from the game.

The matrix tests scheduling, profile registration and peer readiness. Its patch
adapters return fixture results; transaction correctness is tested separately.
It is deliberately not reported as a live game startup or gameplay test.
"""
from pathlib import Path
import importlib.util
import json
import random
import re
import sys

import build as b
sys.path.insert(0, str(b.ROOT / 'work/expanded-stat-editor'))
from lua_runtime import Lua51

def literal(value):
    if isinstance(value, str):
        delimiter = '===='
        while ']' + delimiter + ']' in value:
            delimiter += '='
        return '[' + delimiter + '[' + value + ']' + delimiter + ']'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return '{' + ','.join(literal(x) for x in value) + '}'
    if isinstance(value, dict):
        return '{' + ','.join('[ ' + literal(k) + ' ]=' + literal(v) for k,v in value.items()) + '}'
    raise TypeError(value)

def source_controller(src):
    src = src.replace('\r\n', '\n')
    src = src.split('\nlocal start_interrupt=', 1)[0]
    match = re.search(r'local start\s*=\s*\(function\(\)', src)
    if match:
        tail = src[match.end():]
        end = tail.rindex('\nend)()')
        return tail[:end]
    start = src.index('local function start(make_api)')
    end = src.rindex('\nstart(make_api)')
    return src[start:end].replace('local function start(make_api)', 'return function(make_api)', 1)

def source_function(src, name, next_marker):
    start = src.index('function EXT.' + name + '(')
    end = src.index(next_marker, start)
    return src[start:end]

def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--incremental',action='store_true')
    parser.add_argument('--evidence',type=Path)
    parser.add_argument('--focus-id',default='adjudicator-heavy')
    parser.add_argument('--focus-pairs',action='store_true',help='Also test the changed mod with each existing option, in both orders')
    parser.add_argument('--peer-ids',nargs='*',default=[],help='Only the named shared consumers, plus combined/disabled cases')
    args=parser.parse_args()
    if args.incremental:assert args.evidence
    else:assert not args.evidence
    evidence=args.evidence if args.incremental else b.EVIDENCE
    evidence.mkdir(parents=True,exist_ok=True)
    runtime = Lua51()
    catalog = json.loads((b.CANON / 'catalog.json').read_text())
    packets, all_resources = [], {}
    for p in catalog['packages']:
        lua, paths, modules = {}, [], []
        for rel in p['files']:
            if not rel.startswith('Addon/') or not re.search(r'\.patch_\d+$',rel):
                continue
            path = b.CANON / 'payloads' / p['id'] / rel
            paths.append(path.as_posix())
            for key, data in b.resources(path.read_bytes()).items():
                all_resources[key] = data
                if key[1] == b.LUA:
                    lua[key[0]] = data[8:]
                    modules += [x.decode() for x in re.findall(rb'-- HD2-Addon:\s*([\w/.-]+)', data[8:])]
        packets.append(dict(id=p['id'], paths=paths, modules=modules, lua=lua))

    # Prove the source used for controller extraction produces the shipped code.
    sources = {}
    compiled_checks = []
    mappings = {
        0x9523A79B7FC84D55: 'startup-initialization/runtime.lua',
        0x18D24F3D954046AB: 'scorcher-ar/runtime.lua',
        0x44F5D85AAC628A2C: 'sickle-laser-ar/entry.lua',
        0x3F6806D454115A81: 'tenderizer-armor/entry.lua',
        0x2B2BF12F46CB74AC: 'plas39-accelerator-rifle/implementation.lua',
        0xF157B721BA21CD57: 'vg70-variable/implementation.lua',
    }
    if args.incremental:
        identity=json.loads((b.REPO/'source/adjudicator-heavy/identity.json').read_text())
        mappings[int(identity['implementation_key'],16)]='adjudicator-heavy/entry.lua'
        if any(p['id']=='gl52-de-escalator' for p in catalog['packages']):
            identity=json.loads((b.REPO/'source/gl52-de-escalator/identity.json').read_text())
            mappings[int(identity['implementation_key'],16)]='gl52-de-escalator/entry.lua'
    for (key,kind), data in all_resources.items():
        if kind != b.LUA:
            continue
        code = data[8:]
        if code.startswith(b'\x1bLJ'):
            if key not in mappings:
                continue
            # All six chunks have short ULEB128 chunk names.
            assert code[5] < 128
            name = code[6:6+code[5]].decode()
            path = b.REPO / 'source' / mappings[key]
            src = path.read_bytes()
            assert runtime.compile(src, name) == code, f'Source differs from shipped bytecode: {path}'
            compiled_checks.append(mappings[key])
            sources[key] = src.decode()
        else:
            sources[key] = code.decode()

    controllers = {}
    metadata = {}
    for p in packets:
        # Punisher's source/native installer has a distinct six-argument
        # controller, exercised explicitly below and by its transaction fixture.
        if p['id']=='punisher-plasma':
            continue
        for key in p['lua']:
            src = sources.get(key, '')
            if not re.search(r'local start\s*=\s*\(function\(\)', src) and 'local function start(make_api)' not in src:
                continue
            # Variable has its own full synthetic-runtime fixture; matrix uses
            # its exact readiness function below without replacing that runtime.
            if key == 0xF157B721BA21CD57:
                continue
            control = source_controller(src)
            global_match = re.search(r"rawget\(_G,\s*'([^']+)'\)", control)
            assert global_match, p['id']
            normal = re.findall(r"return '(Applied:[^'\n]+)'", src.split('\nlocal start_interrupt=',1)[0])
            status = normal[-1] if normal else 'Applied: scheduling fixture'
            if p['id'] == 'ac-8-autocannon':
                status = 'Applied: AC-8 scheduling fixture'
            if p['id'] == 'plas-45-epoch':
                status = 'Applied: Epoch scheduling fixture'
            controllers[p['id']] = control
            metadata[p['id']] = dict(global_name=global_match[1], status=status,
                                     returns_boolean=('make_api,patch)' in control or 'make_api, patch,' in control or 'make_api, patch)' in control))
    # Twelve controllers: 11 dedicated patches and PLAS-39's mode controller.
    expected_controllers=14 if any(p['id']=='gl52-de-escalator' for p in catalog['packages']) else (13 if args.incremental else 12)
    assert len(controllers) == expected_controllers, list(controllers)
    profile_chunks = {}
    for p in packets:
        chunks = [sources[key] for key in p['lua'] if key in sources and '.register_profile({' in sources[key]]
        if chunks:
            assert len(chunks) == 1
            profile_chunks[p['id']] = chunks[0]
    assert len(profile_chunks) == 10
    shared = sources[0x9523A79B7FC84D55]
    scorcher = sources[0x18D24F3D954046AB]
    def api_chunk(src):
        return (source_function(src, 'register_profile', "rawset(_G,") +
                source_function(src, 'preset_peers_ready', '\nlocal function prepare'))
    common_api = api_chunk(shared)
    scorcher_api = api_chunk(scorcher)
    variable_gate = (b.REPO / 'source/vg70-variable/compatibility-profile.lua').read_text()
    tenderizer_profile = (b.REPO / 'source/tenderizer-armor/profile.lua').read_text()
    filtration_source = ''
    gas_source = sources.get(0xE54E34210BAC937E, '').replace('\r\n','\n')
    if '\nlocal filtration=(function()' in gas_source:
        filtration_source = (b.REPO/'source/gas-overhaul/filtration.lua').read_text().strip()
        embedded=gas_source.split('\nlocal filtration=(function()\n',1)[1].rsplit('\nend)()\nfiltration.start',1)[0]
        assert embedded.strip()==filtration_source
    n=len(packets)
    assert n==(len(catalog['packages']) if args.incremental else 22)
    orders = [list(range(1,n+1)), list(range(n,0,-1))]
    if not args.incremental:
        for seed in (1107,2911):
            order = list(range(1,n+1)); random.Random(seed).shuffle(order); orders.append(order)
    focus=next(i for i,p in enumerate(packets)if p['id']==args.focus_id)if args.incremental else None
    masks = [1<<focus,(1<<n)-1] if args.incremental else b.selection_matrix()
    if args.focus_pairs:
        assert args.incremental
        masks=sorted(set(masks)|{0,((1<<n)-1)^(1<<focus)}|{(1<<focus)|(1<<i)for i in range(n)if i!=focus})
    if args.peer_ids:
        assert args.incremental and not args.focus_pairs
        indices={p['id']:i for i,p in enumerate(packets)}
        assert set(args.peer_ids)<=set(indices)
        masks=sorted(set(masks)|{0,((1<<n)-1)^(1<<focus)}|{(1<<focus)|(1<<indices[p])for p in args.peer_ids})
    script = 'local controllers=' + literal(controllers) + '\n'
    script += 'local metadata=' + literal(metadata) + '\n'
    script += 'local profile_chunks=' + literal(profile_chunks) + '\n'
    script += 'local common_api=' + literal(common_api) + '\nlocal scorcher_api=' + literal(scorcher_api) + '\n'
    script += 'local variable_gate_source=' + literal(variable_gate) + '\n'
    script += 'local tenderizer_profile_source=' + literal(tenderizer_profile) + '\n'
    script += 'local filtration_source=' + literal(filtration_source) + '\n'
    script += 'local packets=' + literal([{k:v for k,v in p.items() if k != 'lua'} for p in packets]) + '\n'
    script += 'local masks=' + literal(masks) + '\nlocal orders=' + literal(orders) + '\n'
    script += 'local discovery_path=' + literal((b.ROOT / 'work/flag-mod/BingusSharedLoader-main/src/discover.lua').as_posix()) + '\n'
    script += 'local report_path=' + literal((evidence / 'runtime-counts.json').as_posix()) + '\n'
    script += 'local incremental='+literal(args.incremental)+'\n'
    script += 'local focus_id='+literal(args.focus_id)+'\n'
    punisher=next((p for p in packets if p['id']=='punisher-plasma'),None)
    punisher_setup=''
    if punisher:
        source=next(sources[key] for key in punisher['lua'] if len(sources.get(key,''))>1000)
        tail='start(make_api,bridge,prepare,D,modules,helper)'
        assert source.rstrip().endswith(tail)
        punisher_setup=source.rstrip()[:-len(tail)]+'\nreturn {start=start,D=D}\n'
    script+='local punisher_setup='+literal(punisher_setup)+'\n'
    script += r'''
local bit=require('bit')
local discovery=dofile(discovery_path)
local hash=discovery.hasher(require('ffi'),bit)
local dumps={}
local function execute(source,env,name)
 local code=dumps[source]
 if not code then code=string.dump(assert(loadstring(source,name)));dumps[source]=code end
 local fn=assert(loadstring(code,name));setfenv(fn,env);return fn()
end
local function make_environment()
 local env={};setmetatable(env,{__index=_G});env._G=env
 env.print=function()end
 return env
end
local discoveries,cases,controller_calls,profiles=0,0,0,0
local filtration_startups=0
for _,mask in ipairs(masks)do
 local paths,expected={},{}
 for i,p in ipairs(packets)do if bit.band(mask,2^(i-1))~=0 then
  for _,path in ipairs(p.paths)do paths[#paths+1]=path end
  for _,name in ipairs(p.modules)do expected[name]=true end
 end end
 local entries,warnings=discovery.scan(paths,hash,io.open)
 assert(#warnings==0,table.concat(warnings,';'))
 local actual={};for _,name in ipairs(entries)do assert(expected[name],name);actual[name]=true end
 for name in pairs(expected)do assert(actual[name],'Missing selected module: '..name)end
 discoveries=discoveries+1
 for _,order in ipairs(orders)do
  local env=make_environment()
  local now,base_calls=0,0
  local common,scorcher
  local adapters={}
  local profile=(execute(tenderizer_profile_source,env,'@shipped-tenderizer-profile'))
  env.profile=profile
  env.CowboyBingusModLoader={modules={}}
  for name in pairs(expected)do env.CowboyBingusModLoader.modules[name]='declared' end
  env.update=function(a,b)base_calls=base_calls+1;return a,b end
  local function make_api()
   return{now=function()return now end,module=function(name)return name and 'game'or 'exe'end,
    module_hash=function(name)return name=='game'and '2E2C3B7C2500646DADD5F2B4C6E0504DBB7E7896139F64CDDC0D1813C718F51E'
      or 'F5FEE03DCFDB2E553A4752C283590950AC13316B376D8196AA556FF0400D5F06'end}
  end
  local function runtime_api(kind)
   local ext={profile_registry={},required_peers={}}
   local e=setmetatable({EXT=ext,log=function()end},{__index=env})
   execute(kind=='scorcher'and scorcher_api or common_api,e,'@shipped-runtime-api')
   local state={phase='preparing'}
   env[kind=='scorcher'and 'ScorcherARRuntime'or 'ArsenalPreset01Runtime']=state
   return ext,state
  end
  local runtimes={}
  env.require=function(name)
   if name=='mods/codex/arsenal_preset01_runtime'or name=='mods/codex/scorcher_ar_runtime'then
    if not runtimes[name]then
     local ext,state=runtime_api(name:find('scorcher',1,true)and 'scorcher'or 'common')
     runtimes[name]={ext=ext,state=state}
    end
    return runtimes[name].ext
   end
   return require(name)
  end
  local expected_profiles=0
  for _,i in ipairs(order)do if bit.band(mask,2^(i-1))~=0 then
   local id=packets[i].id
   if profile_chunks[id]then execute(profile_chunks[id],env,'@shipped-profile-'..id);expected_profiles=expected_profiles+1 end
   if id=='punisher-plasma'then
    local shipped=execute(punisher_setup,env,'@shipped-punisher-definitions')
    local calls=0
    local api={now=function()return now end,identity=function(p)return p end,
     retain=function()end,epoch=function()return 'fixture'end,
     read=function(p,n)return string.rep('\0',n)end,pointer=function()return nil end}
    local function basic()
     local a=make_api();a.byte_pointer=function()return 0x10000000 end;return a
    end
    local function prepare()
     for _,name in ipairs({'ScorcherARRuntime','ArsenalPreset01Runtime'})do
      local peer=rawget(env,name)
      if peer and peer.phase~='ready'then error('Native data unavailable: waiting for '..name)end
     end
     return {snapshot={stock={}},protected={}}
    end
    local fixture={profile=function()return {}end,plan=function()return {epoch='fixture',guards={},rows={}}end,
     runtime={start=function()calls=calls+1;controller_calls=controller_calls+1;
      return {registry={slots={}},owned={shake_address=1,shake_bytes='x'}}end},
     registry={check=function()return true end},
     registration=function(_,plan)
      plan.rows={{role='child_rounds',address=2,after=string.rep('\0',4)}}
      return {installed=true,install=function()return true end}
     end}
    shipped.start(basic,function()return api end,prepare,shipped.D,fixture,{})
    adapters[#adapters+1]={id=id,meta={global_name='PunisherPlasmaFirstTest'},calls=function()return calls end}
   end
   if controllers[id]then
    local meta=metadata[id]
    local calls=0
    local patch={runtime={}}
    patch.apply=function(api)
     calls=calls+1;controller_calls=controller_calls+1
     if id=='tenderizer-armor-softener'then
      local gas=rawget(env,'SterilizerArmorControlV1')
      if gas then assert((gas.status==profile.gas_applied or gas.status==profile.gas_applied60 or gas.status==profile.gas_appliedenemy)and api.gas_required)else assert(not api.gas_required)end
     end
     if id=='plas-45-epoch'or id=='ac-8-autocannon'then return meta.status end
     return true,meta.status
    end
    patch.prepare=function()calls=calls+1;return {}end
    patch.synchronize=function()return true,'fixture native selection',0,0 end
    local e=setmetatable({patch=patch,apply=patch.apply,profile=profile},{__index=env})
    e._G=env
    -- Writes to update and named globals must target the shared fixture world.
    setmetatable(e,{__index=env,__newindex=function(_,k,v)env[k]=v end})
    local start=execute(controllers[id],e,'@shipped-startup-'..id)
    local super={prepare=function()return {}end,synchronize=function()return 'Ready: fixture'end}
    start(make_api,patch,super)
    adapters[#adapters+1]={id=id,meta=meta,calls=function()return calls end}
   end
  end end
  local filtration_selected=filtration_source~=''and expected['mods/codex/sterilizer_armor_control']
  local filtration_calls=0
  if filtration_selected then
   local m=execute(filtration_source,env,'@shipped-filtration-controller')
   m.start(make_api,function()filtration_calls=filtration_calls+1;filtration_startups=filtration_startups+1;return true,'Applied: filtration scheduling fixture'end)
  end
  local variable_selected=bit.band(mask,2^21)~=0
  local variable_gate=execute(variable_gate_source,env,'@shipped-variable-peer-gate')
  for frame=1,60 do
   now=now+5000
   local a,z=env.update('a','z');assert(a=='a','Base callback result lost')
   for _,entry in pairs(runtimes)do
    if now>=30000 and entry.ext.preset_peers_ready()then entry.state.phase='ready'end
   end
  end
  assert(base_calls==60,'Base update was not preserved')
  if filtration_selected then assert(env.GasFiltrationImmunityV1.active and filtration_calls==1,env.GasFiltrationImmunityV1.status)end
  local registered=0
  for _,entry in pairs(runtimes)do
   assert(entry.state.phase=='ready','Profile companion deadlock')
   for _ in pairs(entry.ext.profile_registry)do registered=registered+1 end
  end
  assert(registered==expected_profiles,'Selected profiles missing or extra')
  profiles=profiles+registered
  for _,adapter in ipairs(adapters)do
   local state=rawget(env,adapter.meta.global_name)
   if adapter.id=='punisher-plasma'then
    assert(state and state.source_installed and not state.stopped,state and state.status)
   elseif adapter.id=='plas-39-accelerator-rifle'then
    assert(state and state.status=='Native mode synchronized; left-side selector active',state and state.status)
   else assert(state and state.active,adapter.id..': '..tostring(state and state.status))end
   assert(adapter.calls()==1,adapter.id..' initialized more/less than once')
  end
  if variable_selected then assert(variable_gate(env)==nil,'Variable companion deadlock')end
  cases=cases+1
 end
end
assert(discoveries==#masks and cases==#masks*#orders)
local fault_cases=0
local peers={
 ['gas-overhaul']='FlagDamagePrototypeV1',
 ['r-40-k-hot-shot']='FlagDamagePrototypeV1',
 ['ac-8-autocannon']='FlagDamagePrototypeV1',
 ['ar-32-pacifier']='FlagDamagePrototypeV1',
 ['plas-45-epoch']='FlagDamagePrototypeV1',
 ['tenderizer-armor-softener']='SterilizerArmorControlV1',
}
for id,control in pairs(controllers)do
 if not incremental or id==focus_id then
 for _,mode in ipairs({'bad_exe','unknown_patch','failed_peer','late_peer'})do
  if (mode~='failed_peer'and mode~='late_peer')or peers[id]then
   local env=make_environment();local now,calls,base_calls=0,0,0
   local meta=metadata[id]
   local profile=execute(tenderizer_profile_source,env,'@shipped-tenderizer-profile')
   env.profile=profile
   env.update=function(a)base_calls=base_calls+1;return a end
   local peer=peers[id]
   if peer and(mode=='failed_peer'or mode=='late_peer')then
    env[peer]={active=false,status='Refused: fixture dependency'}
    if id=='tenderizer-armor-softener'then
     env.CowboyBingusModLoader={modules={['mods/codex/sterilizer_armor_control']='failed'}}
    end
   end
   local function make_api()
    return{now=function()return now end,module=function(name)return name and 'game'or 'exe'end,
     module_hash=function(name)
      if mode=='bad_exe'and name=='exe'then return 'unsupported'end
      return name=='game'and '2E2C3B7C2500646DADD5F2B4C6E0504DBB7E7896139F64CDDC0D1813C718F51E'
        or 'F5FEE03DCFDB2E553A4752C283590950AC13316B376D8196AA556FF0400D5F06'
     end}
   end
   local patch={runtime={}}
   patch.apply=function()
    calls=calls+1
    if mode=='unknown_patch'or mode=='bad_exe'then
     if id=='ac-8-autocannon'or id=='ar-32-pacifier'or id=='plas-45-epoch'then error('Unsupported fixture row')end
     return false,'Unsupported fixture row'
    end
    if id=='ac-8-autocannon'or id=='ar-32-pacifier'or id=='plas-45-epoch'then return meta.status end
    return true,meta.status
   end
   patch.prepare=function()calls=calls+1;error('Unsupported fixture row')end
   local e=setmetatable({patch=patch,apply=patch.apply,profile=profile,_G=env},
    {__index=env,__newindex=function(_,k,v)env[k]=v end})
   local start=execute(control,e,'@shipped-fault-controller-'..id)
   start(make_api,patch,{prepare=function()return {}end,synchronize=function()return 'Ready'end})
   for frame=1,80 do
    now=now+5000
    if mode=='late_peer'and now>=60000 then
     env[peer]={active=true,status=id=='tenderizer-armor-softener'and profile.gas_applied or 'Applied: fixture peer'}
    end
    assert(env.update('base')=='base')
   end
   local state=assert(rawget(env,meta.global_name))
   assert(base_calls==80)
   if mode=='late_peer'then assert(state.active and calls==1,id..':'..tostring(state.status))
   elseif mode=='failed_peer'then assert(not state.active and calls==0,id..':'..tostring(state.status))
   else assert(not state.active,id..' accepted unsupported source')end
   fault_cases=fault_cases+1
  end
 end
 end
end
local f=assert(io.open(report_path,'w'))
f:write('{"result":"PASS","loader_discovery_selections":',discoveries,
 ',"startup_control_cases":',cases,',"patch_adapter_calls":',controller_calls,
 ',"selected_profile_registrations":',profiles,',"additional_fault_cases":',fault_cases,
 ',"filtration_controller_cases":',filtration_startups,'}')
f:close()
'''
    (evidence / 'startup-matrix.lua').write_text(script, encoding='utf-8')
    runtime.run(script.encode(), '@configurable-startup-control-matrix.lua')
    report = json.loads((evidence / 'runtime-counts.json').read_text())
    report.update(compiled_source_matches=compiled_checks,
                  targeted_peer_ids=args.peer_ids,
                  focus_pairs=args.focus_pairs,selection_masks=masks,
                  changed_mod_pairs=(n-1 if args.focus_pairs else len(args.peer_ids)),
                  controllers=len(controllers), profile_entrypoints=len(profile_chunks),
                  orders=['forward','reverse']if args.incremental else ['forward','reverse','seed1107','seed2911'],
                  scope='Real loader discovery, shipped startup controllers, registration and peer gates; patch/native adapters are fixtures.',
                  live_startup='NOT RUN', loaded_resource='NOT RUN', gameplay='NOT RUN',
                  transaction_matrix=False, process_access=False)
    (evidence / 'runtime-matrix.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
