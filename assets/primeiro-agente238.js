(()=>{'use strict';
const initial=[
  {id:'C01',name:'Introdução à IA',seats:30,defaultSeats:30,area:'IA'},
  {id:'C02',name:'Agentes de IA',seats:15,defaultSeats:15,area:'IA'},
  {id:'C03',name:'Banco de Dados',seats:20,defaultSeats:20,area:'BD'},
  {id:'C04',name:'Engenharia de Prompts',seats:0,defaultSeats:0,area:'IA'},
  {id:'C05',name:'Automação com n8n',seats:10,defaultSeats:10,area:'Automação'}
];
let catalog=initial.map(x=>({...x})), previous=null, last=null;
const el=id=>document.getElementById(id);
const asText=(id,value)=>{const node=el(id); if(node) node.textContent=value;};
function cloneCatalog(){return catalog.map(x=>({...x}));}
function selectedCourse(){return catalog.find(c=>c.id===el('course238').value);} 
function renderCatalog(){
  const ul=document.createElement('ul'); ul.className='catalog-list';
  catalog.forEach(c=>{
    const li=document.createElement('li');
    const strong=document.createElement('strong'); strong.textContent=c.name;
    const span=document.createElement('span'); span.textContent=' — '+c.seats+' vagas'; span.className=c.seats>0?'open':'zero';
    li.append(strong, span); ul.append(li);
  });
  el('catalog238').replaceChildren(ul);
  const current=selectedCourse(); if(current) el('seats238').value=current.seats;
}
function setResult(message, status='Pronto'){ asText('answer238', message); asText('stateLabel238', status); }
function setGoalLabel(){ asText('goalLabel238', el('goal238').selectedOptions[0].textContent); }
function resetExplain(){
  asText('what238','Execute primeiro.');
  asText('how238','O mecanismo aplica regras explícitas ao estado observado.');
  asText('risk238','O catálogo é fictício e as decisões dependem das regras definidas.');
  asText('next238','Altere vagas, negue autorização e execute novamente.');
}
function reset(){
  catalog=initial.map(x=>({...x,seats:x.defaultSeats}));
  previous=null; last=null;
  el('goal238').value='available'; el('tool238').checked=true; el('course238').value='C01';
  renderCatalog(); setGoalLabel(); asText('toolLabel238','Leitura autorizada'); setResult('Selecione um objetivo e execute o agente.','Sem execução');
  asText('trace238','Nenhuma execução ainda.'); asText('technicalGoal238','A definir na execução'); asText('technicalDecision238','Aguardando execução'); resetExplain();
}
function updateCourseSeats(value){
  const c=selectedCourse(); if(!c) return false;
  const n=Number(value);
  if(!Number.isInteger(n) || n<0 || n>100){ setResult('Informe um número inteiro de vagas entre 0 e 100.','Erro de entrada'); return false; }
  c.seats=n; renderCatalog();
  setResult('Ambiente atualizado. Agora execute o agente para observar a nova percepção.','Ambiente alterado');
  return true;
}
function change(){ updateCourseSeats(el('seats238').value); }
function scenarioZero(){ el('seats238').value=0; updateCourseSeats(0); }
function scenarioOpen(){ const c=selectedCourse(); if(!c) return; el('seats238').value=c.defaultSeats; updateCourseSeats(c.defaultSeats); }
function run(){
  const goal=el('goal238').value; const authorized=el('tool238').checked; const start=performance.now();
  const trace={ambiente:'catálogo fictício',tipo:'agente reflexivo simples (didático)',decisao:'regras condição–ação',objetivo:goal,autorizado:authorized,percepcao:null,regra:null,acao:null,resultado:null,latencia_ms:0};
  setGoalLabel(); asText('toolLabel238', authorized ? 'Leitura autorizada' : 'Leitura bloqueada');
  if(!authorized){
    trace.regra='Se não houver autorização, bloquear o acesso ao catálogo'; trace.acao='Nenhuma ferramenta executada'; trace.resultado='Execução bloqueada';
    setResult('Acesso ao catálogo não autorizado. O agente não pode observar o ambiente e, portanto, não consegue decidir sobre as vagas.','Execução bloqueada');
    asText('what238','O agente tentou iniciar a observação, mas a ferramenta estava bloqueada.');
    asText('how238','Antes de consultar o catálogo, verificou a autorização e interrompeu a execução por segurança.');
    asText('risk238','Mesmo um agente simples precisa de autorização correta. Sem acesso ao ambiente, não há percepção válida.');
    asText('next238','Marque novamente a autorização e execute de novo. Depois teste o mesmo objetivo com e sem permissão.');
  } else {
    const current=cloneCatalog(); trace.percepcao=current.map(x=>({id:x.id,nome:x.name,vagas:x.seats}));
    let result='';
    if(goal==='available'){
      trace.regra='Se vagas > 0, incluir o curso na resposta'; trace.acao='Listar cursos com vagas';
      const selected=current.filter(x=>x.seats>0);
      result=selected.length ? 'Cursos com vagas: '+selected.map(x=>x.name+' ('+x.seats+')').join('; ') : 'Nenhum curso possui vagas neste momento.';
      asText('what238','Observou o catálogo e listou apenas os cursos com vagas disponíveis.');
      asText('how238','Aplicou a regra “se vagas > 0, incluir na saída”.');
      asText('risk238','Se o catálogo estiver desatualizado, a lista também estará incorreta.');
      asText('next238','Escolha um curso, zere as vagas e execute novamente para verificar a mudança no resultado.');
    } else if(goal==='alerts'){
      trace.regra='Se havia vagas antes e agora o valor chegou a zero, emitir alerta'; trace.acao='Comparar percepção atual com a observação anterior';
      const changed=previous ? current.filter(x=>x.seats===0 && (previous.find(p=>p.id===x.id)?.seats ?? 0) > 0) : [];
      result = previous ? (changed.length ? 'Alerta: '+changed.map(x=>x.name).join(', ')+' ficou sem vagas.' : 'Nenhum curso mudou de “com vagas” para “sem vagas” desde a última observação.') : 'Primeira observação registrada. Agora altere as vagas de algum curso e execute novamente para verificar mudanças.';
      asText('what238','Comparou o estado atual com a observação anterior para detectar transições para zero vagas.');
      asText('how238','Aplicou uma regra temporal simples: só alerta quando identifica mudança entre duas observações.');
      asText('risk238','Se não houver observação anterior, não é possível detectar mudança; apenas registrar o estado atual.');
      asText('next238','Primeiro execute uma vez. Depois mude um curso de valor positivo para zero e execute novamente.');
    } else {
      trace.regra='Se o curso for da área de IA e tiver vagas, recomendar a primeira opção disponível'; trace.acao='Selecionar uma recomendação simples';
      const selected=current.filter(x=>x.area==='IA' && x.seats>0);
      result = selected.length ? 'Recomendação: '+selected[0].name+' ('+selected[0].seats+' vagas).' : 'Nenhum curso da área de IA possui vagas disponíveis.';
      asText('what238','Buscou cursos da área de IA e escolheu uma recomendação com base em uma regra fixa.');
      asText('how238','Aplicou a condição “área = IA” e “vagas > 0”, depois selecionou a primeira opção elegível.');
      asText('risk238','A recomendação é muito simples: não considera preferências, horários, custos ou perfil do estudante.');
      asText('next238','Altere as vagas dos cursos de IA e compare como a recomendação muda.');
    }
    previous=current; trace.resultado=result; setResult(result,'Execução concluída');
  }
  trace.latencia_ms=Math.round((performance.now()-start)*1000)/1000; last=trace;
  asText('technicalGoal238', el('goal238').selectedOptions[0].textContent); asText('technicalDecision238', authorized ? 'Regra aplicada e resposta produzida' : 'Execução bloqueada por permissão'); asText('trace238', JSON.stringify(trace,null,2));
}
function exportTrace(){ if(!last) return; const blob=new Blob([JSON.stringify(last,null,2)],{type:'application/json'}); const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download='registro-primeiro-agente.json'; a.click(); setTimeout(()=>URL.revokeObjectURL(url),1000); }
['goal238','tool238'].forEach(id=>el(id).addEventListener('change',()=>{setGoalLabel(); asText('toolLabel238',el('tool238').checked?'Leitura autorizada':'Leitura bloqueada');}));
el('run238').addEventListener('click',run); el('change238').addEventListener('click',change); el('scenarioZero238').addEventListener('click',scenarioZero); el('scenarioOpen238').addEventListener('click',scenarioOpen); el('reset238').addEventListener('click',reset); el('course238').addEventListener('change',renderCatalog); el('export238').addEventListener('click',exportTrace);
reset();
})();