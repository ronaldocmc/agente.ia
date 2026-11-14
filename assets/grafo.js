(()=>{
'use strict';
const raw=window.WIKI_GRAFO;
if(!raw || !Array.isArray(raw.nodes)) return;
const $=id=>document.getElementById(id),svg=$('knowledgeGraph'),camera=$('gCamera'),gLinks=$('gLinks'),gNodes=$('gNodes'),detail=$('gDetail'),layout=document.querySelector('.map-layout');
if(!svg||!camera||!layout) return;
const byId=Object.fromEntries(raw.nodes.map(n=>[n.id,n]));
const links=raw.edges||[];
const TECH_PATHS = {"t:n8n":{"role":"Automação visual e gatilhos; pode acionar um nó de agente, mas não deve executar decisões institucionais sem validação.","lab":"lab-n8n-detalhado.html","labTitle":"Laboratório n8n guiado","extra":[["Agente n8n + Ollama com ferramenta","laboratorio-n8n-ollama-agente.html"]],"concept":"automacao-agentes.html","case":"aplicacoes-automacao.html","alternative":"decisao-orientada-a-problemas.html","deliverable":"Workflow importável, testes da consulta e registro de execução."},"t:openai-agents-sdk":{"role":"SDK Python para criar agentes, tools e handoffs; Runner executa o ciclo do agente, enquanto a aplicação controla autenticação e autorização.","lab":"lab-agents-sdk.html","labTitle":"Laboratório Agents SDK Python","extra":[["Roteiro complementar","pratica-agents-passo-a-passo.html"]],"concept":"skills.html","case":"escritorio-virtual-decisao.html","alternative":"decisao-tecnologica-detalhada.html","deliverable":"Agente Python com function tools, avaliação de chamadas e tratamento de erros."},"t:langgraph":{"role":"Orquestra estados, transições, interrupções e retomadas; útil quando o processo precisa pausar para aprovação.","lab":"lab-langgraph-detalhado.html","labTitle":"Laboratório LangGraph com estado","extra":[["Laboratório comparativo","laboratorio-langgraph-passo-a-passo.html"]],"concept":"arquitetura.html","case":"escritorio-virtual-decisao.html","alternative":"decisao-tecnologica-detalhada.html","deliverable":"Grafo executável com estados definidos e testes de transições."},"t:crewai":{"role":"Coordenação de especialistas por papéis e tarefas; atenção a custo e qualidade na delegação.","lab":"laboratorio-crewai-passo-a-passo.html","labTitle":"Laboratório CrewAI","extra":[],"concept":"arquitetura.html","case":"casos-integrados.html","alternative":"decisao-tecnologica-detalhada.html","deliverable":"Equipe de agentes com tarefas delimitadas e comparação com solução direta."},"t:hermes-agent":{"role":"Runtime de assistente extensível com memória, terminal e skills; permissões e ambiente de execução precisam ser isolados.","lab":"lab-hermes-detalhado.html","labTitle":"Laboratório Hermes Agent","extra":[["Roteiro alternativo","pratica-hermes-passo-a-passo.html"]],"concept":"skills.html","case":"estudos/assistente-pessoal.html","alternative":"decisao-tecnologica-detalhada.html","deliverable":"Skill de consulta com teste em ambiente de demonstração."},"t:openclaw":{"role":"Gateway e runtime de assistentes persistentes com sessões, canais, skills e ferramentas.","lab":"lab-openclaw-detalhado.html","labTitle":"Laboratório OpenClaw","extra":[["Roteiro complementar","pratica-openclaw-passo-a-passo.html"]],"concept":"skills.html","case":"escritorio-virtual-decisao.html","alternative":"decisao-tecnologica-detalhada.html","deliverable":"Assistente em ambiente isolado com skill autorizada e log de execução."},"t:grok-bot":{"role":"Plataforma gerenciada para Bots especializados, delegação e rotinas; os recursos dependem da conta e da versão.","lab":"lab-grok-detalhado.html","labTitle":"Laboratório Grok Bot","extra":[["Equipes e segundo cérebro","laboratorio-grok.html"]],"concept":"agentes-construtores.html","case":"caso-plataforma-base.html","alternative":"comparador-iniciantes.html","deliverable":"Equipe de Bots de demonstração com plano de tarefas e aprovação humana."},"t:ollama":{"role":"Servidor local de modelos. Não orquestra agentes sozinho: fornece inferência a aplicações ou frameworks.","lab":"laboratorio-n8n-ollama-agente.html","labTitle":"Laboratório n8n + Ollama","extra":[["Primeiro agente em Python","primeiro-agente.html"]],"concept":"ecossistema-tecnologias.html","case":"escritorio-virtual-decisao.html","alternative":"decisao-orientada-a-problemas.html","deliverable":"Modelo local atendendo consultas e chamadas de ferramenta mediadas por uma aplicação."},"t:google-adk":{"role":"SDK para desenvolver agentes por código e integrar ferramentas, modelos e workflows.","lab":"laboratorios-completos.html","labTitle":"Índice de laboratórios — sem roteiro ADK validado","extra":[],"concept":"ecossistema-tecnologias.html","case":"escritorio-virtual-decisao.html","alternative":"decisao-tecnologica-detalhada.html","deliverable":"Selecionar um laboratório de base e adaptar o fluxo para ADK após validar a versão."}};
const colors={tecnologia:'#138b91',categoria:'#284e6b',conceito:'#ad771d',estudo:'#6d4d9a',laboratorio:'#aa4f69',roadmap:'#448b52',caso:'#865b9b'};
const core=['ollama','openclaw','hermes-agent','crewai','langgraph','n8n','openai-agents-sdk','google-adk','mcp','pgvector','dots-openai','grok-bot','flowise','pydanticai','qdrant','claude-agent-sdk','fastapi','postgresql'];
const labs=['n8n','agents sdk','langgraph','hermes','openclaw','grok','primeiro agente','crewai'];
const W=1120,H=780;
let zoom=1,panX=0,panY=0,selected=null,positions={},drag=null,drawnNodes=[];
let fullscreen=false;let filtersOpen=false;
let layoutCache={key:'',positions:{}};
let collapsedCats=new Set();
let focusedTechnology=null;let explorerOpen=false;let detailOpen=true;
const countTechnologies=raw.nodes.filter(n=>n.kind==='tecnologia').length;
const cats=raw.nodes.filter(n=>n.kind==='categoria'&&n.id.startsWith('cat:'));
for(const cat of cats.sort((a,b)=>a.label.localeCompare(b.label,'pt'))){const o=document.createElement('option');o.value=cat.id;o.textContent=cat.label;$('gCategory').append(o);}

function candidateNodes(ignoreKind=false){
 const q=$('gSearch').value.trim().toLocaleLowerCase(),kind=$('gKind').value,full=$('gFull').checked,cat=$('gCategory').value;
 return raw.nodes.filter(n=>{
  const label=n.label.toLocaleLowerCase();
  const hit=!q||(label+' '+(n.cat||'')+' '+(n.summary||'')).toLocaleLowerCase().includes(q);
  const featured=n.id.startsWith('didatico:')||n.kind==='categoria'&&n.id.startsWith('didatico:')||
    (n.kind==='tecnologia'&&core.some(v=>n.id.toLowerCase().includes(v)))||
    (n.kind==='laboratorio'&&labs.some(v=>label.includes(v)))||n.kind==='caso'||n.kind==='estudo'&&/escritório|observar/i.test(n.label);
  return (full||q||featured||cat!=='all')&&hit&&(ignoreKind||kind==='all'||n.kind===kind)&&(cat==='all'||n.catId===cat||n.id===cat);
 });
}
function visible(){
 return candidateNodes(false);
}
function applyDidacticBranches(nodes,edges){
 if($('gLayout').value!=='didatico' || !collapsedCats.size) return {nodes,edges};
 const map=Object.fromEntries(nodes.map(n=>[n.id,n]));
 const neighbors={};
 edges.forEach(e=>{if(map[e.source]&&map[e.target]){(neighbors[e.source]??=[]).push(e.target);(neighbors[e.target]??=[]).push(e.source);}});
 const visibleIds=new Set();
 nodes.forEach(n=>{
   if(n.kind==='tecnologia'){
     if(!(n.catId && collapsedCats.has(n.catId))) visibleIds.add(n.id);
   }else if(n.kind==='categoria' || n.kind==='conceito' || n.kind==='roadmap'){
     visibleIds.add(n.id);
   }
 });
 let changed=true;
 while(changed){
   changed=false;
   nodes.forEach(n=>{
     if(visibleIds.has(n.id)) return;
     if(n.kind==='tecnologia') return;
     const ok=(neighbors[n.id]||[]).some(id=>visibleIds.has(id));
     if(ok){visibleIds.add(n.id);changed=true;}
   });
 }
 const filteredNodes=nodes.filter(n=>visibleIds.has(n.id));
 const ids=new Set(filteredNodes.map(n=>n.id));
 const filteredEdges=edges.filter(e=>ids.has(e.source)&&ids.has(e.target));
 return {nodes:filteredNodes,edges:filteredEdges};
}
function categoriesForDidacticPanel(){
 const candidates=candidateNodes(true).filter(n=>n.kind==='tecnologia');
 const counts={};candidates.forEach(t=>{if(t.catId)counts[t.catId]=(counts[t.catId]||0)+1;});
 return raw.nodes.filter(n=>n.kind==='categoria' && n.id.startsWith('cat:') && counts[n.id]).sort((a,b)=>a.label.localeCompare(b.label,'pt')).map(node=>({node,count:counts[node.id]}));
}
function renderDidacticPanel(){ /* categorias disponíveis no Explorador de tecnologias */ }

const EXPLORE_LABELS={
 'memoria-rag':'RAG, busca e recuperação',
 'memoria-persistencia':'Memória, vetores e armazenamento',
 'modelos':'Modelos e inferência',
 'automacao':'Automação e workflows',
 'sdk':'SDKs programáveis',
 'orquestracao':'Orquestração e multiagentes',
 'runtime':'Runtimes e assistentes',
 'protocolo':'Protocolos e integrações',
 'interface':'Interfaces, canais e multimodalidade',
 'infra':'Infraestrutura, segurança e avaliação',
 'outros':'Outras tecnologias'
};
function exploreGroup(n){
 const cat=(byId[n.catId]?.label||'').toLowerCase();const t=n.label.toLowerCase();
 if(/rag|memória|vetor|embedding|banco|dados/.test(cat)){
   return /rag|retriev|busca|embedding|index|search|rerank|haystack|llamaindex/i.test(t)?'memoria-rag':'memoria-persistencia';
 }
 if(/modelo|llm|inferência|roteamento de modelos/i.test(cat))return 'modelos';
 if(/automação|workflow|orquestração visual/i.test(cat))return 'automacao';
 if(/sdk|agentes programáveis/i.test(cat))return 'sdk';
 if(/multiagente|framework|coordenação/i.test(cat))return 'orquestracao';
 if(/runtime|assistente|plataforma pronta/i.test(cat))return 'runtime';
 if(/protocolo|interop|api/i.test(cat))return 'protocolo';
 if(/interface|métrica|multimodal|canais/i.test(cat))return 'interface';
 if(/infraestrutura|segurança|governança|observabilidade/i.test(cat))return 'infra';
 return 'outros';
}
function openExplorer(on){
 explorerOpen=on;const panel=$('gExplorer');panel.hidden=!on;
 $('gExploreToggle').setAttribute('aria-expanded',String(on));
 $('gExploreToggle').textContent=on?'✕ Fechar explorador':'⌕ Explorar tecnologias';
 if(on){renderExplorer();$('gExploreSearch').focus();}
}
function renderExplorer(){
 const wrap=$('gExploreItems');wrap.replaceChildren();
 const q=$('gExploreSearch').value.toLocaleLowerCase().trim();
 const nodes=raw.nodes.filter(n=>n.kind==='tecnologia'&&(!q||(n.label+' '+(byId[n.catId]?.label||'')).toLocaleLowerCase().includes(q)));
 $('gExploreStatus').textContent=`${nodes.length} de ${countTechnologies} tecnologias`;
 const grouped={};nodes.forEach(n=>(grouped[exploreGroup(n)]??=[]).push(n));
 for(const [key,label] of Object.entries(EXPLORE_LABELS)){
   const arr=(grouped[key]||[]).sort((a,b)=>a.label.localeCompare(b.label,'pt'));
   if(!arr.length)continue;
   const box=document.createElement('details');box.className='explore-category';box.open=Boolean(q)||key==='sdk'||key==='runtime';
   const summary=document.createElement('summary');summary.textContent=`${label} (${arr.length})`;box.append(summary);
   const list=document.createElement('div');list.className='explore-tech-list';
   arr.forEach(n=>{const btn=document.createElement('button');btn.type='button';btn.className='explore-tech'+(focusedTechnology===n.id?' active':'');btn.textContent=n.label;
     btn.addEventListener('click',()=>{
       focusedTechnology=n.id;selected=n.id;layoutCache={key:'',positions:{}};
       $('gSearch').value='';$('gKind').value='all';$('gCategory').value='all';collapsedCats.clear();
       draw(true);select(n.id);openExplorer(false);setDetail(true);
     });list.append(btn);
   });box.append(list);wrap.append(box);
 }
 if(!nodes.length){const p=document.createElement('p');p.className='explore-empty';p.textContent='Nenhuma tecnologia encontrada. Experimente outro termo.';wrap.append(p);}
}
function setDetail(on){
 detailOpen=on;layout.classList.toggle('detail-collapsed',!on);$('gDetailToggle').setAttribute('aria-expanded',String(on));
 $('gDetailToggle').textContent=on?'◧ Ocultar detalhes':'◨ Mostrar detalhes';$('gDetailReopen').hidden=on;
}
function elem(tag,attrs){const e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));return e;}
function seeded(seed){let s=seed>>>0;return()=>((s=(1664525*s+1013904223)>>>0)/4294967296);}
function hash(str){let h=2166136261;for(let i=0;i<str.length;i++){h^=str.charCodeAt(i);h=Math.imul(h,16777619);}return h>>>0;}
function kindOrder(kind){return ({categoria:0,conceito:1,tecnologia:2,laboratorio:3,estudo:4,caso:5,roadmap:6})[kind]??7;}

function didacticHierarchyLayout(nodes,edges){
 const p={};
 const categories=nodes.filter(n=>n.kind==='categoria').sort((a,b)=>a.label.localeCompare(b.label,'pt'));
 const concepts=nodes.filter(n=>n.kind==='conceito').sort((a,b)=>a.label.localeCompare(b.label,'pt'));
 const techs=nodes.filter(n=>n.kind==='tecnologia').sort((a,b)=>a.label.localeCompare(b.label,'pt'));
 const labs=nodes.filter(n=>n.kind==='laboratorio').sort((a,b)=>a.label.localeCompare(b.label,'pt'));
 const studies=nodes.filter(n=>n.kind==='estudo').sort((a,b)=>a.label.localeCompare(b.label,'pt'));
 const cases=nodes.filter(n=>n.kind==='caso').sort((a,b)=>a.label.localeCompare(b.label,'pt'));
 const roadmaps=nodes.filter(n=>n.kind==='roadmap').sort((a,b)=>a.label.localeCompare(b.label,'pt'));
 const others=nodes.filter(n=>!['categoria','conceito','tecnologia','laboratorio','estudo','caso','roadmap'].includes(n.kind));
 const edgeMap={};
 edges.forEach(e=>{(edgeMap[e.source]??=[]).push(e.target);(edgeMap[e.target]??=[]).push(e.source);});
 const x={roadmap:70,categoria:170,conceito:390,tecnologia:620,laboratorio:860,aplicacao:1080};
 // 1) technologies grouped by category to form the main trunk of the hierarchy
 const catGroups=[];
 const categoryVisibleIds=new Set(categories.map(n=>n.id));
 const grouped={}; techs.forEach(t=>{const key=t.catId && categoryVisibleIds.has(t.catId)?t.catId:'__sem_categoria__';(grouped[key]??=[]).push(t);});
 categories.forEach(c=>{if(grouped[c.id]?.length) catGroups.push({id:c.id,node:c,items:grouped[c.id].sort((a,b)=>a.label.localeCompare(b.label,'pt'))});});
 if(grouped['__sem_categoria__']?.length){catGroups.push({id:'__sem_categoria__',node:{id:'__sem_categoria__',label:'Outras tecnologias',kind:'categoria'},items:grouped['__sem_categoria__'].sort((a,b)=>a.label.localeCompare(b.label,'pt'))});}
 let y=90;
 catGroups.forEach(group=>{
   const startY=y;
   group.items.forEach((t,i)=>{p[t.id]={x:x.tecnologia,y};y+=46;});
   const endY=y-46;
   p[group.id]={x:x.categoria,y:(startY+endY)/2};
   y+=34;
 });
 // remaining categories without visible technologies
 categories.filter(c=>!p[c.id]).forEach((c,i)=>{p[c.id]={x:x.categoria,y:y+i*48};});
 // 2) concepts positioned by the average of their linked technologies/categories/labs
 const conceptPlaced=[];
 concepts.forEach((c,idx)=>{
   const ys=(edgeMap[c.id]||[]).map(id=>p[id]?.y).filter(v=>typeof v==='number');
   const avg=ys.length?ys.reduce((a,b)=>a+b,0)/ys.length:110+idx*54;
   conceptPlaced.push({node:c,avg});
 });
 conceptPlaced.sort((a,b)=>a.avg-b.avg||a.node.label.localeCompare(b.node.label,'pt'));
 let lastY=60;
 conceptPlaced.forEach(({node,avg})=>{lastY=Math.max(lastY+44,avg);p[node.id]={x:x.conceito,y:lastY};});
 // 3) roadmaps left of concepts/categories
 roadmaps.forEach((r,idx)=>{
   const ys=(edgeMap[r.id]||[]).map(id=>p[id]?.y).filter(v=>typeof v==='number');
   const avg=ys.length?ys.reduce((a,b)=>a+b,0)/ys.length:120+idx*52;
   p[r.id]={x:x.roadmap,y:avg};
 });
 // 4) labs to the right, anchored by linked technologies/concepts
 const labPlaced=[];
 labs.forEach((l,idx)=>{
   const ys=(edgeMap[l.id]||[]).map(id=>p[id]?.y).filter(v=>typeof v==='number');
   const avg=ys.length?ys.reduce((a,b)=>a+b,0)/ys.length:140+idx*50;
   labPlaced.push({node:l,avg});
 });
 labPlaced.sort((a,b)=>a.avg-b.avg||a.node.label.localeCompare(b.node.label,'pt'));
 lastY=70;
 labPlaced.forEach(({node,avg})=>{lastY=Math.max(lastY+42,avg);p[node.id]={x:x.laboratorio,y:lastY};});
 // 5) studies and cases at the far right, anchored by linked labs/techs/concepts
 const appNodes=[...studies,...cases,...others];
 const appPlaced=[];
 appNodes.forEach((n,idx)=>{
   const ys=(edgeMap[n.id]||[]).map(id=>p[id]?.y).filter(v=>typeof v==='number');
   const avg=ys.length?ys.reduce((a,b)=>a+b,0)/ys.length:160+idx*54;
   appPlaced.push({node:n,avg});
 });
 appPlaced.sort((a,b)=>a.avg-b.avg||a.node.label.localeCompare(b.node.label,'pt'));
 lastY=90;
 appPlaced.forEach(({node,avg})=>{lastY=Math.max(lastY+44,avg);p[node.id]={x:x.aplicacao,y:lastY};});
 // 6) gentle horizontal jitter to avoid perfectly matrix-like columns while preserving hierarchy
 const jitter=(str,amp)=>((hash(str)%1000)/1000-0.5)*amp;
 Object.keys(p).forEach(id=>{
   const node=byId[id]||{};
   const ampX=node.kind==='tecnologia'?14:node.kind==='laboratorio'?10:node.kind==='conceito'?8:6;
   const ampY=node.kind==='tecnologia'?8:node.kind==='laboratorio'?6:5;
   p[id]={x:p[id].x+jitter(id+'x',ampX),y:p[id].y+jitter(id+'y',ampY)};
 });
 if($('gOrientation')?.value==='vertical'){
    Object.keys(p).forEach(id=>{const old=p[id];p[id]={x:old.y*1.30,y:old.x*1.05};});
 }
 return p;
}
function gridLayout(nodes,edges){
  return didacticHierarchyLayout(nodes,edges);
}
function radialLayout(nodes){
 const p={},cx=W/2,cy=H/2;
 const rings={categoria:100,conceito:210,tecnologia:320,laboratorio:420,estudo:500,caso:570,roadmap:640};
 const order=['categoria','conceito','tecnologia','laboratorio','estudo','caso','roadmap'];
 order.forEach(kind=>{
   const arr=nodes.filter(n=>n.kind===kind).sort((a,b)=>a.label.localeCompare(b.label,'pt'));
   const r=rings[kind]||350;if(!arr.length) return;
   arr.forEach((n,i)=>{
     const angle=(-Math.PI/2)+(Math.PI*2*i/arr.length)+(kindOrder(kind)*0.08);
     p[n.id]={x:cx+Math.cos(angle)*r,y:cy+Math.sin(angle)*r};
   });
 });
 return p;
}
function layeredLayout(nodes){
 const p={},layers={categoria:120,conceito:290,tecnologia:520,laboratorio:760,estudo:940,caso:940,roadmap:120};
 const order=['categoria','roadmap','conceito','tecnologia','laboratorio','estudo','caso'];
 order.forEach(kind=>{
   const arr=nodes.filter(n=>n.kind===kind).sort((a,b)=>a.label.localeCompare(b.label,'pt'));
   const x=layers[kind]||W/2; if(!arr.length) return;
   const rows=Math.ceil(arr.length/3);
   arr.forEach((n,i)=>{
     const col=i%3,row=Math.floor(i/3);
     p[n.id]={x:x+col*78-(arr.length>1?78:0),y:120+row*62};
   });
 });
 return p;
}
function categoriesLayout(nodes){
 const p={},cx=W/2,cy=H/2-10;
 const catNodes=nodes.filter(n=>n.kind==='categoria'&&n.id.startsWith('cat:')).sort((a,b)=>a.label.localeCompare(b.label,'pt'));
 const radius=Math.min(W,H)*0.34;
 catNodes.forEach((cat,i)=>{
   const angle=(-Math.PI/2)+2*Math.PI*i/Math.max(1,catNodes.length);
   const ax=cx+Math.cos(angle)*radius, ay=cy+Math.sin(angle)*radius;
   p[cat.id]={x:ax,y:ay};
   const tech=nodes.filter(n=>n.kind==='tecnologia'&&n.catId===cat.id).sort((a,b)=>a.label.localeCompare(b.label,'pt'));
   const localR=tech.length>20?95:tech.length>8?72:52;
   tech.forEach((n,j)=>{
     const a=(2*Math.PI*j/Math.max(1,tech.length));
     p[n.id]={x:ax+Math.cos(a)*localR,y:ay+Math.sin(a)*localR};
   });
 });
 const centerKinds=['conceito','laboratorio','estudo','caso','roadmap'];
 centerKinds.forEach((kind,idx)=>{
   const arr=nodes.filter(n=>n.kind===kind).sort((a,b)=>a.label.localeCompare(b.label,'pt'));
   const r=70+idx*58;
   arr.forEach((n,i)=>{
      const angle=(-Math.PI/2)+2*Math.PI*i/Math.max(1,arr.length)+idx*0.13;
      p[n.id]={x:cx+Math.cos(angle)*r,y:cy+Math.sin(angle)*r};
   });
 });
 // uncategorized technologies
 const otherTech=nodes.filter(n=>n.kind==='tecnologia'&&!p[n.id]).sort((a,b)=>a.label.localeCompare(b.label,'pt'));
 otherTech.forEach((n,i)=>{p[n.id]={x:90+(i%5)*95,y:H-140+Math.floor(i/5)*40};});
 return p;
}
function organicLayout(nodes,edges){
 const p={},rand=seeded(nodes.reduce((a,n)=>a+hash(n.id),0));
 // deterministic start from radial-ish layout
 radialLayout(nodes);
 nodes.forEach((n,i)=>{p[n.id]={x:W*(0.22+0.56*rand()),y:H*(0.18+0.64*rand()),vx:0,vy:0};});
 const nodeIds=nodes.map(n=>n.id);
 const area=W*H, k=Math.sqrt(area/Math.max(1,nodes.length))*0.46;
 for(let iter=0;iter<180;iter++){
   const disp={}; nodeIds.forEach(id=>disp[id]={x:0,y:0});
   for(let i=0;i<nodeIds.length;i++){
     const a=p[nodeIds[i]];
     for(let j=i+1;j<nodeIds.length;j++){
       const b=p[nodeIds[j]];
       let dx=a.x-b.x, dy=a.y-b.y, dist=Math.hypot(dx,dy)||0.01;
       const force=(k*k)/dist;
       dx/=dist; dy/=dist;
       disp[nodeIds[i]].x += dx*force; disp[nodeIds[i]].y += dy*force;
       disp[nodeIds[j]].x -= dx*force; disp[nodeIds[j]].y -= dy*force;
     }
   }
   edges.forEach(e=>{
     const a=p[e.source], b=p[e.target]; if(!a||!b) return;
     let dx=a.x-b.x, dy=a.y-b.y, dist=Math.hypot(dx,dy)||0.01;
     const force=(dist*dist)/k*0.0019;
     dx/=dist; dy/=dist;
     disp[e.source].x -= dx*force; disp[e.source].y -= dy*force;
     disp[e.target].x += dx*force; disp[e.target].y += dy*force;
   });
   nodes.forEach(n=>{
     const d=disp[n.id], anchorBias=n.kind==='categoria'?0.10:n.kind==='tecnologia'?0.04:0.07;
     const targetY=H/2 + (kindOrder(n.kind)-3)*50;
     p[n.id].x += Math.max(-16,Math.min(16,d.x*0.01));
     p[n.id].y += Math.max(-16,Math.min(16,d.y*0.01)) + (targetY-p[n.id].y)*anchorBias*0.015;
     p[n.id].x=Math.max(40,Math.min(W-40,p[n.id].x));
     p[n.id].y=Math.max(40,Math.min(H-40,p[n.id].y));
   });
 }
 const out={}; nodes.forEach(n=>out[n.id]={x:p[n.id].x,y:p[n.id].y});
 return out;
}
function layoutPositions(nodes,edges){
 const mode=$('gLayout').value;
 if(mode==='radial') return radialLayout(nodes);
 if(mode==='camadas') return layeredLayout(nodes);
 if(mode==='categorias') return categoriesLayout(nodes);
 if(mode==='organico') return organicLayout(nodes,edges);
 return gridLayout(nodes,edges);
}

function drawingArea(){
 if(focusedTechnology){
   const ids=new Set([focusedTechnology]);
   const n=byId[focusedTechnology];if(n?.catId)ids.add(n.catId);
   links.forEach(e=>{if(e.source===focusedTechnology)ids.add(e.target);if(e.target===focusedTechnology)ids.add(e.source);});
   const nodes=raw.nodes.filter(n=>ids.has(n.id));
   return {nodes,edges:links.filter(e=>ids.has(e.source)&&ids.has(e.target))};
 }
 const nodes=visible(),ids=new Set(nodes.map(n=>n.id));
 let area={nodes,edges:links.filter(e=>ids.has(e.source)&&ids.has(e.target))};
 return applyDidacticBranches(area.nodes,area.edges);
}
function getPositions(nodes,edges){
 const key=$('gLayout').value+'|'+($('gOrientation')?.value||'horizontal')+'|'+Array.from(collapsedCats).sort().join(',')+'|'+nodes.map(n=>n.id).sort().join('|');
 if(layoutCache.key!==key){layoutCache={key,positions:layoutPositions(nodes,edges)};}
 return layoutCache.positions;
}
function draw(doFit=false){
 renderDidacticPanel();
 const {nodes,edges}=drawingArea();drawnNodes=nodes;positions=getPositions(nodes,edges);
 gLinks.replaceChildren();gNodes.replaceChildren();
 const visibleEdges=selected?edges.filter(e=>e.source===selected||e.target===selected):edges;
 if($('gEdges').checked)visibleEdges.forEach(e=>{
  const a=positions[e.source],b=positions[e.target];if(!a||!b)return;
  gLinks.append(elem('line',{x1:a.x,y1:a.y,x2:b.x,y2:b.y,class:'map-edge'+(selected?' focus':'')}));
 });
 const showLabels=nodes.length<=65||zoom>=1.1||Boolean($('gSearch').value.trim())||$('gLayout').value!=='organico';
 nodes.forEach(n=>{
  const p=positions[n.id];if(!p)return;
  const g=elem('g',{class:'map-node'+(selected===n.id?' selected':''),'data-id':n.id,tabindex:0,role:'button','aria-label':n.label});
  g.append(elem('circle',{cx:p.x,cy:p.y,r:n.kind==='categoria'?10:n.kind==='tecnologia'?7:n.kind==='laboratorio'?8:9,fill:colors[n.kind]||'#5c7983'}));
  if(showLabels||selected===n.id||(n.kind==='categoria'&&n.id.startsWith('cat:'))){
   const tx=elem('text',{x:p.x+11,y:p.y-10,fill:'#203b48'});
   tx.textContent=n.label.length>29?n.label.slice(0,28)+'…':n.label;g.append(tx);
  }
  g.addEventListener('click',()=>select(n.id));g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(n.id)}});
  gNodes.append(g);
 });
 const modeName={'didatico':'didático hierárquico','organico':'orgânico','radial':'radial','camadas':'por camadas','categorias':'por categorias'}[$('gLayout').value]||$('gLayout').value;
 $('gCount').textContent=`${nodes.length} de ${raw.nodes.length} nós · ${edges.length} relações · ${countTechnologies} tecnologias catalogadas · visualização ${modeName}`;
 if(doFit) fit();else applyCamera();
}
function addElement(parent,tag,classname,text){
 const el=document.createElement(tag);if(classname)el.className=classname;
 if(text)el.textContent=text;parent.append(el);return el;
}
function addLink(parent,label,href,subtext){
 const a=document.createElement('a');a.href=href;a.textContent=label;a.className='tech-guide-link';
 if(subtext){const small=document.createElement('small');small.textContent=subtext;a.append(small);}
 parent.append(a);return a;
}
function relatedTo(id){return links.filter(e=>e.source===id||e.target===id).map(e=>({relation:e.relation||'relacionado',node:byId[e.source===id?e.target:e.source]})).filter(v=>v.node);}
function select(id){
 selected=id;const n=byId[id];if(!n)return;
 detail.replaceChildren();
 addElement(detail,'h3','',n.label);
 addElement(detail,'span','tag',n.kind+(n.cat?' · '+n.cat:''));
 addElement(detail,'p','',n.summary||'Consulte o material completo para características e exemplos.');
 if(n.kind==='tecnologia'){
  const path=TECH_PATHS[n.id];
  const guide=addElement(detail,'section','tech-guide');
  addElement(guide,'h4','','Da tecnologia à implementação');
  const subtitle=path?.role||n.use||'Explore a ficha, os conceitos e as relações antes de selecionar uma forma de implementação.';
  addElement(guide,'p','tech-guide-intro',subtitle);
  const steps=addElement(guide,'div','tech-guide-steps');
  const step=(num,title,desc,href,label)=>{
    const el=addElement(steps,'div','tech-guide-step');
    addElement(el,'div','tech-step-number',num);
    const content=addElement(el,'div','tech-step-content');
    addElement(content,'strong','',title);
    addElement(content,'p','',desc);
    if(href)addLink(content,label||'Abrir material →',href);
  };
  step('1','Entender','O que faz, limites, requisitos e quando escolher.',n.href||'ecossistema-tecnologias.html','Ficha da tecnologia →');
  step('2','Relacionar','Conceitos, ferramentas, integrações e responsabilidades.',path?.concept||'ecossistema-tecnologias.html','Fundamentos e arquitetura →');
  step('3','Comparar','Critérios, alternativas e custo de complexidade.',path?.alternative||'decisao-orientada-a-problemas.html','Comparar opções →');
  if(path){
    step('4','Implementar',path.deliverable,path.lab,path.labTitle+' →');
    for(const [label,href] of path.extra){addLink(guide,label+' →',href);}
    step('5','Aplicar','Ver como a tecnologia pode participar de uma aplicação maior.',path.case,'Estudo de caso →');
  }else{
    step('4','Implementar','Ainda não há laboratório específico associado a esta ficha. Escolha um laboratório-base e adapte-o conscientemente.','laboratorios-completos.html','Consultar laboratórios disponíveis →');
    step('5','Aplicar','Encontre exemplos aplicados no catálogo de casos.','casos-integrados.html','Estudos de caso →');
  }
  addElement(guide,'p','tech-guide-caveat','Os materiais descrevem implementações de demonstração. Verifique a documentação, as versões e o status dos testes antes de uso institucional.');
 }
 for(const [name,value] of [['Quando aplicar',n.use],['Atenção',n.caution],['Maturidade',n.maturity],['Execução',n.deployment]]){
  if(!value)continue;const p=addElement(detail,'p','tech-meta');const b=addElement(p,'strong','',name+': ');p.append(document.createTextNode(value));
 }
 if(n.kind!=='tecnologia'&&n.href){addLink(detail,'Abrir material completo →',n.href);}
 if($('gLayout').value==='didatico' && n.kind==='categoria' && n.id.startsWith('cat:')){
   const btn=addElement(detail,'button','action-btn',collapsedCats.has(n.id)?'Expandir ramo desta categoria':'Recolher ramo desta categoria');
   btn.type='button';btn.addEventListener('click',()=>{if(collapsedCats.has(n.id))collapsedCats.delete(n.id);else collapsedCats.add(n.id);layoutCache={key:'',positions:{}};draw(true);select(n.id);});
 }
 const related=relatedTo(id);
 addElement(detail,'h4','',`Relações e conexões (${related.length})`);
 const relSection=addElement(detail,'div','tech-relations');
 const grouped={};for(const x of related){(grouped[x.node.kind]??=[]).push(x);}
 const order=['categoria','conceito','tecnologia','laboratorio','estudo','caso','roadmap'];
 order.concat(Object.keys(grouped).filter(k=>!order.includes(k))).forEach(kind=>{
  if(!grouped[kind])return;
  const group=addElement(relSection,'div','tech-rel-group');
  addElement(group,'h5','',({tecnologia:'Tecnologias',laboratorio:'Laboratórios',conceito:'Conceitos',categoria:'Categorias',estudo:'Estudos de caso',caso:'Aplicações',roadmap:'Roadmap'})[kind]||kind);
  grouped[kind].forEach(({relation,node})=>{
   const item=addElement(group,'div','tech-rel-item');
   const jump=addElement(item,'button','tech-jump','◎');jump.type='button';jump.title='Selecionar este nó no grafo';
   jump.addEventListener('click',()=>{if(!drawnNodes.some(n=>n.id===node.id)){$('gSearch').value=node.label;$('gKind').value='all';$('gCategory').value='all';$('gFull').checked=true;collapsedCats.clear();layoutCache={key:'',positions:{}};}select(node.id);draw(true);});
   const link=addElement(item,'div','tech-rel-link');
   addLink(link,node.label+(node.href?' ↗':''),node.href||'#',relation);
  });
 });
 draw();
}
function applyCamera(){camera.setAttribute('transform',`translate(${panX} ${panY}) scale(${zoom})`);}
function fit(){
 const ps=drawnNodes.map(n=>positions[n.id]).filter(Boolean);if(!ps.length){applyCamera();return;}
 const xs=ps.map(v=>v.x),ys=ps.map(v=>v.y);
 const xmin=Math.min(...xs)-120,xmax=Math.max(...xs)+160,ymin=Math.min(...ys)-105,ymax=Math.max(...ys)+100;
 zoom=Math.min(2.2,Math.max(0.12,Math.min(W/(xmax-xmin),H/(ymax-ymin))));
 panX=(W-zoom*(xmin+xmax))/2;panY=(H-zoom*(ymin+ymax))/2;
 applyCamera();
 if(drawnNodes.length>65 && $('gLayout').value==='didatico') draw(false);
}
function point(event){
 const pt=svg.createSVGPoint();pt.x=event.clientX;pt.y=event.clientY;
 return pt.matrixTransform(svg.getScreenCTM().inverse());
}
function zoomAt(factor,location){
 const next=Math.min(6,Math.max(.10,zoom*factor));const ratio=next/zoom;
 panX=location.x-(location.x-panX)*ratio;panY=location.y-(location.y-panY)*ratio;zoom=next;
 draw();
}
svg.addEventListener('wheel',e=>{ e.preventDefault(); zoomAt(Math.exp(-e.deltaY*.0015),point(e)); },{passive:false});
svg.addEventListener('pointerdown',e=>{ if(e.target.closest('.map-node'))return; const p=point(e); drag={x:p.x,y:p.y,panX,panY}; svg.setPointerCapture(e.pointerId); });
svg.addEventListener('pointermove',e=>{if(!drag)return;const p=point(e);panX=drag.panX+p.x-drag.x;panY=drag.panY+p.y-drag.y;applyCamera();});
svg.addEventListener('pointerup',()=>drag=null);
svg.addEventListener('pointercancel',()=>drag=null);
$('gZoomIn').addEventListener('click',()=>zoomAt(1.28,{x:W/2,y:H/2}));
$('gZoomOut').addEventListener('click',()=>zoomAt(1/1.28,{x:W/2,y:H/2}));
$('gFit').addEventListener('click',fit);
$('gToggleControls').addEventListener('click',()=>{filtersOpen=!filtersOpen;$('explorar').hidden=!filtersOpen;$('gToggleControls').setAttribute('aria-expanded',String(filtersOpen));$('gToggleControls').textContent=filtersOpen?'✕ Ocultar filtros':'⚙ Filtros avançados';});
$('gOrientation').addEventListener('change',()=>{layoutCache={key:'',positions:{}};draw(true);});

if($('gExpandAll')) $('gExpandAll').addEventListener('click',()=>{collapsedCats.clear();layoutCache={key:'',positions:{}};draw(true);});
if($('gCollapseAll')) $('gCollapseAll').addEventListener('click',()=>{categoriesForDidacticPanel().forEach(v=>collapsedCats.add(v.node.id));layoutCache={key:'',positions:{}};draw(true);});
function setFullscreen(on){
 fullscreen=on;layout.classList.toggle('graph-fullscreen',on);document.body.classList.toggle('graph-mode',on);
 $('gFullscreen').textContent=on?'✕ Sair da tela cheia':'⛶ Tela cheia';
 fit();
}
$('gFullscreen').addEventListener('click',()=>setFullscreen(!fullscreen));
document.addEventListener('keydown',e=>{
 if(e.key==='Escape'&&fullscreen)setFullscreen(false);
 if((e.key==='f'||e.key==='F')&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)&&!e.ctrlKey){e.preventDefault();setFullscreen(!fullscreen)}
});
$('gReset').addEventListener('click',()=>{
 selected=null;focusedTechnology=null; collapsedCats.clear(); $('gSearch').value='';$('gKind').value='all';$('gCategory').value='all';$('gLayout').value='didatico';$('gOrientation').value='vertical';$('gFull').checked=false;$('gEdges').checked=true;layoutCache={key:'',positions:{}};draw(true);
});
$('gEdges').addEventListener('change',()=>draw());
for(const id of ['gSearch','gKind','gFull','gCategory','gLayout']) $(id).addEventListener(id==='gSearch'?'input':'change',()=>{selected=null;focusedTechnology=null;layoutCache={key:'',positions:{}};draw(true);});
$('gExploreToggle').addEventListener('click',()=>openExplorer(!explorerOpen));
$('gExploreClose').addEventListener('click',()=>openExplorer(false));
$('gExploreSearch').addEventListener('input',renderExplorer);
$('gExploreReset').addEventListener('click',()=>{focusedTechnology=null;selected=null;layoutCache={key:'',positions:{}};draw(true);openExplorer(false);});
$('gDetailToggle').addEventListener('click',()=>setDetail(!detailOpen));
$('gDetailReopen').addEventListener('click',()=>setDetail(true));
// Explore/close controls work with the existing fullscreen layout.
renderExplorer();
draw(true);
})();
