-- HD2-Addon: mods/codex/arsenal_preset01_modpack
local runtime = require('mods/codex/arsenal_preset01_runtime')
local ok, why = runtime.require_peers({
    'FlagDamagePrototypeV1', 'SaiFocusModV1', 'AR11ArbitratorModV1', 'SterilizerArmorControlV1', 'RapidArcThrowerV1'
})
if not ok then error(why) end
return runtime
