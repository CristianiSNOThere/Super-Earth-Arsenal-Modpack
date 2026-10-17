-- Embedded after add_hidden_part; only the exact Meltagun path is accepted.
function EXT.add_meltagun_fields(weapon,beam_id,damage_id)
    if weapon.hash~='6CFCC7F8801A0266' or beam_id~=18 or damage_id~=509
       or not EXT.meltagun_sources_intact() then return false end
    local range=field_for_owner(T_BEAM,'18',8,'f32',1000)
    local panic=field_for_owner(T_DAMAGE,'509',52,'u32',1000)
    local buildup=field_for_owner(T_DAMAGE,'509',56,'f32',1000)
    if not range or not panic or not buildup then return false end
    for _,field in ipairs({range,panic,buildup}) do field.meltagun_guard=true end
    -- This exception only permits removing the existing assignment, never
    -- choosing another status. All other effect-assignment IDs stay read-only.
    panic.explicit_validation=true
    add_hidden_part(weapon,'melt_range',range,20,20)
    add_hidden_part(weapon,'melt_panic_type',panic,0,0)
    add_hidden_part(weapon,'melt_panic_buildup',buildup,0,0)
    return true
end
