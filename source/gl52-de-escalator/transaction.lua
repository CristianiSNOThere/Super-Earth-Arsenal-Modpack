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

    if not map then fail('Expected one supported GL52 entity table; found 0')end

    local entities=map-26151684

    local plans={}

    for _,spec in ipairs(profile.components)do

        local group=entities+spec.group

        local owners=api.read(group+28,spec.count*16)

        assert(api.read(group,28)==unhex(spec.header) and owners,'GL52 '..spec.label..' group mismatch')

        local hits,aliases=0,0

        for i=0,spec.count-1 do

            local entry=owners:sub(i*16+1,i*16+16)

            if entry:sub(1,8)==unhex(spec.owner)then

                assert(u32(entry,8)==spec.index and u32(entry,12)==0,'GL52 owner index changed');hits=hits+1

            end

            if entry:sub(1,8)~=string.rep('\0',8) and u32(entry,8)==spec.index then aliases=aliases+1 end

        end

        assert(hits==1 and aliases==1,'GL52 component owner is not unique')

        local row=group+28+spec.count*16+spec.index*spec.stride

        local source=api.read(row,spec.stride)

        assert(api.data_access(row,spec.stride) and source and api.sha256(source)==spec.sha,

            'GL52 '..spec.label..' row mismatch or unsupported permissions')

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

            assert(api.read(game+pin.rva,#pin.bytes/2)==unhex(pin.bytes),'Unsupported GL52 native data consumer')

        end

        -- Read-only semantic guard: old SDK enums use different numeric values.

        local status_slot=game+profile.status_slot

        local status_row=api.pointer(api.read(status_slot,8),0)

        if not status_row then fail('Expected one supported GL52 Stun Large row; found 0')end

        local status=api.read(status_row,44)

        local name=status and api.pointer(status,8)

        assert(status and u32(status,0)==39 and status:sub(41,44)==unhex('0000a040')

          and name and api.read(name,11)=='Stun Large\0','GL52 Stun Large definition mismatch')

        local function status_intact()

            return api.read(status_slot,8)==api.pointer_bytes(status_row)

              and api.read(status_row,44)==status and api.read(name,11)=='Stun Large\0'

        end

        local plans=discover(api,game)

        local registries={}

        for _,spec in ipairs(profile.registries)do

            local slot=game+spec.slot

            local row=api.pointer(api.read(slot,8),0)

            if not row then fail('Expected one supported GL52 '..spec.label..' row; found 0')end

            local source=api.read(row,spec.size)

            assert(source and api.sha256(source)==spec.sha and u32(source,0)==spec.id,'GL52 '..spec.label..' source mismatch')

            assert(api.registry_access(game,slot),'GL52 '..spec.label..' registry is not writable data')

            local after=replace(source,spec.offset,unhex(spec.bytes))

            local owned=api.owned_copy(after)

            assert(api.read(owned,spec.size)==after,'GL52 owned row initialization failed')

            registries[#registries+1]={slot=slot,row=row,source=source,size=spec.size,owned=owned,after=after}

        end

        local function sources_intact()

            if not status_intact()then return false end

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

                assert(p.proof() and api.read(p.row,p.size)==expected,'GL52 ownership changed during edit')

                for _,edit in ipairs(p.edits)do

                    local bytes=unhex(edit.bytes)

                    attempted[#attempted+1]={row=p.row,size=p.size,source=expected,offset=edit.offset,bytes=bytes,proof=p.proof}

                    assert(api.write_attachment(p.row+edit.offset,bytes),'GL52 data write incomplete')

                    expected=replace(expected,edit.offset,bytes)

                    assert(api.read(p.row,p.size)==expected,'GL52 component verification failed')

                end

                p.expected=expected

            end

            for _,p in ipairs(registries)do

                assert(api.read(p.row,p.size)==p.source and api.read(p.owned,p.size)==p.after,'GL52 registry source changed')

                published[#published+1]=p

                assert(api.publish(game,p.slot,p.row,p.owned),'GL52 registry publication failed')

            end

            assert(status_intact(),'GL52 Stun Large changed during edit')

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

        return "Applied: GL-52 handling 35; reserve/start/resupply 70; reload speed 1.15x; arc 100/100 AP4/4/4/0; Stun Large strength 1.75; six loaded rounds, 200 RPM and 10 m arc reach retained."

    end)

    return ok,tostring(result)

end

return patch

