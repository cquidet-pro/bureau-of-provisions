// Fixed photographic view: two still straw positions, static spout, animated mist.
const prototype = document.querySelector('[data-drinking-prototype]');
if (prototype) {
  const options = {
    straw: {title:'01 / Straw. A proper sip.', description:'Lift the folding straw for an upright sip, then fold it flat beneath the clear hood. Choose Flat or Up to see both positions.', action:'Unfold. Sip. Fold away.', detail:'Folding stainless steel straw', ready:'Flat. Folded away.'},
    gulp: {title:'02 / Spout. A big gulp.', description:'Tilt the bottle and drink directly through the wide stainless steel spout. A larger opening for a fuller mouthful.', action:'Tilt to drink', detail:'Wide stainless steel drinking spout', ready:'Tilt to drink.'},
    spray: {title:'03 / Spray. A little weather.', description:'Press the rear-centre spray head to release a fine cooling mist. Available with the optional mist lid.', action:'Press. Mist. Much better.', detail:'Rear-centre cooling spray head', ready:'Forecast: locally refreshing.'}
  };
  const find = selector => prototype.querySelector(selector);
  const play = find('[data-drinking-play]');
  const controls = find('.drinking-controls');
  const strawControls = find('[data-straw-positions]');
  const strawUp = find('[data-straw-up]');
  const particles = find('[data-drinking-particles]');
  const status = find('[data-drinking-status]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let method='straw', running=false, frame=0, started=0, lastEmission=0, drops=[];
  function strawPose(up) {
    strawUp.style.display=up?'':'none';
    prototype.dataset.strawPosition=up?'up':'flat';
    prototype.querySelectorAll('[data-straw-position]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.strawPosition===(up?'up':'flat'))));
    if(method==='straw') {
      find('[data-straw-leader]').setAttribute('d',up?'M180 940H340L435 875':'M180 940H350L430 965');
      status.textContent=up?'Up. Ready for a sip.':options.straw.ready;
    }
  }
  function stop(clear=false) {
    const wasRunning=running;
    running=false; prototype.classList.remove('is-running');
    play.setAttribute('aria-pressed','false'); play.textContent='Press to mist.';
    if(clear||reducedMotion.matches) {
      cancelAnimationFrame(frame); frame=0; particles.replaceChildren(); drops=[];
    }
    if(wasRunning) status.textContent='Mist finished. Press to mist again.';
  }
  function emit(now,progress) {
    const node=document.createElementNS('http://www.w3.org/2000/svg','circle');
    const drop={node,born:now,life:650+Math.random()*450,spread:(Math.random()-.5)*210,reach:190+Math.random()*160};
    node.setAttribute('r',1.4+Math.random()*2.8); node.setAttribute('fill','#f5ffff');
    node.setAttribute('stroke','#dbfaff'); node.setAttribute('stroke-width','.25');
    particles.append(node); drops.push(drop);
    if(progress!==undefined) drop.born=now-progress*drop.life;
  }
  function position(drop,now) {
    const t=Math.min(1,(now-drop.born)/drop.life);
    drop.node.setAttribute('cx',642+drop.reach*.8*t);
    drop.node.setAttribute('cy',720-drop.reach*.6*t+drop.spread*.6*t*t);
    drop.node.setAttribute('opacity',Math.sin(Math.PI*t)*.8);
    return t<1;
  }
  function tick(now) {
    frame=0;
    if(running&&now-started>=2600) stop();
    if(running) {
      lastEmission=Math.max(lastEmission,now-80);
      while(now-lastEmission>=10){lastEmission+=10;emit(lastEmission);}
    }
    drops=drops.filter(drop=>{if(position(drop,now))return true;drop.node.remove();return false;});
    if(running||drops.length)frame=requestAnimationFrame(tick);
  }
  function startMist() {
    if(method!=='spray')return;
    stop(true);running=true;started=lastEmission=performance.now();
    prototype.classList.add('is-running');play.setAttribute('aria-pressed','true');play.textContent='Stop mist';
    status.textContent='Cooling mist leaves the separate rear outlet.';
    if(reducedMotion.matches) {
      for(let i=0;i<25;i++)emit(started,(i+.5)/25);
      drops.forEach(drop=>position(drop,started));
      frame=requestAnimationFrame(function end(now){if(now-started>=2600)stop(true);else frame=requestAnimationFrame(end);});
    }else frame=requestAnimationFrame(tick);
  }
  function select(next) {
    stop(true);method=next;const item=options[method];prototype.dataset.method=method;
    prototype.querySelectorAll('[data-drinking-method],[data-drinking-part]').forEach(button=>button.setAttribute('aria-pressed',String((button.dataset.drinkingMethod||button.dataset.drinkingPart)===method)));
    find('[data-drinking-title]').textContent=item.title;find('[data-drinking-description]').textContent=item.description;
    find('[data-drinking-action]').textContent=item.action;find('[data-drinking-detail]').textContent=item.detail;
    find('.drinking-closeup').setAttribute('aria-label',`Overhead lid study highlighting ${item.detail.toLowerCase()}.`);
    controls.hidden=method==='gulp';strawControls.hidden=method!=='straw';play.hidden=method!=='spray';status.hidden=method==='gulp';
    strawPose(false);status.textContent=item.ready;
  }
  prototype.querySelectorAll('[data-drinking-method],[data-drinking-part]').forEach(button=>button.addEventListener('click',()=>select(button.dataset.drinkingMethod||button.dataset.drinkingPart)));
  prototype.querySelectorAll('[data-straw-position]').forEach(button=>button.addEventListener('click',()=>strawPose(button.dataset.strawPosition==='up')));
  play.addEventListener('click',()=>running?stop(true):startMist());
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop(true);});
  reducedMotion.addEventListener('change',()=>stop(true));
  new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)stop(true);}).observe(prototype);
  select('straw');
}
