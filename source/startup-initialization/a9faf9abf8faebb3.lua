-- HD2-Addon: mods/codex/preset01_40k_meltagun
local runtime = require('mods/codex/arsenal_preset01_runtime')
local ok, why = runtime.register_profile({
    id = 'preset01_40k_meltagun',
    name = '40-K Meltagun',
    hash = '6CFCC7F8801A0266',
    values = {
        { hash = '6CFCC7F8801A0266', id = 'ergonomics', value = 40 },
        { hash = '6CFCC7F8801A0266', id = 'melt_range', value = 20 },
        { hash = '6CFCC7F8801A0266', id = 'melt_panic_type', value = 0 },
        { hash = '6CFCC7F8801A0266', id = 'melt_panic_buildup', value = 0 }
    },
})
if not ok then error(why) end
return runtime
