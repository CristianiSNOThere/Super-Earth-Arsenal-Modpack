-- HD2-Addon: mods/codex/flag_settings/preset
-- One complete preset replaces all five configuration values together.
local settings=rawget(_G,'FlagDamageOptionsV1')
if type(settings)~='table' then settings={};_G.FlagDamageOptionsV1=settings end
settings.thousands=@THOUSANDS@
settings.hundreds=@HUNDREDS@
settings.tens=@TENS@
settings.ones=@ONES@
settings.durable_ratio=@RATIO@
return settings
