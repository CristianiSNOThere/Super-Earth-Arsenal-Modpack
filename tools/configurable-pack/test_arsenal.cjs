// Run the installed Arsenal backend against an isolated filesystem/profile.
// Usage: node test_arsenal.cjs <read-only backend copy> <evidence dir> <candidate ZIP>
// Backend copy must contain package.json, obfuscated_src/main and node_modules.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert/strict');
const crypto = require('crypto');
const source = path.resolve(process.argv[2]);
const base = path.resolve(process.argv[3]);
fs.mkdirSync(base, {recursive: true});
const fixture = path.join(base, 'manager-fixture-' + crypto.randomUUID());
assert(!fs.existsSync(fixture), 'Fixture already exists; inspect before retrying.');
const fsExtra = require(path.join(source, 'node_modules/fs-extra'));
const extractZip = require(path.join(source, 'node_modules/extract-zip'));
const AdmZip = require(path.join(source, 'node_modules/adm-zip'));
const JSON5 = require(path.join(source, 'node_modules/json5'));
const game = path.join(fixture, 'Helldivers 2');
const data = path.join(game, 'data');
const library = path.join(fixture, 'library');
const temp = path.join(fixture, 'temp');
const state = path.join(fixture, 'state');
for (const folder of [data, path.join(game, 'bin'), library, temp, state]) fs.mkdirSync(folder, {recursive:true});
const records = {modsList:[], modsLibrary:[], userModsDir:library, userGameDir:game,
  selectedProfile:'test', dataPath:state, setModsActive:true, setAllOptionsActive:true, data:{test:{mods:[]}}};
const logs = [];
const localConsole = Object.fromEntries(['log','warn','error'].map(level=>[level,(...args)=>logs.push({level,message:args.map(String).join(' ')})]));
const utils = {
  readData:(key,all)=>{logs.push({config_read:key,all:!!all});return all?records.data:records[key];},
  writeData:(key,value)=>{records[key]=value;fs.writeFileSync(path.join(state, 'settings.json'),JSON.stringify(records,null,2));},
  cleanFileName:value=>value.replace(/[<>:"/\\|?*]/g,'_'),
  generateUniqueFileName:(name,extension,directory)=>{let result=name,n=1;while(fs.existsSync(path.join(directory,result+extension)))result=name+'-'+n++;return result;},
  stripBOM:value=>value.replace(/^\uFEFF/,''),
  forceDeletePath:async target=>{assert(path.resolve(target).startsWith(fixture+path.sep));await fsExtra.remove(target);},
};
const localDB = {initialized:true, removeModHeaders:()=>true};
const cache = new Map();
function load(relative) {
  const absolute=path.join(source,'obfuscated_src/main',relative);
  if(cache.has(absolute))return cache.get(absolute).exports;
  const module={exports:{}};cache.set(absolute,module);
  function localRequire(name) {
    if(['fs','path','crypto'].includes(name))return require(name);
    if(name==='fs-extra')return fsExtra;
    if(name==='extract-zip')return extractZip;
    if(name==='adm-zip')return AdmZip;
    if(name==='json5')return JSON5;
    if(name==='electron')return {dialog:{showOpenDialog:async()=>{throw new Error('Unexpected UI access');}}};
    if(name.endsWith('/utils')||name==='./utils')return utils;
    if(name.endsWith('/constants'))return {MODS_DIR:library,DATA_PATH:state};
    if(name.endsWith('/LocalDB'))return localDB;
    if(['node-unrar-js','node-7z','7zip-min','7zip-bin'].includes(name))return {};
    if(name.startsWith('.')) {
      const resolved=path.relative(path.join(source,'obfuscated_src/main'),path.resolve(path.dirname(absolute),name+'.js'));
      return load(resolved);
    }
    throw new Error('Unexpected dependency: '+name);
  }
  const context=vm.createContext({module,exports:module.exports,require:localRequire,console:localConsole,
    process:{platform:process.platform,env:{DEV:'true'},resourcesPath:''},Buffer,setTimeout,clearTimeout});
  new vm.Script(fs.readFileSync(absolute,'utf8'),{filename:absolute}).runInContext(context,{timeout:5000});
  return module.exports;
}
const handler=load('modsHandler.js');
const icons=load('modules/iconHandler.js');
const deployer=load('modules/modDeployer.js');
const remover=load('modules/modRemover.js');
const release=path.resolve(process.argv[4]);
const selections=JSON.parse(fs.readFileSync(path.join(base,'selections.json'),'utf8'));
const digest=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const listFiles=directory=>fs.readdirSync(directory,{recursive:true,withFileTypes:true})
 .filter(e=>e.isFile()).map(e=>path.relative(directory,path.join(e.parentPath||e.path,e.name)).replaceAll('\\','/')).sort();
const clone=o=>JSON.parse(JSON.stringify(o));
const pack=new AdmZip(release);
const manifest=JSON5.parse(pack.readAsText('manifest.json'));
const allEntries=pack.getEntries().filter(e=>!e.isDirectory);
function expectedFiles(folders) {
 const entries=[];
 for(const folder of folders) for(const e of allEntries) {
  if(e.entryName.startsWith(folder+'/') && /^.+\.patch_\d+(?:\.stream|\.gpu_resources)?$/.test(e.entryName)) {
   const basename=path.basename(e.entryName);
   entries.push({stem:basename.replace(/\.patch_\d+.*$/,''),
     suffix:basename.replace(/^.+\.patch_\d+/,''),hash:digest(pack.readFile(e))});
  }
 }
 return entries.map(e=>`${e.stem}|${e.suffix}|${e.hash}`).sort();
}
function actualFiles() {
 return listFiles(data).map(name=>{
  assert(/^.+\.patch_\d+(?:\.stream|\.gpu_resources)?$/.test(name),name);
  return `${name.replace(/\.patch_\d+.*$/,'')}|${name.replace(/^.+\.patch_\d+/,'')}|${digest(fs.readFileSync(path.join(data,name)))}`;
 }).sort();
}
(async()=>{
 assert.equal(manifest.Options.length,27);
 // Exercise the installed import code and its two global import preferences.
 const importDefaults=[];
 for(const active of [false,true]) {
  records.modsList=[];records.modsLibrary=[];records.setAllOptionsActive=active;
  await handler.processAndValidateZipsFromRenderer(library,[release]);
  assert.equal(records.modsList.length,1);
  const mod=records.modsList[0];
  assert.equal(mod.uuid,manifest.Guid);assert.equal(mod.options.length,27);
  // With "enable all" off, Arsenal still enables the first top-level option.
  assert.equal(mod.options.filter(o=>o.enabled).length,active?27:1);
  if(!active)assert.equal(mod.options[0].enabled,true);
  importDefaults.push({setAllOptionsActive:active,enabled_options:mod.options.filter(o=>o.enabled).length});
 }
 const imported=clone(records.modsList[0]);
 // Legacy v1 option cannot silently map to 22 independently named toggles.
 const oldConfig=[{name:'Enable Super Earth Arsenal Mod Pack',enabled:true}];
 const migrated=deployer.mergeOptionsWithConfig(clone(imported.options),oldConfig);
 assert.equal(migrated.length,27);
 const migration={legacy_name_does_not_match_new_options:true,review_new_switches_required:true};
 const checks=[];
 async function run(mask,label,flagControls=false,choice=null,occupied=false) {
  await remover.purgeMods();assert.equal(listFiles(game).length,0);
  const mod=clone(imported);mod.enabled=true;mod.deployed=false;
  mod.options.forEach((o,i)=>{
   o.enabled=i<22?!!(mask&(1<<i)):flagControls;
   if(choice&&i>=22&&o.suboptions) {
    const selected=choice[i-22];
    o.suboptions.forEach((s,j)=>s.enabled=j===selected);
   }
  });
  records.modsList=[mod];records.modsLibrary=[mod];records.data.test.mods=[mod];
  const full=await deployer.getFullModData(mod, [mod]);
  const folders=deployer.getValidFolders(full);
  const desired=manifest.Options.slice(0,22).flatMap((o,i)=>(mask&(1<<i))?o.Include:[]);
  if(flagControls)manifest.Options.slice(22).forEach((o,i)=>desired.push(...o.SubOptions[choice?choice[i]:0].Include));
  assert.deepEqual(Array.from(folders).sort(),desired.sort(),'Manager ignored requested selections');
  assert.equal(folders.length,new Set(folders).size,'Duplicate Include folder');
  const expected=expectedFiles(folders);
  const occupiedFiles=[];
  if(occupied)for(const slot of [0,2])for(const suffix of ['', '.stream','.gpu_resources']) {
   const name=`9ba626afa44a3aa3.patch_${slot}${suffix}`;
   const body=Buffer.from(`isolated existing mod fixture ${slot}${suffix}`);
   fs.writeFileSync(path.join(data,name),body);occupiedFiles.push({name,body});
   expected.push(`9ba626afa44a3aa3|${suffix}|${digest(body)}`);
  }
  expected.sort();
  const deployed=await deployer.deployMod(mod.uuid,[mod],data,temp,state,[mod]);
  records.modsList=deployed;records.modsLibrary=deployed;records.data.test.mods=deployed;
  assert.deepEqual(actualFiles(),expected,`Payload mismatch for ${label}`);
  for(const f of occupiedFiles)assert(fs.readFileSync(path.join(data,f.name)).equals(f.body),'Existing patch overwritten');
  assert.equal(listFiles(path.join(game,'bin')).length,0);
  // Per base archive numbering must be contiguous from zero in a clean fixture.
  const slots={};
  for(const name of listFiles(data).filter(n=>/\.patch_\d+$/.test(n))) {
   const m=name.match(/^(.+)\.patch_(\d+)$/);(slots[m[1]]??=[]).push(+m[2]);
  }
  if(!occupied)for(const nums of Object.values(slots))assert.deepEqual(nums.sort((a,b)=>a-b),nums.map((_,i)=>i));
  checks.push({mask,label,files:expected.length,exact_payloads:true});
 }
 for(let i=0;i<selections.length;i++) {
  const mask=selections[i];await run(mask,'mask-'+mask);
  if((i+1)%200===0)console.log(`Deployment matrix: ${i+1}/${selections.length}`);
 }
 // All 5 settings groups enabled with Flag disabled must not deploy its main mod.
 await run(0,'disabled-flag-with-default-controls',true);
 const flagIndex=manifest.Options.findIndex(o=>o.Name.includes('One True Flag'));
 assert(flagIndex>=0&&flagIndex<22);
 for(const selection of [0,(1<<22)-1]) await run(selection,'flag-controls-'+selection,true);
 await run(1<<flagIndex,'flag-zero',true,[0,1,0,0,0]);
 await run(1<<flagIndex,'flag-9999-equal',true,[9,9,9,9,1]);
 await run(1<<flagIndex,'flag-1337-equal',true,[1,0,3,7,1]);
 await run(0,'disabled-flag-9999-controls',true,[9,9,9,9,1]);
 await run((1<<22)-1,'occupied-archive-slots',false,null,true);
 await remover.purgeMods();assert.equal(listFiles(game).length,0);
 const result={result:'PASS',manager_version:JSON.parse(fs.readFileSync(path.join(source,'package.json'))).version,
  artifact:release,sha256:digest(fs.readFileSync(release)),selection_cases:selections.length,
  additional_cases:checks.length-selections.length,importDefaults,migration,checks,
  fixture,live_profile_changed:false,real_game_directory_changed:false,game_launched:false};
 fs.writeFileSync(path.join(base,'arsenal-deployment.json'),JSON.stringify(result,null,2));
 console.log(`PASS: ${checks.length} isolated deployments; exact files, archive slots, toggling and purge.`);
})().catch(error=>{
 fs.writeFileSync(path.join(fixture,'backend-log.json'),JSON.stringify(logs,null,2));
 console.error(error);console.error('Fixture:',fixture);process.exitCode=1;
});
