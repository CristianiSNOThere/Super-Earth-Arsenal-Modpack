"""Verify the current canonical Gas Overhaul source and archive."""
from pathlib import Path
import hashlib,sys
REPO=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO/'tools/configurable-pack'))
from build import lua_archive
sys.path.insert(0,str(REPO.parents[1]/'work/expanded-stat-editor'))
from lua_runtime import Lua51
source=Path(__file__).with_name('sterilizer-entry.lua').read_bytes()
assert source==(REPO/'source/startup-initialization/e54e34210bac937e.lua').read_bytes()
Lua51().compile(source,'@mods/codex/sterilizer_armor_control.lua')
archive=lua_archive(0xe54e34210bac937e,source)
target=REPO/'source/configurable-pack/payloads/gas-overhaul/Addon/9ba626afa44a3aa3.patch_0'
assert target.read_bytes()==archive,'Canonical source and payload differ'
print('Gas Overhaul canonical source/archive match:',hashlib.sha256(archive).hexdigest().upper())
