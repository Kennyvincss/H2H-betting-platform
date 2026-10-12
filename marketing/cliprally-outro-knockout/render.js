const { chromium } = require(process.env.PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright');
// node render.js <outDir> <fps> <vert 0|1> [frame.png|-] [t1,t2,...]
const [,,out,fps,vert,frame,times]=process.argv;
(async()=>{
  const b=await chromium.launch();
  const W=vert==='1'?1080:1920,H=vert==='1'?1920:1080;
  const pg=await b.newPage({viewport:{width:W,height:H}});
  let q='?v='+vert; if(frame&&frame!=='-') q+='&frame='+encodeURIComponent('file://'+require('path').resolve(frame));
  await pg.goto('file://'+__dirname+'/outro6.html'+q); await pg.waitForFunction(()=>window.READY,null,{timeout:30000});
  const list=times?times.split(',').map(Number):Array.from({length:5*+fps},(_,i)=>i/+fps);
  for(const t of list){
    await pg.evaluate(t=>window.render(t),t);
    const name=times?`p_${t.toFixed(2)}.png`:`f_${String(Math.round(t*+fps)).padStart(4,'0')}.png`;
    await pg.screenshot({path:`${out}/${name}`});
  }
  await b.close();
})();
