-- HD2-Addon: mods/codex/preset01_plas39_accelerator_rifle
local runtime = require('mods/codex/arsenal_preset01_runtime')
local ok, why = runtime.register_profile({
    id = 'preset01_plas39_accelerator_rifle',
    name = 'PLAS-39 Accelerator Rifle',
    hash = '30061F91AF477F5E',
    values = {
        { hash = '30061F91AF477F5E', id = 'capacity', value = 21 },
        { hash = '30061F91AF477F5E', id = 'recoil_dh', value = 2 },
        { hash = '30061F91AF477F5E', id = 'recoil_ch', value = 2 },
        { hash = '30061F91AF477F5E', id = 'recoil_dv', value = 2 },
        { hash = '30061F91AF477F5E', id = 'recoil_cv', value = 2 },
        { hash = '30061F91AF477F5E', id = 'spread_h', value = 0.3 },
        { hash = '30061F91AF477F5E', id = 'spread_v', value = 0.3 },
        { hash = '30061F91AF477F5E', id = 'sway', value = 0.4 },
        { hash = '30061F91AF477F5E', id = 'stagger', value = 25 },
        { hash = '30061F91AF477F5E', id = 'ap_direct', value = 4 },
        { hash = '30061F91AF477F5E', id = 'ap_slight', value = 4 },
        { hash = '30061F91AF477F5E', id = 'ap_large', value = 4 },
        { hash = '30061F91AF477F5E', id = 'blast_outer', value = 2.5 },
        { hash = '30061F91AF477F5E', id = 'blast_shockwave', value = 2.5 }
    },
})
if not ok then error(why) end
return runtime
