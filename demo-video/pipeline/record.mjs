import { chromium } from 'playwright';
import fs from 'fs';
const B='http://127.0.0.1:8080', W=1920, H=1080, PAD=0.6;
const timing = JSON.parse(fs.readFileSync('../build/timing.json'));
const only = process.argv[2];
const b = await chromium.launch({executablePath: process.env.CH, args:['--proxy-server='+process.env.HTTPS_PROXY,'--proxy-bypass-list=127.0.0.1:8080;localhost:8080']});

// one-off login to reuse the session in signed-in scenes
if (!fs.existsSync('auth.json')) {
  const c = await b.newContext(); const p = await c.newPage();
  await p.goto(B+'/account',{waitUntil:'networkidle'}); await p.waitForTimeout(1000);
  await p.fill('input[type=email]', process.env.E); await p.fill('input[type=password]', process.env.P);
  await p.getByRole('button',{name:'Sign in'}).click(); await p.waitForTimeout(5000);
  await c.storageState({path:'auth.json'}); await c.close();
}

const CURSOR = `addEventListener('DOMContentLoaded',()=>{const d=document.createElement('div');d.id='__cur';
d.style.cssText='position:fixed;z-index:2147483647;pointer-events:none;width:22px;height:22px;margin:-4px 0 0 -4px;left:-50px;top:-50px;transition:transform .12s';
d.innerHTML='<svg width="30" height="30" viewBox="0 0 24 24"><path d="M4 2l16 10-7 1.5L9.5 21z" fill="#111" stroke="#fff" stroke-width="1.6"/></svg>';
document.body.appendChild(d);addEventListener('mousemove',e=>{d.style.left=e.clientX+'px';d.style.top=e.clientY+'px'},true);
addEventListener('mousedown',()=>d.style.transform='scale(.8)',true);addEventListener('mouseup',()=>d.style.transform='',true);});`;

const sleep = ms => new Promise(r=>setTimeout(r,ms));
async function scroll(p, to, ms){ await p.evaluate(async ([to,ms])=>{const s=scrollY,dy=(to==='end'?document.documentElement.scrollHeight-innerHeight:to)-s,t0=performance.now();
  await new Promise(r=>{const f=t=>{const k=Math.min(1,(t-t0)/ms),e=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;scrollTo(0,s+dy*e);k<1?requestAnimationFrame(f):r()};requestAnimationFrame(f)})},[to,ms]); }
async function scrollTo(p, loc, ms, off=120){ const y = await loc.first().evaluate((e,off)=>e.getBoundingClientRect().top+scrollY-off, off); await scroll(p, y, ms); }
async function move(p, loc){ const bb = await loc.first().boundingBox(); if(!bb) return; await p.mouse.move(bb.x+bb.width/2, bb.y+bb.height/2, {steps:14}); await sleep(120); }
async function click(p, loc){ await move(p, loc); await loc.first().click(); }
async function type(p, loc, text){ await click(p, loc); await loc.first().fill(''); await loc.first().pressSequentially(text,{delay:45}); }
const cont = p => p.getByRole('button',{name:/^Continue/}).first();
const btn = (p, re) => p.locator('main button').filter({hasText:re});

async function login(p, path, ms=0){ await p.goto(B+path,{waitUntil:'networkidle'}); await sleep(800); }

const scenes = {
  '01_intro': {auth:true, start:'/', run: async (p,d)=>{ await p.mouse.move(300,300); await sleep(d*1000*0.45); await move(p,p.getByText('Get a Cleaning Quote').first()); await sleep(1500); await move(p,p.getByText('View Services').first()); }},
  '02_home': {auth:true, start:'/', run: async (p,d)=>{ await scrollTo(p,p.getByText('Tell us about your home'),2200,300); await sleep(1500); await scrollTo(p,p.getByText('Pick a starting point.'),2200,100); await sleep(1500); await scroll(p,'end',2500); }},
  '03_services': {auth:true, start:'/services', run: async (p,d)=>{ await sleep(1500); await scrollTo(p,p.getByText('Deep Clean').first(),2500,80); await sleep(1200); await scrollTo(p,p.getByText('Move In / Move Out').first(),2500,80); await sleep(1200); await scrollTo(p,p.getByText('Custom Clean').first(),2500,80); }},
  '04_how': {auth:true, start:'/how-it-works', run: async (p,d)=>{ await sleep(1500); await scrollTo(p,p.getByText('After you book',{exact:false}).first(),2500,100); await sleep(1200); await scroll(p,'end',2500); }},
  '05_reviews_referrals': {auth:true, start:'/reviews', run: async (p,d)=>{ await sleep(2500); await click(p,p.getByRole('link',{name:'Get a quote'}).first()).catch(()=>{}); await p.goto(B+'/referrals',{waitUntil:'networkidle'}); await sleep(600); await p.mouse.move(700,400,{steps:20}); }},
  '06_book_a': {auth:false, start:'/book', run: async (p,d)=>{
      await click(p,p.locator('input[type=email]')); await p.locator('input[type=email]').fill(process.env.E); await p.locator('input[type=password]').fill(process.env.P);
      await click(p,p.getByRole('button',{name:'Sign in'})); await p.locator('main button').filter({hasText:/^Duplex$/}).first().waitFor(); await sleep(600);
      await click(p,btn(p,/^Duplex$/)); await click(p,btn(p,/^3$/).first()); await click(p,btn(p,/^Moderate$/));
      await click(p,cont(p)); await sleep(800);
      await click(p,btn(p,/^Standard Clean/)); await sleep(500); await click(p,btn(p,/^Sofa Cleaning/)); await click(p,btn(p,/^Oven Cleaning/)); }},
  '07_book_b': {auth:true, start:'/book', pre: async p=>{ p.__dbg=1; await sleep(1500); await cont(p).click(); await sleep(500); await btn(p,/^Standard Clean/).first().click(); await btn(p,/^Sofa Cleaning/).first().click(); await cont(p).click(); await sleep(500); await scroll(p,0,10); },
      run: async (p,d)=>{ await click(p,btn(p,/^Living room$/)); await click(p,cont(p)); await sleep(700);
        await click(p,p.locator('main input').nth(0)); await p.locator('main input').nth(0).fill('12 Admiralty Way, Lekki'); await p.locator('main input').nth(4).fill('105102'); await click(p,btn(p,/^Lekki/)); await sleep(300); await click(p,cont(p)); await sleep(1200);
        const slot=p.locator('main button').filter({hasText:/^\d{1,2}:\d{2}/}); if(!(await slot.count())){ await p.locator('main button').filter({hasText:/View next available/}).first().click(); await sleep(800);} await click(p,slot.first()); }},
  '08_book_c': {auth:true, start:'/book', pre: async p=>{ await sleep(1500); await cont(p).click(); await sleep(500); await btn(p,/^Standard Clean/).first().click();
        for(const i of [0,1]){ await cont(p).click(); await sleep(500); }
        await p.locator('main input').nth(0).fill('12 Admiralty Way, Lekki'); await p.locator('main input').nth(4).fill('105102'); await btn(p,/^Lekki/).first().click(); await cont(p).click(); await sleep(1500);
        const slot=p.locator('main button').filter({hasText:/^\d{1,2}:\d{2}/}); if(!(await slot.count())){ await p.locator('main button').filter({hasText:/View next available/}).first().click(); await sleep(800);} await slot.first().click(); await cont(p).click(); await sleep(800); await scroll(p,0,10); },
      run: async (p,d)=>{ const ins=p.locator('main input'); await click(p,ins.nth(0)); await ins.nth(0).fill('Kehinde Adeyeye'); await click(p,ins.nth(1)); await ins.nth(1).fill('kehinde@example.com');
        await click(p,ins.nth(2)); await ins.nth(2).fill('+234 801 234 5678'); await click(p,p.locator('main button').filter({hasText:/^Weekly$/}));
        const promo=p.getByPlaceholder('WELCOME10'); await scrollTo(p,promo,800,400); await click(p,promo); await promo.fill('WELCOME10'); await click(p,p.getByRole('button',{name:'Apply'})).catch(()=>{}); await sleep(900);
        await click(p,cont(p)); await sleep(500); await scroll(p,'end',1400); const pay=p.locator('main button').filter({hasText:/deposit securely/}); await move(p,pay).catch(()=>{}); }},
  '09_account': {auth:true, start:'/booking/NS-66890', run: async (p,d)=>{ await p.mouse.move(900,300,{steps:10}); await sleep(1000);
      for (const t of [/Confirmed/, /Reschedule/, /Pay balance/, /Booking created/]) { await move(p,p.getByText(t).first()).catch(()=>{}); await sleep(1100); }
      await move(p,p.getByRole('link',{name:'Rescheduling'})).catch(()=>{}); await sleep(500); await move(p,p.getByRole('link',{name:'Terms'})).catch(()=>{}); await sleep(400); await move(p,p.getByRole('link',{name:'Refund policy'})).catch(()=>{}); }},
  '10_owner_overview': {auth:false, start:'/owner/login', run: async (p,d)=>{ await type(p,p.locator('input[type=email]'),process.env.E); await click(p,p.locator('input[type=password]')); await p.locator('input[type=password]').fill(process.env.P);
        await click(p,p.getByRole('button',{name:'Sign in'})); await sleep(3000); await p.mouse.move(700,450,{steps:20}); await scroll(p,400,2000); }},
  '11_owner_bookings': {auth:true, start:'/owner/bookings', run: async (p,d)=>{ await sleep(800); await click(p,p.getByRole('button',{name:'Confirmed'}).first()).catch(()=>{}); await sleep(400);
        await click(p,p.getByText('NS-66890').first()); await sleep(2000); await scroll(p,500,2000); await sleep(800); await scroll(p,'end',2000); }},
  '12_owner_calendar': {auth:true, start:'/owner/calendar', run: async (p,d)=>{ await sleep(800); await click(p,p.getByRole('button',{name:'Day'})); await sleep(600); await click(p,p.getByRole('button',{name:'Month'})); await sleep(600); await click(p,p.getByRole('button',{name:'Week'})); }},
  '13_owner_customers': {auth:true, start:'/owner/customers', run: async (p,d)=>{ await sleep(1000); await move(p,p.getByRole('button',{name:'Send reminder'}).nth(2)).catch(()=>{}); await sleep(800); await scroll(p,'end',2500); }},
  '14_owner_payments': {auth:true, start:'/owner/payments', run: async (p,d)=>{ await sleep(1500); await scroll(p,'end',2000); }},
  '15_owner_analytics': {auth:true, start:'/owner/analytics', run: async (p,d)=>{ await sleep(800); await click(p,p.getByRole('button',{name:'Weekly'})).catch(()=>{}); await sleep(300); await scrollTo(p,p.getByText('Business insights'),2000,100); await sleep(1200); await scroll(p,'end',2000); }},
  '16_owner_reviews_notif': {auth:true, start:'/owner/reviews', run: async (p,d)=>{ await sleep(2200); await click(p,p.locator('a[href="/owner/notifications"]')); await sleep(800); await p.mouse.move(700,350,{steps:20}); }},
  '17_owner_settings': {auth:true, start:'/owner/settings', run: async (p,d)=>{ await sleep(800); for (const t of ['Availability & booking','Cancellation policy','Services','Service areas & travel fees','Promo codes']) { await scrollTo(p,p.getByText(t,{exact:true}).first(),1300,90).catch(()=>{}); await sleep(700);} }},
  '18_outro': {auth:true, start:'/', run: async (p,d)=>{ await p.mouse.move(-10,-10); }},
};

for (const s of timing) {
  if (only && !s.id.startsWith(only)) continue;
  const sc = scenes[s.id]; const dur = s.dur + PAD + (s.id==='18_outro'?2:0);
  const ctx = await b.newContext({viewport:{width:W,height:H}, recordVideo:{dir:'tmpvid',size:{width:W,height:H}}, ...(sc.auth?{storageState:'auth.json'}:{})});
  await ctx.addInitScript(CURSOR);
  const t0 = Date.now(); const p = await ctx.newPage(); p.setDefaultTimeout(6000);
  await p.goto(B+sc.start,{waitUntil:'networkidle'}); await sleep(1200);
  if (sc.pre) await sc.pre(p);
  const ready = (Date.now()-t0)/1000;
  try { await sc.run(p, s.dur); } catch(e){ console.log('WARN',s.id,e.message.split('\n')[0]); await p.screenshot({path:'shots/fail_'+s.id+'.png'}); }
  const used = (Date.now()-t0)/1000 - ready;
  if (used < dur) await sleep((dur-used)*1000);
  const v = p.video(); await ctx.close(); fs.renameSync(await v.path(), `clips/${s.id}.webm`);
  fs.writeFileSync(`clips/${s.id}.json`, JSON.stringify({ready, dur, used}));
  console.log(s.id, 'ready', ready.toFixed(1), 'actions', used.toFixed(1), 'target', dur.toFixed(1), used>dur+0.5?'  <-- OVERRUN':'');
}
await b.close();
