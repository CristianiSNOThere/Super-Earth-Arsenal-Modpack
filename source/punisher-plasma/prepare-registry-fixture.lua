-- Appended to the shipped runtime definitions with their final start call removed.
-- All addresses below belong to synthetic maps or retained fixture allocations.
local ffi=require('ffi')
local cases={}
local function pass(s)cases[#cases+1]=s end
local function word(v)local a=ffi.new('uint32_t[1]',v);return ffi.string(a,4)end
local function ptrbytes(v)local a=ffi.new('uint64_t[1]',v);return ffi.string(a,8)end
local function u32(s,o)local a=ffi.new('uint32_t[1]');ffi.copy(a,s:sub(o+1,o+4),4);return tonumber(a[0])end
local function fixture(modified)
 local mem,pins,ranges={},{},{}
 local function put(p,s)for i=1,#s do mem[p+i-1]=s:byte(i)end end
 local function id(p)return type(p)=='number' and p or tonumber(ffi.cast('uintptr_t',p))end
 local function read(p,n)
  local a=id(p)
  for _,r in ipairs(ranges)do if a>=r[1] and a+n<=r[2]then return ffi.string(ffi.cast('uint8_t*',p),n)end end
  local out={};for i=0,n-1 do if not mem[a+i]then return nil end;out[#out+1]=string.char(mem[a+i])end
  return table.concat(out)
 end
 local function pointer(s,o)
  if not s or #s<o+8 then return nil end
  local a=ffi.new('uint64_t[1]');ffi.copy(a,s:sub(o+1,o+8),8)
  local n=tonumber(a[0]);return n>=65536 and n<2^47 and n or nil
 end
 local game,owner=0x10000000,0x20000000
 put(game+0x346bf98,ptrbytes(owner))
 for _,rva in ipairs({0x348e2f8,0x348e1f8,0x348ec88})do put(game+rva,ptrbytes(0x25000000+rva))end
 local map=0x30000000;local components={}
 for name,g in pairs(D.components)do
  put(owner+g.offset,ptrbytes(map));put(map,string.rep('\0',g.count*16))
  put(map+(g.count-1)*16,D.owner..word(g.index)..word(0))
  local address=map+g.count*16+g.index*g.stride;put(address,g.bytes)
  components[name]=address;map=map+0x100000
 end
 for _,g in ipairs(D.code)do put(game+g.rva,g.bytes)end
 local at=0x60000000;local records={}
 for name,g in pairs(D.records)do
  local bytes=modified and g.accepted[#g.accepted] or g.serialized
  if g.kind=='explosion'then
   put(at+1024,g.array);bytes=bytes:sub(1,40)..ptrbytes(at+1024)..bytes:sub(49)
  end
  put(at,bytes);put(game+g.registry+g.id*8,ptrbytes(at));records[name]=at;at=at+0x10000
 end
 local api={read=read,pointer=pointer,identity=id,data_access=function()return true end,
  pointer_bytes=function(p)return ptrbytes(id(p))end,now=function()return 0 end}
 api.retain=function(v)
  pins[#pins+1]=v
  if v.records then
   for k,bytes in pairs(v.records)do local a=id(v.addresses[k]);ranges[#ranges+1]={a,a+#bytes}end
   local a=id(v.shake_address);ranges[#ranges+1]={a,a+#v.shake_bytes}
   for _,g in ipairs(v.shakes or {})do local p=id(g.address);ranges[#ranges+1]={p,p+#g.bytes}end
  end
 end
 local allowed={damage={[305]=true,[311]=true},projectile={[171]=true,[57]=true},explosion={[355]=true,[290]=true,[377]=true}}
 local offsets={damage=0x37c60c0,projectile=0x37c7670,explosion=0x37cc920}
 api.slot_allowed=function(kind,n,p)return allowed[kind] and allowed[kind][n] and id(p)==game+offsets[kind]+n*8 end
 local writes=0
 api.write_slot=function(kind,n,p,s)
  assert(api.slot_allowed(kind,n,p));writes=writes+1
  if writes==api.fail_at then
   if api.foreign_change then api.foreign_change(put)end
   return false
  end
  put(id(p),s);return true
 end
 return api,game,put,read,records,components,function()return writes end
end
local function reset()_G.ScorcherARRuntime=nil;_G.ArsenalPreset01Runtime=nil end
for _,modified in ipairs({false,true})do
 reset();if modified then _G.ScorcherARRuntime={phase='ready'}end
 local a,g,put,read,records,components,w=fixture(modified)
 local c=prepare(a,g,D);c.magazine_tuning=false
 local originals={};for name,r in pairs(D.records)do originals[name]=read(g+r.registry+r.id*8,8)end
 local s=assert(modules.runtime.start(a,c,modules));assert(s.active and w()==7)
 assert(u32(s.owned.records.normal_damage,4)==350 and u32(s.owned.records.normal_damage,8)==225)
 assert(u32(s.owned.records.damage,4)==25 and u32(s.owned.records.damage,8)==9)
 for _,off in ipairs({12,16,20,24})do assert(u32(s.owned.records.damage,off)==3)end
 for _,p in ipairs(c.protected)do assert(read(p.address,#p.bytes)==p.bytes)end
 assert(modules.registry.check(a,s.registry));collectgarbage('collect');assert(modules.registry.check(a,s.registry))
 pass(modified and 'Scorcher-first supported values; seven owned registry writes; protected peers unchanged' or 'stock/absent companions; seven owned registry writes; protected peers unchanged')
end
for fail=1,7 do
 reset();local a,g,put,read,records,components,w=fixture(false);local c=prepare(a,g,D);c.magazine_tuning=false;a.fail_at=fail
 local before={};for _,r in pairs(D.records)do before[g+r.registry+r.id*8]=read(g+r.registry+r.id*8,8)end
 local s,why,state=modules.runtime.start(a,c,modules);assert(not s and why and state and not state.poisoned)
 for p,s in pairs(before)do assert(read(p,8)==s,'Incomplete registry rollback')end
 pass('registry partial transaction rollback at write '..fail)
end
do
 reset();local a,g,put,read,records,components,w=fixture(false);local c=prepare(a,g,D);c.magazine_tuning=false
 local slot=c.originals.damage.slot;local foreign=ptrbytes(0x6ffff000);put(slot,foreign)
 assert(not pcall(modules.runtime.start,a,c,modules) and w()==0 and read(slot,8)==foreign)
 pass('redirected active registry refuses before publication; foreign pointer preserved')
end
do
 reset();local a,g,put,read,records,components,w=fixture(false);local c=prepare(a,g,D);c.magazine_tuning=false
 local first=g+0x37cc920+377*8;local foreign=ptrbytes(0x6ffff000)
 a.fail_at=4;a.foreign_change=function(p)p(first,foreign)end
 local s,why,state=modules.runtime.start(a,c,modules)
 assert(not s and state.poisoned and read(first,8)==foreign)
 pass('foreign edit during failed publication preserved; transaction marked poisoned')
end
for _,name in ipairs({'ScorcherARRuntime','ArsenalPreset01Runtime'})do
 for _,phase in ipairs({'preparing','gave_up','ready'})do
  reset();local a,g,put,read,records,components,w=fixture(false);_G[name]={phase=phase}
  local c=prepare(a,g,D);assert(w()==0);c.magazine_tuning=false
  assert(modules.runtime.start(a,c,modules) and w()==7)
  pass('exact source validation independent of optional '..name..' phase '..phase)
 end
end
for _,what in ipairs({'source','registry_record','explosion_array'})do
 reset();local a,g,put,read,records,components,w=fixture(false)
 if what=='source'then put(components.weapon,'X')
 elseif what=='registry_record'then put(records.donor_damage,'X')
 else put(records.donor_explosion+1024,'X')end
 assert(not pcall(prepare,a,g,D) and w()==0)
 pass('unknown '..what..' refused before writes')
end
reset()
-- Actual startup + prepare + seven-slot transaction, with only source-plan and
-- native-install adapters replaced by synthetic fixture-owned source storage.
local function startup_fixture(peer_phase,modified)
 reset();local a,g,put,read,records,components,w=fixture(modified)
 local now,installs=0,0;a.now=function()return now end
 local basic={module=function(n)return n and 2 or 1 end,module_hash=function(m)return m==1 and D.exe_hash or D.game_hash end,byte_pointer=function()return g end}
 local m={};for name,value in pairs(modules)do m[name]=value end
 m.plan=function(api,game,c,dd,profiles)
  local rows={};for i,r in ipairs(profiles)do
   local p=r.role=='parent_magazine' and components.magazine or 0x70000000+i*0x10000;put(p,r.before)
   rows[#rows+1]={role=r.role,address=p,before=r.before,after=r.after}
  end
  return {rows=rows,guards={},epoch=c.epoch}
 end
 m.registration=function(api,plan)
  return {installed=true,install=function()
   installs=installs+1;for _,r in ipairs(plan.rows)do assert(read(r.address,#r.before)==r.before);put(r.address,r.after)end
   return true
  end}
 end
 m.observe=function()return {}end
 _G.ScorcherARRuntime=peer_phase and {phase=peer_phase} or nil
 _G.ArsenalPreset01Runtime=peer_phase and {phase=peer_phase} or nil
 _G.PunisherPlasmaFirstTest=nil;update=function()return 'base',nil,7 end
 local state=start(function()return basic end,function()return a end,prepare,D,m,helper)
 local function tick(ms)now=ms;local x,y,z=update();assert(x=='base' and y==nil and z==7)end
 return state,tick,a,g,put,read,records,w,function()return installs end
end
for _,order in ipairs({'absent','Scorcher-first','Punisher-first'})do
 local state,tick,a,g,put,read,records,w,installs=startup_fixture(order~='absent' and (order=='Scorcher-first' and 'ready' or 'preparing') or nil,order=='Scorcher-first')
 tick(0);tick(7000)
 assert(state.source_installed and w()==7 and installs()==1,'Source missed pre-ship deadline')
 if order=='Punisher-first'then
  assert(not state.stopped and state.status:find('waiting for ScorcherARRuntime',1,true))
  for _,name in ipairs({'scorcher_direct','scorcher_blast','scorcher_explosion'})do
   local d=D.records[name];local bytes=d.accepted[#d.accepted]
   if d.kind=='explosion'then bytes=bytes:sub(1,40)..read(records[name]+40,8)..bytes:sub(49)end
   put(records[name],bytes)
  end
  _G.ScorcherARRuntime.phase='ready';_G.ArsenalPreset01Runtime.phase='ready';tick(30000)
 end
 assert(not state.stopped and w()==7 and installs()==1)
 pass(order..': source installed before 7s; late 30s peers cannot delay equipment profiles; no reinstall')
end
for _,name in ipairs({'ScorcherARRuntime','ArsenalPreset01Runtime'})do
 for _,failure in ipairs({'gave_up','timeout'})do
  local state,tick,a,g,put,read,records,w,installs=startup_fixture('preparing',false)
  tick(0);assert(state.source_installed and w()==7 and installs()==1)
  local other=name=='ScorcherARRuntime' and 'ArsenalPreset01Runtime' or 'ScorcherARRuntime';_G[other].phase='ready'
  if failure=='gave_up'then _G[name].phase='gave_up' end
  for i=1,242 do tick(i*1001)end
  assert(state.stopped and state.source_installed and state.status:find(name,1,true) and w()==7 and installs()==1)
  pass('post-install '..failure..' named '..name..'; source retained; no repeated writes; base callback preserved')
 end
end
for _,mutation in ipairs({'unknown_peer_record','foreign_registry','source_drift','epoch_drift'})do
 local state,tick,a,g,put,read,records,w,installs=startup_fixture('preparing',false)
 tick(0);assert(state.source_installed)
 local changed,before
 if mutation=='unknown_peer_record'then changed=records.scorcher_direct;put(changed,'X')
 elseif mutation=='foreign_registry'then changed=g+0x37c60c0+305*8;put(changed,ptrbytes(0x6ffff000))
 elseif mutation=='source_drift'then changed=0x70010000;put(changed,'X')
 else changed=g+0x346bf98;put(changed,ptrbytes(0x6ffff000))end
 before=read(changed,(mutation=='foreign_registry' or mutation=='epoch_drift') and 8 or 1)
 _G.ScorcherARRuntime.phase='ready';_G.ArsenalPreset01Runtime.phase='ready';tick(30000)
 assert(state.stopped and state.source_installed and w()==7 and installs()==1 and read(changed,#before)==before)
 pass('post-install '..mutation..' refused; foreign edit preserved; no reinstall')
end
reset()
local f=assert(io.open(REPORT_PATH,'wb'));f:write(table.concat(cases,'\n'));f:close()
print('PUNISHER_PREPARE_REGISTRY_CASES',#cases)
