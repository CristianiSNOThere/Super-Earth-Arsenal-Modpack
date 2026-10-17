// Extend the established isolated backend fixture with the changed selections.
const fs=require('fs'),path=require('path');
let script=fs.readFileSync(path.join(__dirname,'test_gl52_arsenal.cjs'),'utf8');
const marker=" await run(0,'all-off');";
if(script.split(marker).length!==2)throw Error('Expected one fixture insertion point');
script=script.replace(marker,marker+`
 await run(1<<index('40-K Meltagun'),'meltagun-only');
 await run(1<<index('APW-1'),'amr-only');
 await run((1<<index('40-K Meltagun'))|(1<<index('APW-1')),'meltagun-amr');
 await run((1<<index('40-K Meltagun'))|(1<<index('APW-1'))|(1<<index('GL-52')),'three-changed-mods');
 await run(((1<<25)-1)^(1<<index('40-K Meltagun'))^(1<<index('APW-1')),'full-with-melt-amr-disabled');
 await run((1<<index('40-K Meltagun'))|(1<<index('APW-1')),'melt-amr-occupied-slots',true);
`);
new Function('require','process','__dirname',script)(require,process,__dirname);
