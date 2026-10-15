// Reuse the isolated installed-backend loader; exercise only the changed layout.
// Args: <backend copy> <evidence folder> <Rev3 ZIP>.
const fs=require('fs');
const path=require('path');
const original=fs.readFileSync(path.join(__dirname,'test_arsenal.cjs'),'utf8');
const marker='(async()=>{';
const prefix=original.slice(0,original.indexOf(marker));
const body=String.raw`
(async()=>{
 assert.equal(manifest.Options.length,22,'There must be only 22 top-level switches');
 const flagIndex=manifest.Options.findIndex(o=>o.Name==='Enable One True Flag');
 assert(flagIndex>=0);
 const presets=manifest.Options[flagIndex].SubOptions;
 assert.equal(presets.length,29);
 assert.equal(presets[0].Name,'300 normal / 150 durable (default)');
 assert(manifest.Options.every((o,i)=>i===flagIndex||!o.SubOptions));
 assert(allEntries.every(e=>!e.entryName.includes('/Settings/thousands/')&&
   !e.entryName.includes('/Settings/hundreds/')&&!e.entryName.includes('/Settings/durable/')));
 const importDefaults=[];
 for(const enabled of [false,true]) {
  records.modsList=[];records.modsLibrary=[];records.setAllOptionsActive=enabled;
  await handler.processAndValidateZipsFromRenderer(library,[release]);
  assert.equal(records.modsList.length,1);
  const mod=records.modsList[0];assert.equal(mod.options.length,22);
  const option=mod.options[flagIndex];assert.equal(option.suboptions.length,29);
  assert.equal(option.suboptions.filter(s=>s.enabled).length,enabled?1:0);
  if(enabled)assert.equal(option.suboptions[0].enabled,true);
  importDefaults.push({enable_all:enabled,enabled_mods:mod.options.filter(o=>o.enabled).length,
    flag_choices:option.suboptions.filter(o=>o.enabled).length});
 }
 const imported=clone(records.modsList[0]);
 // A v2 Rev2 enabled Flag carries forward its name, with the new default first.
 const old=clone(imported.options);delete old[flagIndex].suboptions;
 const merged=deployer.mergeOptionsWithConfig(clone(imported.options),old);
 assert.equal(merged[flagIndex].suboptions[0].enabled,true);
 const checks=[];
 async function run(mask,presetIndex,label) {
  await remover.purgeMods();assert.equal(listFiles(game).length,0);
  const mod=clone(imported);mod.enabled=true;mod.deployed=false;
  mod.options.forEach((o,i)=>o.enabled=!!(mask&(1<<i)));
  mod.options[flagIndex].suboptions.forEach((o,i)=>o.enabled=i===presetIndex);
  // Use distinct profile/library objects: all library switches enabled, only
  // the requested subset in the profile. Verify the backend merges correctly.
  const libraryMod=clone(imported);
  records.modsList=[mod];records.modsLibrary=[libraryMod];records.data.test.mods=[mod];
  const full=await deployer.getFullModData(mod,[libraryMod]);
  const folders=deployer.getValidFolders(full);
  const desired=manifest.Options.flatMap((o,i)=>(mask&(1<<i))?o.Include:[]);
  if((mask&(1<<flagIndex))&&presetIndex!==null)desired.push(...presets[presetIndex].Include);
  assert.deepEqual(Array.from(folders).sort(),desired.sort(),label);
  const expected=expectedFiles(desired);
  const deployed=await deployer.deployMod(mod.uuid,[mod],data,temp,state,[libraryMod]);
  records.modsList=deployed;records.data.test.mods=deployed;
  assert.deepEqual(actualFiles(),expected,label);
  if((mask&(1<<flagIndex))&&presetIndex!==null) {
   const cpuFiles=listFiles(data).filter(n=>/\.patch_\d+$/.test(n));
   const flagEntry=allEntries.find(e=>e.entryName.startsWith(manifest.Options[flagIndex].Include[0]+'/')&&/\.patch_\d+$/.test(e.entryName));
   const presetEntry=allEntries.find(e=>e.entryName.startsWith(presets[presetIndex].Include[0]+'/')&&/\.patch_\d+$/.test(e.entryName));
   const flagBody=pack.readFile(flagEntry),presetBody=pack.readFile(presetEntry);
   const flagFile=cpuFiles.find(n=>fs.readFileSync(path.join(data,n)).equals(flagBody));
   const presetFile=cpuFiles.find(n=>fs.readFileSync(path.join(data,n)).equals(presetBody));
   const slot=n=>+n.match(/\.patch_(\d+)$/)[1];
   assert(slot(presetFile)>slot(flagFile),'Preset must be discovered before Flag');
   if(label==='flag-alone-preset-0'||label==='full-max')for(const name of [flagFile,presetFile]) {
    const folder=path.join(base,'flag-loader-rev3',label);fs.mkdirSync(folder,{recursive:true});
    const target=path.join(folder,name),body=fs.readFileSync(path.join(data,name));
    if(fs.existsSync(target))assert(fs.readFileSync(target).equals(body),'Immutable loader fixture changed');
    else fs.writeFileSync(target,body);
   }
  }
  assert.equal(listFiles(path.join(game,'bin')).length,0);
  checks.push({mask,presetIndex,label,files:expected.length});
 }
 const index=name=>manifest.Options.findIndex(o=>o.Name.includes(name));
 const small=['APW-1','P-34','CQC-20','RS-422'].reduce((m,n)=>m|(1<<index(n)),0);
 const peers=(1<<index('SAI'))|(1<<index('Gas Overhaul'))|(1<<flagIndex);
 await run(0,0,'all-off-default-preset-selected');
 await run(0,28,'all-off-max-preset-selected');
 await run(small,0,'accepted-four-mod-subset');
 await run(1<<flagIndex,null,'flag-no-preset-uses-internal-default');
 for(let i=0;i<presets.length;i++) {
  await run(1<<flagIndex,i,'flag-alone-preset-'+i);
  await run(peers,i,'flag-sai-gas-preset-'+i);
 }
 await run((1<<22)-1,0,'full-default');
 await run((1<<22)-1,28,'full-max');
 await remover.purgeMods();assert.equal(listFiles(game).length,0);
 const report={result:'PASS',manager_version:JSON.parse(fs.readFileSync(path.join(source,'package.json'))).version,
  artifact:release,sha256:digest(fs.readFileSync(release)),presets:presets.length,top_level_options:22,
  single_flag_dropdown:true,isolated_deployment_cases:checks.length,checks,importDefaults,
  distinct_profile_library_objects:true,real_settings_changed:false,real_deployment_changed:false};
 fs.writeFileSync(path.join(base,'flag-dropdown-arsenal-rev3.json'),JSON.stringify(report,null,2));
 console.log('PASS: one Flag dropdown; '+checks.length+' targeted Arsenal deployments, all 29 presets and peer combinations.');
})().catch(error=>{
 fs.writeFileSync(path.join(fixture,'backend-log.json'),JSON.stringify(logs,null,2));
 console.error(error);console.error('Fixture:',fixture);process.exitCode=1;
});
`;
new Function('require','process',prefix+body)(require,process);
