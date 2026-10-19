// Fixed photographic view: two still straw positions, static spout, animated mist.
const prototype = document.querySelector('[data-drinking-prototype]');
if (prototype) {
  const options = {
    straw: {title:'01 / Straw. A proper sip.', description:'Lift the folding straw for an upright sip, then fold it flat beneath the clear hood. Choose Flat or Up to see both positions.', action:'Unfold. Sip. Fold away.', detail:'Folding stainless steel straw', ready:'Flat. Folded away.'},
    gulp: {title:'02 / Spout. A big gulp.', description:'Tilt the bottle and drink directly through the wide stainless steel spout. A larger opening for a fuller mouthful.', action:'Tilt to drink', detail:'Wide stainless steel drinking spout', ready:'Tilt to drink.'},
    spray: {title:'03 / Spray. A little weather.', description:'Press once: the rear-centre spray head moves down and releases one short burst of cooling mist. It returns to rest while the droplets travel away. Available with the optional mist lid.', action:'Press. Mist. Much better.', detail:'Rear-centre cooling spray head', ready:'Forecast: locally refreshing.'}
  };
  const find = selector => prototype.querySelector(selector);
  const play = find('[data-drinking-play]');
  const controls = find('.drinking-controls');
  const strawControls = find('[data-straw-positions]');
  const strawUp = find('[data-straw-up]');
  const particles = find('[data-drinking-particles]');
  const status = find('[data-drinking-status]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const pressedHead = find('[data-mist-pressed]');
  const pump = {down:140, burstEnd:280, returned:500, count:240, x:666, y:792};
  let method='straw', pumping=false, frame=0, pumpStarted=null, drops=[];
  let releaseTimer, clearTimer;
  function headPose(amount, phase) {
    pressedHead.setAttribute('opacity',String(amount));
    prototype.dataset.pumpPhase=phase;
  }
  function releasePump() {
    pumping=false; pumpStarted=null;
    headPose(0,'resting');
    prototype.classList.remove('is-running');
    play.disabled=false; play.removeAttribute('aria-busy');
  }
  function strawPose(up) {
    strawUp.style.display=up?'':'none';
    prototype.dataset.strawPosition=up?'up':'flat';
    prototype.querySelectorAll('[data-straw-position]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.strawPosition===(up?'up':'flat'))));
    if(method==='straw') {
      find('[data-straw-leader]').setAttribute('d',up?'M180 940H340L435 875':'M180 940H350L430 965');
      status.textContent=up?'Up. Ready for a sip.':options.straw.ready;
    }
  }
  function stop() {
    clearTimeout(releaseTimer); clearTimeout(clearTimer);
    cancelAnimationFrame(frame); frame=0;
    particles.replaceChildren(); drops=[];
    releasePump();
  }
  function emit(born) {
    const node=document.createElementNS('http://www.w3.org/2000/svg','circle');
    const drop={node,born,life:800+Math.random()*500,spread:(Math.random()-.5)*125,reach:240+Math.random()*140};
    node.setAttribute('r',1.3+Math.random()*2.1);
    node.setAttribute('fill','#dff2f8'); node.setAttribute('stroke','#86acb7'); node.setAttribute('stroke-width','.55');
    node.setAttribute('opacity','0');
    particles.append(node); drops.push(drop);
    return drop;
  }
  function position(drop,now) {
    const age=now-drop.born;
    if(age<0) return true;
    const t=Math.min(1,age/drop.life);
    // One finite pulse leaves the side outlet, aimed toward the 03 Spray label.
    const travel=1-Math.pow(1-t,1.35);
    drop.node.setAttribute('cx',pump.x+drop.reach*.95*travel);
    drop.node.setAttribute('cy',pump.y-drop.reach*.34*travel+drop.spread*t+12*t*t);
    drop.node.setAttribute('opacity',Math.min(1,age/55)*Math.pow(1-t,1.2)*.85);
    return t<1;
  }
  function tick(now) {
    frame=0;
    if(pumpStarted!==null) {
      const elapsed=now-pumpStarted;
      if(elapsed<pump.down) headPose(elapsed/pump.down,'pressing');
      else if(elapsed<pump.burstEnd) headPose(1,'pressed');
      else if(elapsed<pump.returned) headPose(1-(elapsed-pump.burstEnd)/(pump.returned-pump.burstEnd),'returning');
      else {
        releasePump();
        status.textContent='Back at rest. The droplets continue away.';
      }
    }
    drops=drops.filter(drop=>{if(position(drop,now))return true;drop.node.remove();return false;});
    if(pumping||drops.length) frame=requestAnimationFrame(tick);
    else status.textContent='One burst finished. Press to mist again.';
  }
  function startMist() {
    if(method!=='spray'||pumping) return;
    pumping=true; pumpStarted=performance.now();
    prototype.classList.add('is-running');
    play.disabled=true; play.setAttribute('aria-busy','true');
    status.textContent='One press. One short burst of mist.';
    if(reducedMotion.matches) {
      headPose(1,'pressed');
      for(let i=0;i<24;i++) {
        const drop=emit(pumpStarted);
        position(drop,pumpStarted+drop.life*(.15+i/48));
      }
      releaseTimer=setTimeout(()=>{
        headPose(0,'resting');
        status.textContent='Back at rest. One mist burst.';
      },400);
      clearTimer=setTimeout(()=>{stop();status.textContent='One burst finished. Press to mist again.';},1000);
      return;
    }
    headPose(0,'pressing');
    // The full emission schedule is fixed by this click; no continuing emitter.
    for(let i=0;i<pump.count;i++) emit(pumpStarted+pump.down+i*(pump.burstEnd-pump.down)/pump.count);
    if(!frame) frame=requestAnimationFrame(tick);
  }
  function select(next) {
    stop();method=next;const item=options[method];prototype.dataset.method=method;
    prototype.querySelectorAll('[data-drinking-method],[data-drinking-part]').forEach(button=>button.setAttribute('aria-pressed',String((button.dataset.drinkingMethod||button.dataset.drinkingPart)===method)));
    find('[data-drinking-title]').textContent=item.title;find('[data-drinking-description]').textContent=item.description;
    find('[data-drinking-action]').textContent=item.action;find('[data-drinking-detail]').textContent=item.detail;
    find('.drinking-closeup').setAttribute('aria-label',`Overhead lid study highlighting ${item.detail.toLowerCase()}.`);
    controls.hidden=method==='gulp';strawControls.hidden=method!=='straw';play.hidden=method!=='spray';status.hidden=method==='gulp';
    strawPose(false);status.textContent=item.ready;
  }
  prototype.querySelectorAll('[data-drinking-method],[data-drinking-part]').forEach(button=>button.addEventListener('click',()=>select(button.dataset.drinkingMethod||button.dataset.drinkingPart)));
  prototype.querySelectorAll('[data-straw-position]').forEach(button=>button.addEventListener('click',()=>strawPose(button.dataset.strawPosition==='up')));
  play.addEventListener('click',startMist);
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});
  reducedMotion.addEventListener('change',()=>stop());
  new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)stop();}).observe(prototype);
  select('straw');
}
