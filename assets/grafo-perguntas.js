(()=>{
'use strict';
const data=window.WIKI_GRAFO;
const $=id=>document.getElementById(id);
if(!data||!$('qpTech'))return;
const nodes=data.nodes||[], edges=data.edges||[];
const byId=new Map(nodes.map(n=>[n.id,n]));
const byName=new Map(nodes.filter(n=>n.kind==='tecnologia').map(n=>[n.label.toLocaleLowerCase('pt-BR'),n]));
const datalist=$('qpSuggestions');
nodes.filter(n=>n.kind==='tecnologia').sort((a,b)=>a.label.localeCompare(b.label,'pt')).forEach(n=>{const x=document.createElement('option');x.value=n.label;datalist.append(x);});
const kindNames={categoria:'Categoria',conceito:'Conceito',tecnologia:'Tecnologia',laboratorio:'Laboratório',estudo:'Estudo de caso',caso:'Aplicação',roadmap:'Percurso'};
function category(n){return kindNames[n.kind]||n.kind;}
function roleGroup(n,relation){
 const r=(relation||'').toLocaleLowerCase();
 if(n.kind==='laboratorio'||r.includes('laborat')||r==='usa'&&n.kind==='laboratorio')return 'laboratorio';
 if(n.kind==='estudo'||n.kind==='caso')return 'aplicacao';
 if(n.kind==='categoria')return 'categoria';
 if(r.includes('alternativa')||r.includes('diferencia')||r.includes('compara'))return 'alternativa';
 if(n.kind==='conceito')return 'concept';
 return 'outros';
}
const labels={laboratorio:'Laboratórios e implementação',aplicacao:'Aplicações e estudos de caso',categoria:'Categorias',alternativa:'Alternativas e comparação',concept:'Conceitos e capacidades',outros:'Outras relações cadastradas'};
function addLink(node,text,parent){const a=document.createElement('a');a.href=node.href||'grafo.html';a.textContent=text;parent.append(a);}
function render(){
 const query=$('qpTech').value.trim().toLocaleLowerCase('pt-BR');const matches=[...byName.values()].filter(n=>n.label.toLocaleLowerCase('pt-BR').includes(query));
 const n=byName.get(query)||(matches.length===1?matches[0]:null);
 const feedback=$('qpFeedback'),out=$('qpResults');out.replaceChildren();
 if(!n){feedback.textContent=query?`Selecione uma das tecnologias sugeridas. ${matches.length} correspondência(s) encontradas.`:'Digite ou selecione uma tecnologia.';return;}
 $('qpTech').value=n.label;
 const q=$('qpQuestion').value;
 const related=edges.filter(e=>e.source===n.id||e.target===n.id).map(e=>({relation:e.relation||'relacionado',node:byId.get(e.source===n.id?e.target:e.source)})).filter(v=>v.node);
 const grouped={};for(const item of related){const key=roleGroup(item.node,item.relation);(grouped[key]??=[]).push(item);}
 feedback.textContent=`${n.label}: ${related.length} relação(ões) registradas no grafo. A lista abaixo não comprova suporte técnico nativo.`;
 const title=document.createElement('h3');title.textContent=n.label;out.append(title);
 const desc=document.createElement('p');desc.textContent=n.summary||'Consulte a ficha da tecnologia.';out.append(desc);
 const intro=document.createElement('p');addLink(n,'Ficha da tecnologia',intro);intro.append(' · ');const graph=document.createElement('a');graph.href='grafo.html?tech='+encodeURIComponent(n.label);graph.textContent='Selecionar no grafo visual';intro.append(graph);intro.append(' · ');const comp=document.createElement('a');comp.href='comparar-tecnologias.html';comp.textContent='Comparar tecnologias';intro.append(comp);out.append(intro);
 let groupsShown=0;
 const ordered=['categoria','concept','alternativa','laboratorio','aplicacao','outros'];
 const keys=q==='all'?ordered:(q==='concept'?['concept','outros']:q==='alternativa'?['alternativa','outros']:q==='categoria'?['categoria']:q==='laboratorio'?['laboratorio']:['aplicacao']);
 for(const key of keys){const items=grouped[key]||[];if(!items.length)continue;groupsShown++;
   const section=document.createElement('section'),h=document.createElement('h4');h.textContent=labels[key];section.append(h);
   const ul=document.createElement('ul');for(const item of items){const li=document.createElement('li');const rel=document.createElement('strong');rel.textContent=item.relation+' · ';li.append(rel);addLink(item.node,item.node.label,li);const badge=document.createElement('small');badge.textContent=' ('+category(item.node)+')';li.append(badge);ul.append(li);}section.append(ul);out.append(section);
 }
 if(!groupsShown){const p=document.createElement('p');p.textContent='Não há relações explícitas cadastradas para essa pergunta. Isso não significa que a tecnologia não tenha a capacidade; consulte sua documentação oficial.';out.append(p);}
 if(q==='laboratorio'&&!(grouped.laboratorio||[]).length){const p=document.createElement('p');p.append('Nenhum laboratório diretamente vinculado. Consulte o ');const a=document.createElement('a');a.href='laboratorios-completos.html';a.textContent='índice de laboratórios';p.append(a,'.');out.append(p);}
}
$('qpRun').addEventListener('click',render);
$('qpQuestion').addEventListener('change',()=>{if($('qpTech').value)render();});
$('qpTech').addEventListener('keydown',e=>{if(e.key==='Enter')render();});
$('qpClear').addEventListener('click',()=>{$('qpTech').value='';$('qpResults').replaceChildren();$('qpFeedback').textContent='';});
const params=new URLSearchParams(location.search);const start=params.get('tech');if(start){$('qpTech').value=start;render();}
})();
