const {chromium}=require('playwright');
const axe=require('axe-core');
const assert=require('node:assert/strict');
const fs=require('node:fs');const path=require('node:path');
const ROOT=path.resolve(__dirname,'..'),BASE=process.env.BASE_URL||'http://127.0.0.1:4208/';
const content=JSON.parse(fs.readFileSync(path.join(ROOT,'content.json'),'utf8'));
const output=path.join(ROOT,'docs','screenshots');fs.mkdirSync(output,{recursive:true});
(async()=>{
 const browser=await chromium.launch();const report={browser:browser.version(),base:BASE,checkedAt:new Date().toISOString(),viewports:[],limitations:['Headless Chromium only; no physical phone or screen-reader test.','200% zoom modeled as 720 CSS pixels on a 1440px display (device scale 2).','No real business messages or calls sent.','No production-network Lighthouse or field Core Web Vitals measurements.']};
 try{
  for(const width of [320,390,768,1440]){
   const page=await browser.newPage({viewport:{width,height:900},hasTouch:width<800});const errors=[],bad=[],external=[];
   page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400)bad.push(r.url())});page.on('request',r=>{if(!r.url().startsWith(BASE))external.push(r.url())});
   await page.goto(BASE);await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
   assert.equal(await page.locator('h1').count(),1);assert.equal(await page.locator('form,input').count(),0);
   assert.equal(await page.locator('a[href=""],a[href="#"]').count(),0);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow ${width}`);
   await page.keyboard.press('Tab');assert.equal(await page.locator('.skip-link').evaluate(e=>document.activeElement===e),true);await page.keyboard.press('Enter');assert.equal(await page.locator('main').evaluate(e=>document.activeElement===e),true);
   const menu=page.locator('.menu-button');
   if(width<=800){await menu.tap();assert.equal(await menu.getAttribute('aria-expanded'),'true');await page.keyboard.press('Escape');assert.equal(await menu.getAttribute('aria-expanded'),'false');assert(await menu.evaluate(e=>document.activeElement===e));await menu.click();await page.locator('nav a[href="#contact"]').click();assert.equal(await menu.getAttribute('aria-expanded'),'false');assert(await page.locator('#contact').evaluate(e=>document.activeElement===e));}
   else assert.equal(await menu.isVisible(),false);
   for(const link of await page.locator('a[href^="#"]').all()){const id=(await link.getAttribute('href')).slice(1);assert.equal(await page.locator('[id="'+id+'"]').count(),1);}
   const facebook=await page.locator('a[href*="facebook.com"]').evaluateAll(es=>es.map(e=>e.href));assert(facebook.length>0);assert(facebook.every(h=>h===content.facebook));
   const telephone=await page.locator('a[href^="tel:"]').evaluateAll(es=>es.map(e=>e.getAttribute('href')));
   assert.equal(telephone.length,4);assert(telephone.every(h=>h==='tel:+13134519200'));
   assert.equal(await page.locator('a[href^="mailto:"]').getAttribute('href'),'mailto:info@thecomputerhub.net');
   assert.equal(await page.locator('a[href*="google.com/maps"]').getAttribute('href'),content.address.directions);
   assert.equal(await page.locator('.repair-promo .button').getAttribute('href'),'tel:+13134519200');
   assert.match(await page.locator('#repair-title').innerText(),/Slow computer\?\s*Broken screen\?/);
   const photo=page.locator('.repair-photo img');assert.match(await photo.getAttribute('alt'),/Illustrative typing photo/);
   assert(await photo.evaluate(i=>i.complete&&i.naturalWidth===620&&i.naturalHeight===770));
   assert(await page.locator('#owner-note').isVisible());
   assert.equal(await page.locator('.contact-intro .hours-table tr').count(),7);
   assert.deepEqual(await page.locator('.hours-table th').allTextContents(),content.hours.map(h=>h.day));
   assert.deepEqual(await page.locator('.hours-table td').allTextContents(),content.hours.map(h=>h.time));
   const hoursBox=await page.locator('.contact-intro .hours').boundingBox(),detailsBox=await page.locator('.contact-details').boundingBox(),introBox=await page.locator('.contact-intro>p:not(.eyebrow)').boundingBox();
   assert(hoursBox.y>=introBox.y+introBox.height,'hours below contact introduction');
   if(width>800)assert(hoursBox.x+hoursBox.width<=detailsBox.x,'hours in desktop left column');
   else assert(hoursBox.y+hoursBox.height<=detailsBox.y,'hours stack above mobile contacts');
   await page.addScriptTag({content:axe.source});const a=await page.evaluate(async()=>axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}}));
   assert.deepEqual(a.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)})),[],`axe at ${width}`);
   const small=await page.locator('a,button').evaluateAll(es=>es.filter(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&e.className!=='skip-link'&&(r.width<44||r.height<44)}).map(e=>({text:e.textContent.trim(),w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height})));assert.deepEqual(small,[],`targets ${width}`);
   assert.deepEqual(errors,[]);assert.deepEqual(bad,[]);assert.deepEqual(external,[]);
   await page.evaluate(()=>{document.activeElement.blur();scrollTo(0,0)});await page.screenshot({path:path.join(output,`${width===1440?'desktop':width===390?'mobile':'viewport-'+width}.png`),fullPage:true});
   const perf=await page.evaluate(()=>({resources:performance.getEntriesByType('resource').filter(r=>r.name.startsWith(location.origin)).map(r=>({name:r.name.split('/').pop(),bytes:r.encodedBodySize})),domContentLoadedMs:performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd}));
   report.viewports.push({width,axeViolations:a.violations.length,axeIncomplete:a.incomplete.map(v=>v.id),performance:perf});console.log(`PASS ${width}: layout, links, keyboard/menu, 44px targets, axe (${a.violations.length} violations)`);await page.close();
  }
  const nojs=await browser.newPage({javaScriptEnabled:false,viewport:{width:320,height:900}});await nojs.goto(BASE);assert(await nojs.locator('nav').isVisible());await nojs.locator('nav a[href="#contact"]').click();assert(nojs.url().endsWith('#contact'));assert(await nojs.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await nojs.close();console.log('PASS no-JavaScript content/navigation');
  const motion=await browser.newPage({reducedMotion:'reduce',viewport:{width:390,height:900}});await motion.goto(BASE);assert.equal(await motion.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior),'auto');await motion.close();console.log('PASS reduced motion');
  const zoom=await browser.newPage({viewport:{width:720,height:450},deviceScaleFactor:2});await zoom.goto(BASE);assert(await zoom.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await zoom.locator('.menu-button').click();assert(await zoom.locator('nav').isVisible());await zoom.screenshot({path:path.join(output,'zoom-200-equivalent.png'),fullPage:true});await zoom.close();console.log('PASS 200% equivalent reflow (720 CSS px, scale 2)');
  // Future carousel exercised using clearly isolated test-only images, not published content.
  const slide=await browser.newPage({viewport:{width:390,height:900},hasTouch:true});await slide.setContent('<html lang="en"><head></head><body><div class="photo-slider" aria-label="Test photographs"><figure class="slide">TEST PHOTO ONE</figure><figure class="slide" hidden>TEST PHOTO TWO</figure><div class="slider-controls" hidden><button data-prev aria-label="Previous photograph">←</button><span data-position role="status"></span><button data-next aria-label="Next photograph">→</button></div></div></body></html>');await slide.addStyleTag({path:path.join(ROOT,'assets/site.css')});await slide.addScriptTag({path:path.join(ROOT,'assets/site.js')});await slide.locator('[data-next]').click();assert.equal(await slide.locator('[data-position]').innerText(),'2 / 2');await slide.keyboard.press('ArrowRight');assert.equal(await slide.locator('[data-position]').innerText(),'1 / 2');await slide.locator('.photo-slider').evaluate(el=>{el.dispatchEvent(new TouchEvent('touchstart',{touches:[new Touch({identifier:1,target:el,clientX:260,clientY:100})]}));el.dispatchEvent(new TouchEvent('touchend',{changedTouches:[new Touch({identifier:1,target:el,clientX:100,clientY:105})]}));});assert.equal(await slide.locator('[data-position]').innerText(),'2 / 2');await slide.locator('.photo-slider').evaluate(el=>{el.dispatchEvent(new TouchEvent('touchstart',{touches:[new Touch({identifier:2,target:el,clientX:200,clientY:100})]}));el.dispatchEvent(new TouchEvent('touchend',{changedTouches:[new Touch({identifier:2,target:el,clientX:180,clientY:300})]}));});assert.equal(await slide.locator('[data-position]').innerText(),'2 / 2');await slide.emulateMedia({reducedMotion:'reduce'});assert.equal(await slide.locator('.slide:visible').evaluate(e=>getComputedStyle(e).animationName),'none');await slide.close();console.log('PASS isolated carousel controls, keyboard, synthetic horizontal/vertical touch, reduced motion');
  report.result='PASS';fs.writeFileSync(path.join(ROOT,'docs','qa-results.json'),JSON.stringify(report,null,2));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
