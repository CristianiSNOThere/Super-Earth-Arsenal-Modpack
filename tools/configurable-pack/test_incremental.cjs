// Targeted real Arsenal backend checks for the 23-option BR-14 addition.
// Same args as test_arsenal.cjs; every write stays inside a fresh fixture.
const fs=require('fs'),path=require('path');
const original=fs.readFileSync(path.join(__dirname,'test_arsenal.cjs'),'utf8');
const prefix=original.slice(0,original.indexOf('(async()=>{'));
const body=String.raw`
(async()=>{
 assert.equal(manifest.Options.length,23);
 const flag=manifest.Options.findIndex(o=>o.Name==='Enable One True Flag');
 const added=manifest.Options.findIndex(o=>o.Name==='Enable BR-14 Adjudicator Heavy Battle Rifle');
 assert.equal(added,22);assert.equal(manifest.Options[flag].SubOptions.length,29);
 const importDefaults=[];
 for(const enabled of [false,true]){
  records.modsList=[];records.modsLibrary=[];records.setAllOptionsActive=enabled;
  await handler.processAndValidateZipsFromRenderer(library,[release]);
  assert.equal(records.modsList.length,1);
  const mod=records.modsList[0];assert.equal(mod.options.length,23);
  assert.equal(mod.options.filter(o=>o.enabled).length,enabled?23:1);
  assert.equal(mod.options[flag].suboptions.filter(o=>o.enabled).length,enabled?1:0);
  importDefaults.push({enable_all:enabled,enabled:mod.options.filter(o=>o.enabled).length});
 }
 const imported=clone(records.modsList[0]);
 const old=clone(imported.options.slice(0,22));old.forEach((o,i)=>o.enabled=i===0||i===5);
 const merged=deployer.mergeOptionsWithConfig(clone(imported.options),old);
 old.forEach((o,i)=>assert.equal(merged[i].enabled,o.enabled,'Existing selection changed'));
 assert.equal(merged.length,23);
 const checks=[];
 async function run(mask,label,occupied=false){
  await remover.purgeMods();assert.equal(listFiles(game).length,0);
  const mod=clone(imported);mod.enabled=true;mod.deployed=false;
  mod.options.forEach((o,i)=>o.enabled=!!(mask&(1<<i)));
  mod.options[flag].suboptions.forEach((o,i)=>o.enabled=i===0);
  const lib=clone(imported);
  records.modsList=[mod];records.modsLibrary=[lib];records.data.test.mods=[mod];
  const full=await deployer.getFullModData(mod,[lib]);const folders=deployer.getValidFolders(full);
  const desired=manifest.Options.flatMap((o,i)=>(mask&(1<<i))?o.Include:[]);
  if(mask&(1<<flag))desired.push(...manifest.Options[flag].SubOptions[0].Include);
  assert.deepEqual(Array.from(folders).sort(),desired.sort(),label);
  const expected=expectedFiles(desired),existing=[];
  if(occupied)for(const slot of [0,2])for(const suffix of ['','.stream','.gpu_resources']){
   const name='9ba626afa44a3aa3.patch_'+slot+suffix,bytes=Buffer.from('existing fixture '+name);
   fs.writeFileSync(path.join(data,name),bytes);existing.push({name,bytes});
   expected.push('9ba626afa44a3aa3|'+suffix+'|'+digest(bytes));
  }
  const deployed=await deployer.deployMod(mod.uuid,[mod],data,temp,state,[lib]);
  records.modsList=deployed;records.data.test.mods=deployed;
  assert.deepEqual(actualFiles(),expected.sort(),label);
  for(const e of existing)assert(fs.readFileSync(path.join(data,e.name)).equals(e.bytes));
  assert.equal(listFiles(path.join(game,'bin')).length,0);
  checks.push({mask,label,files:expected.length});
  await remover.purgeMods();
  // Arsenal's global purge removes every patch file, including these fixture
  // occupied slots. Their preservation is checked before purge above.
  assert.equal(listFiles(game).length,0,'Global purge left patch files');
 }
 const index=n=>{const i=manifest.Options.findIndex(o=>o.Name.includes(n));assert(i>=0);return i;};
 const small=['APW-1','P-34','CQC-20','RS-422'].reduce((m,n)=>m|(1<<index(n)),0);
 await run(0,'all-off');
 await run(1<<added,'adjudicator-only');
 await run((1<<added)|(1<<index('Tenderizer')),'adjudicator-tenderizer');
 await run(small,'accepted-four-mod-subset');
 await run((1<<23)-1,'full-23-default-flag');
 await run(1<<added,'adjudicator-occupied-slots',true);
 assert.equal(listFiles(game).length,0);
 const report={result:'PASS',manager_version:JSON.parse(fs.readFileSync(path.join(source,'package.json'))).version,
  artifact:release,sha256:digest(fs.readFileSync(release)),cases:checks.length,checks,importDefaults,
  existing_22_selections_preserved:true,new_option_import_default:merged[added].enabled,
  distinct_profile_library_objects:true,real_settings_changed:false,real_deployment_changed:false};
 fs.writeFileSync(path.join(base,'incremental-arsenal.json'),JSON.stringify(report,null,2));
 console.log('PASS: '+checks.length+' focused real Arsenal deployments, import preferences, migration, occupied slots and purge.');
})().catch(error=>{fs.writeFileSync(path.join(fixture,'backend-log.json'),JSON.stringify(logs,null,2));console.error(error);console.error('Fixture:',fixture);process.exitCode=1;});
`;
new Function('require','process',prefix+body)(require,process);
