(()=>{
'use strict';
const $=id=>document.getElementById(id), db=window.UNESP_IA_TECHS||[];
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const by=k=>db.find(x=>x.key===k);
const fields=[['group','Função predominante'],['skill','Modo de implementação'],['goal','O que constrói'],['when','Quando vale a pena'],['llm','Qual modelo / provedor'],['lab','Exemplo de atividade']];
if($('cmpA')){
 const selects=[$('cmpA'),$('cmpB'),$('cmpC')];
 selects.forEach((el,i)=>{
  if(i===2)el.add(new Option('Não comparar terceira tecnologia',''));
  db.forEach(x=>el.add(new Option(x.name,x.key)));
 });
 $('cmpA').value='n8n';$('cmpB').value='openclaw';$('cmpC').value='hermes';
 function render(){
  const keys=selects.map(x=>x.value).filter(Boolean);
  const warning=$('cmpWarning');const dup=new Set(keys).size<keys.length;
  warning.hidden=!dup;if(dup)warning.textContent='Escolha tecnologias diferentes para uma comparação mais útil.';
  const rows=keys.map(by).filter(Boolean);
  let out='<table class="comparison-table"><thead><tr><th>Critério</th>'+rows.map(x=>'<th>'+escape(x.name)+'</th>').join('')+'</tr></thead><tbody>';
  fields.forEach(([key,label])=>{out+='<tr><th>'+escape(label)+'</th>'+rows.map(x=>'<td>'+escape(x[key])+'</td>').join('')+'</tr>';});
  out+='<tr><th>Explorar</th>'+rows.map(x=>'<td><a href="'+encodeURI(x.lab_url)+'">Abrir laboratório</a> · <a href="grafo.html?tech='+encodeURIComponent(x.graph)+'">Ver no grafo</a></td>').join('')+'</tr></tbody></table>';
  $('cmpTable').innerHTML=out;
 }
 selects.forEach(x=>x.addEventListener('change',render));
 $('cmpReset').addEventListener('click',()=>{$('cmpA').value='n8n';$('cmpB').value='openclaw';$('cmpC').value='hermes';render();});
 render();
}
if($('advGo')){
 const prefs={
  automatizar:['n8n','python','Um fluxo determinístico é a primeira hipótese; só acrescente IA se precisar interpretar entradas não estruturadas.'],
  tool:['agents','n8n','Um SDK Python permite definir funções e testá-las; n8n é uma alternativa quando a integração visual domina.'],
  estado:['langgraph','agents','Transições, estados e eventual retomada exigem controle explícito do processo.'],
  equipe:['crewai','adk','Papéis especializados só ajudam quando as tarefas são realmente separáveis e avaliáveis.'],
  assistente:['hermes','openclaw','Skills, sessões e memória justificam experimentar um runtime.'],
  canais:['openclaw','n8n','Gateway e sessões têm valor para vários canais; integrações simples ainda podem ser um workflow.'],
  bots:['grok','crewai','A plataforma gerenciada pode acelerar uma demonstração, mas é preciso avaliar acesso e dependência de fornecedor.'],
  rag:['python','agents','Primeiro valide recuperação e citações; não acrescente autonomia antes de medir qualidade das fontes.']
 };
 const safeNote='Se houver informações pessoais ou institucionais, comece com dados sintéticos, políticas de acesso e aprovação humana; não conecte documentos sensíveis diretamente a plataformas externas.';
 function render(){
  const goal=$('advGoal').value,skill=$('advSkill').value,infra=$('advInfra').value,sensitive=$('advData').value==='sim';
  let [first,alt,why]=prefs[goal]||prefs.tool;
  if(skill==='visual'&&['tool','rag'].includes(goal)){alt=first;first='n8n';why='Para quem prefere interface visual, comece por um workflow e evolua para ferramentas agênticas se necessário. '+why;}
  if(skill==='python'&&goal==='automatizar'){alt='agents';}
  if(infra==='restrito'&&first==='grok'){alt='python';why+=' Caso o acesso ao Grok Bot não esteja disponível, use um baseline reproduzível em Python.';}
  if(infra==='restrito'&&first==='openclaw'){why+=' Considere infraestrutura, modelo e custos antes de iniciar um runtime persistente.';}
  const a=by(first),b=by(alt);const modelText=(infra==='local'?'Comece com Ollama e um modelo pequeno compatível; confirme suporte a ferramentas na versão instalada.':'Use um provedor compatível e registre política de dados, custo, latência e credenciais.');
  $('advResult').innerHTML='<h2>Seu percurso recomendado</h2><p><strong>Ponto de partida: '+escape(a.name)+'</strong> — '+escape(why)+'</p><p><strong>Alternativa: '+escape(b.name)+'</strong>. Compare os dois antes de decidir.</p><p><strong>LLM e execução:</strong> '+escape(modelText)+'</p>'+(sensitive?'<p class="advisor-warning"><strong>Atenção aos dados:</strong> '+safeNote+'</p>':'')+'<ol><li><a href="percurso.html">Revisar fundamentos e arquitetura</a></li><li><a href="primeiro-agente.html">Executar um exemplo mínimo</a></li><li><a href="'+escape(a.lab_url)+'">Seguir o laboratório recomendado</a></li><li><a href="qualidade-laboratorios.html">Documentar testes e evidências</a></li><li><a href="comparar-tecnologias.html">Comparar alternativas tecnológicas</a></li></ol><p><a href="grafo.html?tech='+encodeURIComponent(a.graph)+'">Explorar conexões no grafo</a></p>';
 }
 $('advGo').addEventListener('click',render);render();
}
if($('auditChecklist')){
 const all=Array.from($('auditChecklist').querySelectorAll('input'));
 function status(){$('auditStatus').textContent=all.filter(x=>x.checked).length+' de '+all.length+' critérios marcados — estes registros não substituem a comprovação da execução.';}
 all.forEach(x=>x.addEventListener('change',status));status();
 $('auditCopy').addEventListener('click',()=>{
  const text=all.map(x=>(x.checked?'[x] ':'[ ] ')+x.parentNode.textContent.trim()).join('\n');
  if(navigator.clipboard?.writeText)navigator.clipboard.writeText(text).catch(()=>window.prompt('Copie seu checklist:',text));
  else window.prompt('Copie seu checklist:',text);
 });
}
})();