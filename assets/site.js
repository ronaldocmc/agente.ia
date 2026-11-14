const root=document.documentElement.dataset.root||'';const si=document.getElementById('search'), sr=document.getElementById('search-results');let index=[];fetch(root+'assets/search.json').then(r=>r.json()).then(d=>index=d).catch(()=>{});si?.addEventListener('input',()=>{let q=si.value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();if(!q){sr&&(sr.style.display='none');return}let matches=index.filter(x=>x.title.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().includes(q)).slice(0,16);sr.replaceChildren();matches.forEach(x=>{let a=document.createElement('a');a.href=root+x.url;a.textContent=x.title;let sub=document.createElement('em');sub.textContent=x.type;a.append(sub);sr.append(a)});sr.style.display='block';});document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();const b=document.querySelector('.menu-btn');if(b?.getAttribute('aria-expanded')==='false')b.click();si?.focus()}if(e.key==='Escape')sr&&(sr.style.display='none')});document.addEventListener('click',e=>{if(si&&sr&&!si.contains(e.target)&&!sr.contains(e.target))sr&&(sr.style.display='none')});

// Navegação lateral única em desktop e mobile, com preferência local.
(()=>{
  const nav=document.querySelector('.nav');
  const button=document.querySelector('.menu-btn');
  if(!nav||!button)return;
  const MOBILE=760;
  const storageKey='agenteia.menu.recolhido';
  const mobile=()=>window.innerWidth<=MOBILE;
  let desktopCollapsed=false;
  try{desktopCollapsed=localStorage.getItem(storageKey)==='1';}catch(e){}
  function render(){
    if(mobile()){
      document.body.classList.remove('nav-collapsed');
      const opened=nav.classList.contains('open');
      button.setAttribute('aria-expanded',String(opened));
      button.setAttribute('aria-label',opened?'Fechar navegação':'Abrir navegação');
    }else{
      nav.classList.remove('open');
      document.body.classList.toggle('nav-collapsed',desktopCollapsed);
      button.setAttribute('aria-expanded',String(!desktopCollapsed));
      button.setAttribute('aria-label',desktopCollapsed?'Expandir menu lateral':'Recolher menu lateral');
    }
    button.title=button.getAttribute('aria-label');
  }
  button.addEventListener('click',()=>{
    if(mobile())nav.classList.toggle('open');
    else{
      desktopCollapsed=!desktopCollapsed;
      try{localStorage.setItem(storageKey,desktopCollapsed?'1':'0');}catch(e){}
    }
    render();
  });
  document.addEventListener('keydown',event=>{
    if(event.key==='Escape'&&mobile()&&nav.classList.contains('open')){
      nav.classList.remove('open');render();button.focus();
    }
  });
  document.addEventListener('click',event=>{
    if(mobile()&&nav.classList.contains('open')&&!nav.contains(event.target)&&!button.contains(event.target)){
      nav.classList.remove('open');render();
    }
  });
  nav.addEventListener('click',event=>{
    if(mobile()&&event.target.closest('a')){nav.classList.remove('open');render();}
  });
  window.addEventListener('resize',render);
  render();
})();
