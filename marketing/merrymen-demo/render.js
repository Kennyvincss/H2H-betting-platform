const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const [,,outDir,fps,start,end,step] = process.argv;
(async () => {
  const b = await chromium.launch({ args:['--allow-file-access-from-files'] });
  const pg = await b.newPage({ viewport:{width:1920,height:1080} });
  await pg.goto('file://'+__dirname+'/film.html'); await pg.waitForTimeout(1500);
  await pg.evaluate(()=>document.fonts.ready);
  const times = step ? [] : null;
  if (step) { for (const x of step.split(',')) times.push(+x); }
  const list = times || Array.from({length: Math.round((+end - +start)*+fps)}, (_,i)=> +start + i/+fps);
  let i=0;
  for (const t of list) {
    await pg.evaluate(t=>window.render(t), t);
    // images: ensure decoded
    await pg.evaluate(()=>Promise.all([...document.images].map(im=>im.decode().catch(()=>{}))));
    const name = times ? `p_${t.toFixed(1)}.jpg` : `f_${String(Math.round(t*+fps)).padStart(5,'0')}.jpg`;
    await pg.screenshot({ path: `${outDir}/${name}`, type:'jpeg', quality:92 });
    i++;
  }
  await b.close(); console.log('frames', i);
})();
