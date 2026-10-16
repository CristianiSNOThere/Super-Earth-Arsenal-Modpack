
local ffi=require('ffi')
local tests={};local function pass(s)tests[#tests+1]=s end
local function word(v)local b=ffi.new('uint32_t[1]',v);return ffi.string(b,4)end
local function float(v)local b=ffi.new('float[1]',v);return ffi.string(b,4)end
local function u32(s,o)local b=ffi.new('uint32_t[1]');ffi.copy(b,s:sub(o+1,o+4),4);return tonumber(b[0])end
local profile,plan,registration,observe,startup,modes=modules.profile,modules.plan,modules.registration,modules.observe,start,modules.modes
local stock={weapon=D.components.weapon.bytes,projectile=D.components.projectile.bytes,magazine=D.components.magazine.bytes}
local profiles=profile(D.source_rows,modes,stock,D.child_reload_template);local by={}
for _,r in ipairs(profiles)do by[r.role]=r end
assert(by.parent_projectile.after:sub(9,12)==float(60))
assert(by.parent_magazine.after:sub(137,152)==word(17)..word(1)..word(1)..word(1))
assert(by.child_rounds.after:sub(73,77)==float(20)..by.child_rounds.after:sub(77,77))
assert(by.child_rounds.after:sub(81,92)==word(60)..word(60)..word(60))
pass('current60RPM/17+17 normal and independent20+60 child source profiles')
local mem={};local function put(p,s)for i=1,#s do mem[p+i-1]=s:byte(i)end end
local function read(p,n)local out={};for i=0,n-1 do if not mem[p+i]then return nil end;out[#out+1]=string.char(mem[p+i])end;return table.concat(out)end
local function pointer(v,o)if not v then return nil end;local n=u32(v,o)+u32(v,o+4)*4294967296;return n>0 and n or nil end
local function ptrbytes(v)local a=ffi.new('uint64_t[1]',v);return ffi.string(a,8)end
local game,root=0x10000000,0x20000000
put(game+0x346bf98,ptrbytes(root));put(game+0x348456c,word(4294967295))
for _,rva in ipairs({0x348e2f8,0x348e1f8,0x348ec88})do put(game+rva,ptrbytes(0x90000000+rva))end
put(root+0xf32f18,string.rep('\0',2048*24));for i=0,2047 do put(root+0xf32f18+i*24+8,word(4294967295))end
local groups={};local buffers,sizes='', '';local address=0x30000000
for _,r in ipairs(profiles)do
 if not groups[r.offset]then
  local max=r.index;for _,x in ipairs(profiles)do if x.offset==r.offset then max=math.max(max,x.index)end end
  local size=r.count*16+(max+1)*r.stride;groups[r.offset]={p=address,size=size,slot=0};put(address,string.rep('\0',size));put(root+r.offset,ptrbytes(address))
  buffers=buffers..ptrbytes(address);sizes=sizes..word(size);address=address+0x100000
 end
 local g=groups[r.offset];put(g.p+g.slot*16,r.owner..word(r.index)..word(0));g.slot=g.slot+1
 put(g.p+r.count*16+r.index*r.stride,r.before)
end
local group_count=#buffers/8;put(root+0xf12470,word(group_count));put(root+0xf11c70,buffers);put(root+0xf12070,sizes);put(root+0xf12270,string.rep('\0',group_count*4))
for _,g in ipairs(D.code)do put(game+g.rva,g.bytes)end
for _,g in ipairs(D.attachment_code)do put(game+g.rva,g.bytes)end
local function api()return {read=read,pointer=pointer,identity=function(p)return p end,epoch=function()return 'fixture'end}end
local c={epoch='fixture',protected={},snapshot={stock=stock}}
local p=plan(api(),game,c,D,profiles);assert(#p.rows==8 and #p.busy==3);pass('source planner: loader ledger/sole owner/exact code/absence guards')
for _,rva in ipairs({0x348e2f8,0x348e1f8,0x348ec88})do
 local found=false;for _,guard in ipairs(p.guards)do if guard.address==game+rva then found=true end end
 assert(found,'Resource epoch anchor absent from native guards')
end
pass('all three resource epoch owners included in paused native guard set')
local function refuse(label,fn)
 local ok=pcall(fn);assert(not ok,label);pass(label)
end
for _,owner in ipairs({D.owner,D.child_owner,D.one_two_owner})do
 put(root+0xf32f18,owner..word(123)..string.rep('\0',12));refuse('planner refuses existing target '..u32(owner,0),function()plan(api(),game,c,D,profiles)end)
 put(root+0xf32f18,string.rep('\0',8)..word(4294967295)..string.rep('\0',12))
end
local g=groups[profiles[1].offset];put(g.p+2*16,ptrbytes(0xabc)..word(profiles[1].index)..word(0))
refuse('planner refuses shared source row',function()plan(api(),game,c,D,profiles)end);put(g.p+2*16,string.rep('\0',16))
local original=read(root+0xf12070,#sizes);put(root+0xf12070,string.rep('\0',#sizes))
refuse('planner refuses invalid ledger',function()plan(api(),game,c,D,profiles)end);put(root+0xf12070,original)
local target=g.p+profiles[1].count*16+profiles[1].index*profiles[1].stride;put(target,'X')
refuse('planner refuses source drift',function()plan(api(),game,c,D,profiles)end);put(target,profiles[1].before:sub(1,1))
local a=api();local p2=plan(a,game,c,D,profiles);assert(a.epoch()=='fixture');put(root+profiles[1].offset,ptrbytes(g.p+4));assert(a.epoch()=='changed');put(root+profiles[1].offset,ptrbytes(g.p));pass('source pointer epoch expiry')
-- Separate child source/runtime ammo observation; no inventory writes.
local manager,mainmap,privmap,refs,refaddr,selection,active,private_rows=0x60000000,0x60001000,0x60002000,0x60003000,0x60004000,0x60005000,0x60006000,0x60007000
put(game+0x3326cf0,ptrbytes(manager));put(manager,string.rep('\0',0xb0))
put(manager+0x14,word(1));put(manager+0x28,ptrbytes(mainmap)..word(8)..word(4294967295)..word(1))
put(manager+0x40,ptrbytes(refs));put(refs,ptrbytes(refaddr));put(manager+0x50,ptrbytes(active));put(manager+0x58,ptrbytes(selection))
put(manager+0x68,ptrbytes(privmap)..word(8)..word(4294967295)..word(1));put(manager+0xa0,word(1));put(manager+0xa8,ptrbytes(private_rows))
for i=0,7 do put(mainmap+i*8,word(4294967295)..word(4294967295));put(privmap+i*8,word(4294967295)..word(4294967295))end
put(mainmap+3*8,word(123)..word(0))
local entity=D.child_owner..word(123)..word(77)..word(32767)..word(1);put(refaddr,entity)
put(selection,word(60)..word(0)..word(20)..word(0)..word(1));put(active,word(1)..word(20)..word(0)..word(0)..word(0)..word(1))
local rounds_group=groups[by.child_rounds.offset];local rounds_address=rounds_group.p+50*16+13*136
put(rounds_address,by.child_rounds.after);put(private_rows,by.child_rounds.after)
local join=function()return {{parent_id=7,child_id=123,child_owner='02cd7321cd8445f5',child_record=entity}},function()end end
assert(#observe(api(),game,function()return {},function()end end,by.child_rounds.after)==0);pass('observer waits without reading Rounds when no Punisher child exists')
local observed=observe(api(),game,join,by.child_rounds.after);assert(#observed==1 and observed[1].loaded==20 and observed[1].spares==60 and observed[1].ready_flag==1)
pass('observer recognizes native20/60 with no-chamber readiness flag1 and local engine sentinel')
put(active+4,word(19));observed=observe(api(),game,join,by.child_rounds.after);assert(observed[1].loaded==19 and observed[1].saved_loaded==20)
pass('observer permits consumed runtime ammo distinct from saved reset state');put(active+4,word(20))
put(privmap+3*8,word(123)..word(0));assert(#observe(api(),game,join,by.child_rounds.after)==1);pass('observer validates actual private Rounds when present')
put(private_rows,'X');refuse('observer refuses private configuration drift',function()observe(api(),game,join,by.child_rounds.after)end);put(private_rows,by.child_rounds.after)
put(active+4,word(21));refuse('observer refuses excess native ammo',function()observe(api(),game,join,by.child_rounds.after)end);put(active+4,word(20))
put(refaddr+12,word(78));refuse('observer refuses factory generation mismatch',function()observe(api(),game,join,by.child_rounds.after)end);put(refaddr,entity)
refuse('observer refuses wrong attached owner',function()observe(api(),game,function()return {{child_owner='other'}},function()end end,by.child_rounds.after)end)
local changing=api();local calls=0;changing.read=function(p,n)calls=calls+1;if calls>8 and p==active then return nil end;return read(p,n)end
refuse('observer refuses unreadable state',function()observe(changing,game,join,by.child_rounds.after)end)
-- Actual extracted helper through ACTUAL Lua FFI adapter in this disposable
-- process. Seven retained source buffers, no callbacks under suspension.
local pins={};local nativeapi={epoch=function()return 'native-fixture'end,retain=function(v)pins[#pins+1]=v end,
 identity=function(p)return tonumber(ffi.cast('uintptr_t',p))end,read=function(p,n)return ffi.string(p,n)end}
local np={approved=true,epoch='native-fixture',rows={},guards={},busy={{0x11000000,0x11000001},{0x12000000,0x12000001},{0x13000000,0x13000001}}}
local nativeprofiles={unpack(profiles)}

for _,r in ipairs(nativeprofiles)do
 local buf=ffi.new('uint8_t[?]',#r.before);pins[#pins+1]=buf;ffi.copy(buf,r.before,#r.before)
 np.rows[#np.rows+1]={role=r.role,address=buf,before=r.before,after=r.after}
 for o=0,#r.before-1,4096 do np.guards[#np.guards+1]={address=buf+o,bytes=r.before:sub(o+1,o+4096)}end
end
local nr=registration(nativeapi,np,helper);assert(nr.install());assert(nr.installed and not nr.poisoned)
for _,r in ipairs(np.rows)do assert(ffi.string(r.address,#r.after)==r.after)end
collectgarbage('collect');for _,r in ipairs(np.rows)do assert(ffi.string(r.address,#r.after)==r.after)end
pass('actual Lua retained adapter executes extracted native source transaction; GC survival')
refuse('adapter refuses repeat installation',function()nr.install()end)
-- Real isolated readonly source page: check the exact shipped log decoder.
local k=ffi.load('kernel32')
local readonly=k.VirtualAlloc(nil,4096,0x3000,4);assert(readonly~=nil)
readonly=ffi.cast('uint8_t*',readonly);pins[#pins+1]=readonly
local first=np.rows[1];ffi.copy(readonly,first.before,#first.before)
first.address=readonly;np.guards={}
for _,r in ipairs(np.rows)do
 ffi.copy(r.address,r.before,#r.before)
 for o=0,#r.before-1,4096 do np.guards[#np.guards+1]={address=r.address+o,bytes=r.before:sub(o+1,o+4096)}end
end
local accepted=registration(nativeapi,np,helper)
local oldprotect=ffi.new('uint32_t[1]');assert(k.VirtualProtect(readonly,4096,2,oldprotect)~=0)
assert(accepted.install() and accepted.installed)
local info=ffi.new('uint8_t[48]');assert(k.VirtualQuery(readonly,info,48)==48)
assert(u32(ffi.string(info,48),36)==2,'Readonly source protection not restored')
for _,r in ipairs(np.rows)do assert(ffi.string(r.address,#r.after)==r.after)end
assert(k.VirtualProtect(readonly,4096,4,oldprotect)~=0)
for _,r in ipairs(np.rows)do ffi.copy(r.address,r.before,#r.before)end
pass('actual Lua adapter commits readonly source page and restores original protection')
local rejected=registration(nativeapi,np,helper)
assert(k.VirtualProtect(readonly,4096,0x20,oldprotect)~=0)
local ok,why=pcall(rejected.install)
assert(not ok and rejected.poisoned and not rejected.installed)
assert(tostring(why):find('reason=page protection',1,true),why)
assert(tostring(why):find('role=parent_weapon; offset=104',1,true),why)
assert(tostring(why):find('protection=32; type=131072; query_size=48',1,true),why)
assert(tostring(why):find('address=0x',1,true) and not tostring(why):find('deleted',1,true),why)
for _,r in ipairs(np.rows)do assert(ffi.string(r.address,#r.before)==r.before)end
assert(k.VirtualProtect(readonly,4096,4,oldprotect)~=0)
pass('actual Lua decoder rejects executable source page, formats exact scalar address and retains allocations')
-- Startup wiring fixtures exercise the shipped callback; mocked modules stay
-- exclusively in this offline verifier. No such backend enters the ZIP.
local now=0;local writes,installs,observations=0,0,0
local aa={epoch=function()return 'fixture'end,now=function()return now end,identity=function(p)return p end,retain=function()end,read=read,pointer=function()return 999999 end}
local basic={module=function(n)return n=='game.dll' and 2 or 1 end,module_hash=function(m)return m==1 and D.exe_hash or D.game_hash end,byte_pointer=function(p)return p end}
local mod={profile=profile,modes=modes,plan=function()return {rows={},guards={},epoch='fixture'}end,
 runtime={start=function()writes=writes+1;return {registry={slots={}},owned={shake_address=555,shake_bytes='x',shakes={}}}end},registry={check=function()return true end},
 registration=function(_,p)
  p.rows={{role='child_rounds',address=777,after=by.child_rounds.after}};put(777,by.child_rounds.after)
  return {installed=true,install=function()installs=installs+1;return true end}
 end,
 observe=function()observations=observations+1;return {{parent_id=1,child_id=2,loaded=20,spares=60}}end}
_G.PunisherPlasmaFirstTest=nil;update=function()return 'kept',nil,7 end
local state=startup(function()return basic end,function()return aa end,function()return c end,D,mod,helper)
for i=1,4 do now=now+300;local x,y,z=update();assert(x=='kept' and y==nil and z==7)end
assert(state.source_installed and state.native_20_60_observed and not state.gameplay_verified and writes==1 and installs==1 and observations>0)
assert(state.retained[1].api==aa and state.retained[2].run,'Missing global process retention')
pass('startup installs exactly once, preserves callback nil holes, reports ammo separately')
local old_observe,old_print=mod.observe,print;local change_index=0
print=function()end
mod.observe=function()change_index=change_index+1;return {{parent_id=1,child_id=2,loaded=20,spares=change_index%61}}end
for i=1,105 do now=now+300;update()end
print=old_print;mod.observe=old_observe
assert(#state.observations==100 and state.observations[100]:find('tick_ms='..now..'; ',1,true)==1)
assert(state.observations[100]:find('spares=44',1,true),'Recent ammo event lost')
assert(writes==1 and installs==1,'Observation history mutated installation')
pass('bounded latest100 timestamped observations retain late ammo events without reinstall')
_G.PunisherPlasmaFirstTest=nil;writes=0;installs=0;local old_registration=mod.registration
mod.registration=function()error('Fixture helper refusal after publication')end
state=startup(function()return basic end,function()return aa end,function()return c end,D,mod,helper);update();collectgarbage('collect')
assert(state.stopped and writes==1 and not state.source_installed and state.retained[1].api==aa and state.retained[2].run)
pass('post-publication refusal retains native allocation graph in global state after dead coroutine/GC');mod.registration=old_registration
-- Failed absence plan precedes owned publication and never installs.
_G.PunisherPlasmaFirstTest=nil;writes=0;installs=0;mod.plan=function()error('Target weapon already exists')end
state=startup(function()return basic end,function()return aa end,function()return c end,D,mod,helper);update()
assert(state.stopped and not state.source_installed and writes==0 and installs==0);pass('already-created target stops before tuning publication/source installation')

local f=assert(io.open(REPORT_PATH,'wb'));f:write(table.concat(tests,'\n'));f:close();print('CURRENT_SOURCE_CASES',#tests)
