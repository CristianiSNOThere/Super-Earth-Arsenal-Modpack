local ffi=require('ffi')
local patch={}
local function unhex(s)return(s:gsub('..',function(h)return string.char(tonumber(h,16))end))end
local function u32(s,o)
    if not s or #s<o+4 then return nil end
    local a,b,c,d=s:byte(o+1,o+4);return a+b*256+c*65536+d*16777216
end
local function replace(s,o,b)return s:sub(1,o)..b..s:sub(o+#b+1)end
local function fail(s)error(s..'. No edit applied.',0)end
local function discover(api,game)
    local owner=api.pointer(api.read(game+0x346bf98,8),0)
    local map=owner and api.pointer(api.read(owner+0xf12bd8,8),0)
    if not map then fail('Expected one supported Adjudicator entity table; found 0')end
    local entities=map-26151684
    local plans={}
    for _,spec in ipairs(profile.components)do
        local group=entities+spec.group
        local owners=api.read(group+28,spec.count*16)
        assert(api.read(group,28)==unhex(spec.header) and owners,'Adjudicator '..spec.label..' group mismatch')
        local hits,aliases=0,0
        for i=0,spec.count-1 do
            local entry=owners:sub(i*16+1,i*16+16)
            if entry:sub(1,8)==unhex(spec.owner)then
                assert(u32(entry,8)==spec.index and u32(entry,12)==0,'Adjudicator owner index changed');hits=hits+1
            end
            if entry:sub(1,8)~=string.rep('\0',8) and u32(entry,8)==spec.index then aliases=aliases+1 end
        end
        assert(hits==1 and aliases==1,'Adjudicator component owner is not unique')
        local row=group+28+spec.count*16+spec.index*spec.stride
        local source=api.read(row,spec.stride)
        assert(api.data_access(row,spec.stride) and source and api.sha256(source)==spec.sha,
            'Adjudicator '..spec.label..' row mismatch or unsupported permissions')
        local function proof()
            local current_owner=api.pointer(api.read(game+0x346bf98,8),0)
            local current_map=current_owner and api.pointer(api.read(current_owner+0xf12bd8,8),0)
            return current_owner and current_map and api.distance(current_owner,owner)==0 and api.distance(current_map,map)==0
              and api.read(group,28)==unhex(spec.header) and api.read(group+28,spec.count*16)==owners
        end
        plans[#plans+1]={row=row,size=spec.stride,source=source,edits=spec.edits,proof=proof,label=spec.label}
    end
    return plans
end
function patch.apply(api,module)
    local ok,result=pcall(function()
        local game=ffi.cast('uint8_t *',module)
        for _,pin in ipairs(profile.pins)do
            assert(api.read(game+pin.rva,#pin.bytes/2)==unhex(pin.bytes),'Unsupported Adjudicator native data consumer')
        end
        local plans=discover(api,game)
        local registries={}
        for _,spec in ipairs(profile.registries)do
            local slot=game+spec.slot
            local row=api.pointer(api.read(slot,8),0)
            if not row then fail('Expected one supported Adjudicator '..spec.label..' row; found 0')end
            local source=api.read(row,spec.size)
            assert(source and api.sha256(source)==spec.sha and u32(source,0)==spec.id,'Adjudicator '..spec.label..' source mismatch')
            assert(api.registry_access(game,slot),'Adjudicator '..spec.label..' registry is not writable data')
            local after=replace(source,spec.offset,unhex(spec.bytes))
            local owned=api.owned_copy(after)
            assert(api.read(owned,spec.size)==after,'Adjudicator owned row initialization failed')
            registries[#registries+1]={slot=slot,row=row,source=source,size=spec.size,owned=owned,after=after}
        end
        local function sources_intact()
            for _,p in ipairs(plans)do
                if api.read(p.row,p.size)~=p.source or not p.proof()then return false end
            end
            for _,p in ipairs(registries)do
                if api.read(p.slot,8)~=api.pointer_bytes(p.row) or api.read(p.row,p.size)~=p.source then return false end
            end
            return true
        end
        assert(sources_intact(),'Data changed before edit. No edit applied.')
        local attempted,published={},{}
        local applied,reason=pcall(function()
            for _,p in ipairs(plans)do
                local expected=p.source
                assert(p.proof() and api.read(p.row,p.size)==expected,'Adjudicator ownership changed during edit')
                for _,edit in ipairs(p.edits)do
                    local bytes=unhex(edit.bytes)
                    attempted[#attempted+1]={row=p.row,size=p.size,source=expected,offset=edit.offset,bytes=bytes,proof=p.proof}
                    assert(api.write_attachment(p.row+edit.offset,bytes),'Adjudicator data write incomplete')
                    expected=replace(expected,edit.offset,bytes)
                    assert(api.read(p.row,p.size)==expected,'Adjudicator component verification failed')
                end
                p.expected=expected
            end
            for _,p in ipairs(registries)do
                assert(api.read(p.row,p.size)==p.source and api.read(p.owned,p.size)==p.after,'Adjudicator registry source changed')
                published[#published+1]=p
                assert(api.publish(game,p.slot,p.row,p.owned),'Adjudicator registry publication failed')
            end
            for _,p in ipairs(plans)do assert(p.proof() and api.read(p.row,p.size)==p.expected,'Full table verification failed')end
            for _,p in ipairs(registries)do
                assert(api.read(p.slot,8)==api.pointer_bytes(p.owned) and api.read(p.owned,p.size)==p.after
                  and api.read(p.row,p.size)==p.source,'Full registry verification failed')
            end
        end)
        if not applied then
            local restored=true
            for i=#published,1,-1 do
                local p=published[i]
                local current=api.read(p.slot,8)
                if current==api.pointer_bytes(p.owned)then
                    restored=api.publish(game,p.slot,p.owned,p.row)and restored
                elseif current~=api.pointer_bytes(p.row)then restored=false end
            end
            for i=#attempted,1,-1 do
                local p=attempted[i]
                local before=p.source:sub(p.offset+1,p.offset+#p.bytes)
                local current=api.read(p.row,p.size)
                local owned=p.proof() and current and replace(current,p.offset,before)==p.source
                if owned then
                    for j=1,#p.bytes do
                        local b=current:byte(p.offset+j)
                        if b~=before:byte(j)and b~=p.bytes:byte(j)then owned=false;break end
                    end
                end
                if owned then restored=api.write_attachment(p.row+p.offset,before)and api.read(p.row,p.size)==p.source and restored
                else restored=false end
            end
            error(tostring(reason)..'; restored='..tostring(restored),0)
        end
        return "Applied: BR-14 Adjudicator 115/30 damage, stagger 25, push 10, 48-round magazine, recoil horizontal 16.5 / vertical 57.5, sway 0.6, 1000 m/s, penetration speed loss 15%; 480 RPM; stock AP, spread, spare magazines and drag retained."
    end)
    return ok,tostring(result)
end
return patch
