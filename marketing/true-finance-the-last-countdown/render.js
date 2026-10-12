const { chromium } = require(process.env.PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright');
// node render.js <outDir> <fps> <start> <end>  |  node render.js <outDir> - - - t1,t2,...
const [,,out,fps,start,end,times]=process.argv;
(async()=>{
  const b=await chromium.launch({args:['--allow-file-access-from-files']});
  const pg=await b.newPage({viewport:{width:1920,height:1080}});
  pg.on('pageerror',e=>console.log('ERR',e.message));
  await pg.goto('file://'+__dirname+'/film.html'); await pg.waitForFunction(()=>window.READY,null,{timeout:60000});
  const list=times?times.split(',').map(Number):Array.from({length:Math.round((+end-+start)*+fps)},(_,i)=>+start+i/+fps);
  for(const t of list){
    await pg.evaluate(t=>window.render(t),t);
    const name=times?`p_${t.toFixed(2)}.jpg`:`f_${String(Math.round(t*+fps)).padStart(5,'0')}.jpg`;
    await pg.screenshot({path:`${out}/${name}`,type:'jpeg',quality:92});
  }
  await b.close();
})();
