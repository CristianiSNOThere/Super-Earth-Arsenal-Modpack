// Exercise real Arsenal import/migration for a descriptions-only release.
// Same first three arguments as test_arsenal.cjs, then the previous release ZIP.
const fs=require('fs'),path=require('path');
const original=fs.readFileSync(path.join(__dirname,'test_arsenal.cjs'),'utf8');
const prefix=original.slice(0,original.indexOf('(async()=>{')).replace("const selections=JSON.parse(fs.readFileSync(path.join(base,'selections.json'),'utf8'));","const selections=[];");
const body=String.raw`
(async()=>{
 const previous=path.resolve(process.argv[5]);
 const previousManifest=JSON5.parse(new AdmZip(previous).readAsText('manifest.json'));
 assert.equal(previousManifest.Version,'2.2.0');assert.equal(manifest.Version,'2.2.1');
 const flag=manifest.Options.findIndex(o=>o.Name==='Enable One True Flag');assert(flag>=0);
 for(const active of [false,true]){
  records.modsList=[];records.modsLibrary=[];records.setAllOptionsActive=active;
  await handler.processAndValidateZipsFromRenderer(library,[release]);
  assert.equal(records.modsList.length,1);
  const mod=records.modsList[0];assert.equal(mod.uuid,manifest.Guid);
  assert.equal(mod.description,manifest.Description);
  assert.equal(mod.options.length,24);
  mod.options.forEach((o,i)=>{
   assert.equal(o.name,manifest.Options[i].Name);
   assert.equal(o.description,manifest.Options[i].Description);
   assert(o.description.includes('\n\n- '),'Summary and bullet text lost');
  });
  assert.equal(mod.options.filter(o=>o.enabled).length,active?24:1);
 }
 const current=clone(records.modsList[0]);
 records.modsList=[];records.modsLibrary=[];records.setAllOptionsActive=true;
 await handler.processAndValidateZipsFromRenderer(library,[previous]);
 assert.equal(records.modsList.length,1);
 const old=clone(records.modsList[0]);
 old.options.forEach((o,i)=>o.enabled=i%3===1);
 old.options[flag].enabled=true;
 old.options[flag].suboptions.forEach((o,i)=>o.enabled=i===17);
 const merged=deployer.mergeOptionsWithConfig(clone(current.options),old.options);
 assert.equal(merged.length,24);
 merged.forEach((o,i)=>{
  assert.equal(o.name,old.options[i].name);
  assert.equal(o.enabled,old.options[i].enabled);
  assert.equal(o.description,manifest.Options[i].Description);
 });
 assert.deepEqual(merged[flag].suboptions.map(o=>o.enabled),old.options[flag].suboptions.map(o=>o.enabled));
 assert.equal(current.options[flag].suboptions.length,29);
 const report={result:'PASS',real_arsenal_import:true,all_24_descriptions_exact:true,
  multiline_text_preserved:true,previous_24_selections_preserved:true,flag_choice_preserved:true,
  import_enable_all_preferences:[false,true],real_user_settings_changed:false,real_deployment_changed:false};
 fs.writeFileSync(path.join(base,'public-copy-arsenal.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report));
})().catch(error=>{console.error(error);process.exitCode=1;});
`;
new Function('require','process',prefix+body)(require,process);
