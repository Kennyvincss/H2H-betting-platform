const { chromium } = require(process.env.PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright');
// node render.js <outDir> <fps> <vert 0|1> <alpha 0|1> [frameImage] [times]
const [,,out,fps,vert,alpha,frame,times]=process.argv;
(async()=>{
  const b=await chromium.launch();
  const W=vert==='1'?1080:1920,H=vert==='1'?1920:1080;
  const pg=await b.newPage({viewport:{width:W,height:H}});
  let q='?v='+vert; if(frame&&frame!=='-') q+='&frame='+encodeURIComponent(frame);
  await pg.goto('file://'+__dirname+'/outro.html'+q); await pg.waitForFunction(()=>window.READY); await pg.waitForTimeout(500);
  const list=times?times.split(',').map(Number):Array.from({length:5*+fps},(_,i)=>i/+fps);
  for(const t of list){
    await pg.evaluate(t=>window.render(t),t);
    const name=times?`p_${t.toFixed(2)}.png`:`f_${String(Math.round(t*+fps)).padStart(4,'0')}.png`;
    await pg.screenshot({path:`${out}/${name}`,omitBackground:alpha==='1'});
  }
  await b.close();
})();
