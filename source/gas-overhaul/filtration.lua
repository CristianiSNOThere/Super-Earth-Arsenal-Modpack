local P={[ [====[id]====] ]=13,[ [====[count]====] ]=32,[ [====[manager]====] ]=53634296,[ [====[object]====] ]=[====[0d000000b4ecef7c4e99358bef711250000000000000000001000000000000000000000000000000000000000000000000000000]====],[ [====[modifier]====] ]=[====[e5cc996e02000000cdcc4c3eed24ca9b]====],[ [====[reader_rva]====] ]=8889392,[ [====[reader_code]====] ]=[====[48895c2408574883ec20f30f10152ec9b401498bf90f28c28bda4183e80174244183e80174174183e801745f4183f8020f8598000000bae5cc996eeb0cbac439df4beb05ba7192f24d41b8030000008bcbe86af99500488bc84885c0742d8b500485d27507f30f104008eb1f8d42ffa9fdffffff740c83fa027510f30f104108eb09f30f104108f30f58c2ba9600a5b541b8030000008bcbe823f99500488bc84885c074298b500485d27507f30f104008eb1b8d42ffa9fdffffff740c83fa02750cf30f594108eb05f30f5841088b44245083f8057565ba6994a525448d40fe8bcbe8d9f89500488bc84885c0740c8b500485d27529f30f1040080f57c90f2ec17a02740bf30f5907f30f5fc20f28c8f30f110f488b5c24304883c4205fc38d42ffa9fdffffff740c83fa0275cdf30f594108ebc6f30f584108ebbf83f80275baf30f5907488b5c2430f30f11074883c4205fc3]====],[ [====[gas_applied]====] ]=[====[Applied: Gas Overhaul gas 60/60; Sterilizer contact 2/2; Helldiver incoming Gas multiplier 0.55; magazine 175; gas/confusion buildup 0.75; Acid Storm removed from shared gas hits; enemy-only host observer; duration 15 seconds.]====],[ [====[exe_sha]====] ]=[====[F5FEE03DCFDB2E553A4752C283590950AC13316B376D8196AA556FF0400D5F06]====],[ [====[dll_sha]====] ]=[====[2E2C3B7C2500646DADD5F2B4C6E0504DBB7E7896139F64CDDC0D1813C718F51E]====]}
local M={}
local function u32(s,o)
    if not s or #s<o+4 then return nil end
    local a,b,c,d=s:byte(o+1,o+4);return a+b*256+c*65536+d*16777216
end
local function unhex(s)return(s:gsub('..',function(h)return string.char(tonumber(h,16))end))end
local function replace(s,o,b)return s:sub(1,o)..b..s:sub(o+#b+1)end
function M.apply(api,module)
    local applied=false;local before;local desired;local row;local proof;local attempted=false
    local ok,result=pcall(function()
        local base=api.byte_pointer(module)
        assert(base~=nil,'Game module unavailable')
        assert(api.read(base+P.reader_rva,#P.reader_code/2)==unhex(P.reader_code),'Native gas resistance reader changed')
        local function ptr(p)return api.pointer(api.read(p,8),0)end
        local manager=ptr(base+P.manager)
        if not manager then return 'Waiting for customization manager' end
        local head=api.read(manager+32,16)
        if not head or u32(head,8)==0 then return 'Waiting for passive table' end
        assert(u32(head,8)==P.count and u32(head,12)==0,'Unknown passive table count/layout')
        local table_address=api.pointer(head,0)
        if not table_address then return 'Waiting for passive pointers' end
        local pointers=assert(api.read(table_address,P.count*8),'Passive table unreadable')
        local map=assert(api.read(manager+48+P.id*4,4),'Advanced Filtration index unreadable')
        local index=u32(map,0);assert(index<P.count,'Advanced Filtration index unsupported')
        local object=assert(api.pointer(pointers,index*8),'Advanced Filtration object missing')
        local raw=assert(api.read(object,52),'Advanced Filtration object unreadable')
        local normalized=replace(replace(raw,16,string.rep('\0',8)),32,string.rep('\0',8))
        assert(normalized==unhex(P.object),'Advanced Filtration object changed')
        row=assert(api.pointer(raw,16),'Advanced Filtration modifier list missing')
        assert(api.data_access(row,16),'Advanced Filtration modifier permissions unsupported')
        before=assert(api.read(row,16),'Advanced Filtration modifier unreadable')
        local stock=unhex(P.modifier);desired=replace(stock,8,string.rep('\0',4))
        assert(before==stock or before==desired,'Advanced Filtration gas modifier changed')
        -- Prove the modifier range is not shared with another passive object.
        local ownership={};local seen={};local ids={}
        for i=0,P.count-1 do
            local other=assert(api.pointer(pointers,i*8),'Passive object pointer missing')
            local identity=api.identity(other);assert(not seen[identity],'Passive object alias collision');seen[identity]=true
            local data=assert(api.read(other,52),'Passive owner metadata unreadable')
            local id=u32(data,0);assert(id<42 and not ids[id],'Passive owner identity collision');ids[id]=true
            local count=u32(data,24);assert(count and count<=16 and u32(data,28)==0,'Passive modifier count unsupported')
            if i~=index and count>0 then
                local address=assert(api.pointer(data,16),'Other passive modifiers unavailable')
                local delta=api.distance(address,row)
                assert(delta>=16 or delta+count*16<=0,'Advanced Filtration modifier overlaps another passive')
            end
            ownership[#ownership+1]={address=other,raw=data}
        end
        proof=function()
            if ptr(base+P.manager)~=manager or api.read(manager+32,16)~=head
              or api.read(manager+48+P.id*4,4)~=map or api.read(table_address,P.count*8)~=pointers then return false end
            for _,owner in ipairs(ownership)do if api.read(owner.address,52)~=owner.raw then return false end end
            return api.read(base+P.reader_rva,#P.reader_code/2)==unhex(P.reader_code)
        end
        assert(proof() and api.read(row,16)==before,'Passive ownership changed before edit')
        if before~=desired then
            attempted=true
            assert(api.write_protected(row+8,string.rep('\0',4)),'Advanced Filtration write incomplete')
            assert(proof() and api.read(row,16)==desired,'Advanced Filtration full modifier verification failed')
        end
        applied=true
        return 'Applied: Advanced Filtration gas multiplier 0.2 -> 0; gas damage and gas status immunity; other passives unchanged.'
    end)
    if ok then return applied,result end
    local restored=true
    if attempted then
        local current=api.read(row,16)
        local owned=current and #current==16 and proof()and current:sub(1,8)==before:sub(1,8)and current:sub(13)==before:sub(13)
        if owned then
            for i=9,12 do if current:byte(i)~=before:byte(i)and current:byte(i)~=desired:byte(i)then owned=false end end
        end
        if owned then
            local rollback_ok,value=pcall(api.write_protected,row+8,before:sub(9,12))
            restored=rollback_ok and value and api.read(row,16)==before
        else restored=false end
    end
    return false,tostring(result)..'; restored='..tostring(restored)..'. No further edit applied.'
end
function M.start(make_api,apply)
    if rawget(_G,'GasFiltrationImmunityV1')then return end
    local state={active=false,status='Waiting for Gas Overhaul',version='1',multiplier=nil}
    _G.GasFiltrationImmunityV1=state
    local api=make_api();local previous=update;local callback;local started=api.now();local next_try=0;local done=false;local checked=false
    local function log()
        pcall(function()
            local loader=rawget(_G,'CowboyBingusModLoader');local file=loader and loader.open_log and loader.open_log('GasFiltrationImmunity.log')
            if file then file:write('Advanced Filtration gas immunity test1\nstatus='..state.status..'\nmultiplier='..tostring(state.multiplier)..'\n');file:close()end
        end)
    end
    local function step()
        if done then return end
        local now=api.now();if now<next_try then return end;next_try=now+250
        local ok,reason=pcall(function()
            local gas=rawget(_G,'SterilizerArmorControlV1')
            assert(now-started<120000,'Installed companion or passive data did not become ready within120s: '..state.status)
            if not gas or not gas.active then state.status='Waiting for Gas Overhaul';return end
            assert(gas.status==P.gas_applied,'Unsupported Gas Overhaul Applied state')
            local module=api.module('game.dll')
            if not checked then
                assert(api.module_hash(module)==P.dll_sha and api.module_hash(api.module(nil))==P.exe_sha,'Unsupported game build')
                checked=true
            end
            local applied,status=apply(api,module)
            if applied then state.active=true;state.multiplier=0;state.status=status;done=true
            elseif status:sub(1,8)=='Waiting 'then state.status=status
            else error(status,0)end
        end)
        if not ok then state.status='Refused: '..tostring(reason);done=true end
        if done then log();if update==callback then update=previous or function()end end end
    end
    local function finish(...)step();return ... end
    callback=function(...)if previous then return finish(previous(...))end;step()end
    update=callback;log()
end
return M
