-- Embedded in the shared runtime after its fields/defaults declarations.
-- Only the Meltagun's beam 18 and damage 509 receive these exceptions.
EXT.meltagun_sources = {
    {kind=T_BEAM,owner='18',size=112,
     hex='120000000000000000007041fd01000000007041000020410000803f9a99193f0000803f0000803f0000803e0d010000385e71d394489be900000000000000000000000000000000000000000000000000000000b71b299108000000000080bf00000000010000000500000000000000',
     members={8}},
    {kind=T_DAMAGE,owner='509',size=76,
     hex='fd010000280a0000280a0000070000000700000007000000070000001e0000002800000028000000000000004300000000000040060000000000804000000000000000000000000000000000',
     members={52,56}},
}
function EXT.meltagun_sources_intact()
    for _,spec in ipairs(EXT.meltagun_sources) do
        local entry=tables[spec.kind]
        local base=entry and entry.base_by_owner and entry.base_by_owner[spec.owner]
        if not base or not entry.owner_by_base or entry.owner_by_base[base]~=spec.owner
           or entry.stride~=spec.size or not entry.copies or #entry.copies==0 then return false end
        local stock=(spec.hex:gsub('..',function(h)return string.char(tonumber(h,16))end))
        for _,block in ipairs(entry.copies) do
            local current=api.read(block+HEADER_BYTES+base,spec.size)
            if not current or #current~=spec.size then return false end
            for _,offset in ipairs(spec.members) do
                local word=u32(current,offset)
                local field=fields[spec.kind..':'..(base+offset)]
                local owned=field and EXT.safety_tx and EXT.safety_tx.owned_value(field)
                if word~=u32(stock,offset) and (owned==nil or word~=owned) then return false end
                current=current:sub(1,offset)..stock:sub(offset+1,offset+4)..current:sub(offset+5)
            end
            if current~=stock then return false end
        end
    end
    return true
end
