(()=>{'use strict';
const host=document.querySelector('.inter241');if(!host)return;
const type=host.dataset.lab,$=id=>document.getElementById(id),value=id=>$(id)?.value,checked=id=>!!$(id)?.checked;
const courses=[{id:'C01',name:'Introdução à IA',price:0,hours:20,seats:30,area:'IA'},{id:'C02',name:'Agentes de IA',price:100,hours:40,seats:15,area:'IA'},{id:'C03',name:'Banco de Dados',price:80,hours:30,seats:20,area:'BD'},{id:'C04',name:'Engenharia de Prompts',price:50,hours:10,seats:0,area:'IA'},{id:'C05',name:'Automação com n8n',price:60,hours:20,seats:10,area:'Automação'}];
const state={memory:null,notes:[],diva:[],last:null};
const currency=n=>Number(n).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
const n=id=>{const num=Number(value(id));return Number.isFinite(num)&&num>=0?num:null;};
function explained(what,how,risk,next){for(const [id,text] of Object.entries({'lab241-what':what,'lab241-how':how,'lab241-risk':risk,'lab241-next':next}))$(id).textContent=text;}
function setOutput(result,extra=''){$('lab241-output').textContent=result;$('lab241-extra').textContent=extra;}
function finish(op,params,result,steps,what,how,risk,next,start,model='nenhum'){
 const trace={laboratorio:type,operacao:op,parametros:params,etapas:steps,resultado:result,modelo:model,latencia_ms:Math.round((performance.now()-start)*1000)/1000};
 state.last=trace;$('lab241-trace').textContent=JSON.stringify(trace,null,2);$('lab241-flow').textContent=steps.join(' → ');$('lab241-model').textContent=model;
 explained(what,how,risk,next);$('lab241-explain').open=true;return trace;
}
function runSync(){const start=performance.now();let result='',extra='',what='',how='',risk='',next='',params={},steps=[],model='nenhum';
 switch(type){
 case 'workflow':{
   const c=courses.find(x=>x.id===value('lab241-course')),approved=checked('lab241-approve');params={curso:c.id,aprovado:approved};steps=['Consultar catálogo','Verificar vagas'];
   if(c.seats===0){steps.push('Interromper fluxo');result=`Inscrição não simulada: ${c.name} está sem vagas.`;}
   else if(!approved){steps.push('Solicitar aprovação','Interromper fluxo');result='Inscrição não simulada: aprovação humana não concedida.';}
   else {steps.push('Confirmar autorização','Simular inscrição');result=`Inscrição fictícia autorizada para ${c.name}. Nenhuma vaga foi alterada.`;}
   what='Executou uma sequência de etapas predefinidas.';how='A ordem das verificações é fixa: catálogo, vagas e autorização.';risk='Fluxos fixos não resolvem situações fora das regras previstas.';next='Selecione um curso sem vagas ou desmarque a autorização.';break;
 }
 case 'skill':{
   const budget=n('lab241-budget'),hours=n('lab241-hours'),priority=value('lab241-priority');if(budget===null||hours===null||hours<1){setOutput('Informe orçamento e duração válidos.');return;}
   const eligible=courses.filter(c=>c.seats>0&&c.price<=budget&&c.hours<=hours);const comparator=priority==='preco'?(a,b)=>a.price-b.price:priority==='horas'?(a,b)=>a.hours-b.hours:(a,b)=>b.seats-a.seats;eligible.sort(comparator);
   result=eligible.length?eligible.map(c=>`${c.name} — ${currency(c.price)}, ${c.hours}h, ${c.seats} vagas`).join('\n'):'Nenhum curso atende às regras da skill.';
   extra=`SKILL.md (representação didática): orçamento: ${budget}; duração máxima: ${hours}h; prioridade: ${priority}.`;
   steps=['Ler parâmetros declarativos','Consultar catálogo','Filtrar cursos','Ordenar resultados'];params={budget,hours,priority};what='Aplicou uma competência de recomendação configurável.';how='Filtrou cursos por preço, duração e disponibilidade e depois ordenou.';risk='O interpretador didático não executa uma skill nativa de agente.';next='Altere a prioridade e o orçamento para observar outras recomendações.';break;
 }
 case 'memoria':{
   const name=value('lab241-name').trim(),interest=value('lab241-interest'),enabled=checked('lab241-memory-on');if(!name){setOutput('Informe um nome fictício.');return;}
   params={name,interest,memory:enabled};steps=['Receber preferências','Consultar estado da memória'];const previous=state.memory;
   const used=enabled?previous:null;result=used?`Bem-vindo(a) de volta, ${name}. Lembrei que seu interesse anterior era ${used.interest}. Agora você selecionou ${interest}.`:`Olá, ${name}. Interesse atual: ${interest}. ${enabled?'Vou registrar para a próxima execução.':'A memória foi desativada nesta execução.'}`;
   if(enabled){state.memory={name,interest};steps.push('Atualizar memória da sessão');}steps.push('Responder');
   what='Consultou e, quando autorizado, atualizou um registro de preferências.';how='Usou uma variável estruturada em memória da aba.';risk='Os dados são voláteis e não representam armazenamento seguro.';next='Execute novamente com outra área, compare memória ligada e desligada.';break;
 }
 case 'agente-llm':{
   const message=value('lab241-message').trim(),runtime=value('lab241-runtime');if(!message){setOutput('Informe uma solicitação.');return;}
   if(runtime==='backend'){setOutput('O modo institucional requer servidor implantado e credencial. Realizando teste de conexão…');runBackend(message);return;}
   params={message,runtime};steps=['Receber solicitação','Reconhecer padrões','Selecionar consulta','Apresentar resultado'];
   const match=message.match(/(sem vagas|indispon[ií]vel)/i)?'empty':/(ia|intelig[êe]ncia artificial)/i.test(message)?'ai':'all';
   const found=courses.filter(c=>match==='empty'?c.seats===0:match==='ai'?c.area==='IA'&&c.seats>0:c.seats>0);
   result=found.map(c=>`${c.name}: ${c.seats} vagas`).join('\n')||'Nenhum curso encontrado.';extra='ATENÇÃO: esta resposta foi produzida por regras, não por um LLM.';
   what='Selecionou uma consulta a partir de palavras-chave.';how='Utilizou expressões regulares e regras fixas.';risk='Não entende solicitações livres como um modelo de linguagem.';next='Teste uma solicitação com sinônimos e compare com um backend real.';break;
 }
 case 'rag':{
   const document=value('lab241-document').trim(),question=value('lab241-question').trim();if(!document||!question){setOutput('Preencha o documento e a pergunta.');return;}
   const chunks=document.split(/(?<=[.!?])\s+/).filter(Boolean);const norm=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();const stop=new Set(['qual','como','para','uma','que','com','por','sao','tem','dos','das','esse','esta','sobre','necessario','preciso','receber','minima']);
   const keys=[...new Set(norm(question).match(/[a-z0-9]+/g)||[])].filter(w=>w.length>2&&!stop.has(w));const scores=chunks.map((text,i)=>({text,i,score:keys.filter(w=>norm(text).includes(w)).length})).sort((a,b)=>b.score-a.score);const top=scores.filter(x=>x.score>0).slice(0,3);
   result=top.length?top.map(c=>`Trecho ${c.i+1} (correspondências: ${c.score}): ${c.text}`).join('\n'):'Nenhum trecho lexicalmente correspondente foi encontrado.';
   extra='Resultado extrativo com indicação dos trechos; não houve resposta gerada por LLM.';params={question,trechos:chunks.length};steps=['Extrair texto','Dividir em trechos','Comparar palavras','Retornar fontes'];what='Recuperou trechos do texto fornecido.';how='Aplicou correspondência lexical simplificada.';risk='Pode falhar em sinônimos e não verifica verdade factual.';next='Troque palavras da pergunta por sinônimos e compare os trechos recuperados.';break;
 }
 case 'mcp':{
   const tool=value('lab241-tool'),c=courses.find(c=>c.id===value('lab241-course'));const request={jsonrpc:'2.0',id:1,method:'tools/call',params:{name:tool,arguments:{id:c.id}}};
   const resultObject=tool==='listar_cursos'?courses.map(x=>({id:x.id,nome:x.name,vagas:x.seats})):tool==='consultar_vagas'?{id:c.id,vagas:c.seats}:tool==='consultar_regulamento'?{certificado:'frequência mínima de 70% (regra fictícia)'}:{id:c.id,pode_simular:c.seats>0,alterou_dados:false};
   result='Resposta simulada:\n'+JSON.stringify({jsonrpc:'2.0',id:1,result:{content:[{type:'text',text:JSON.stringify(resultObject)}]}},null,2);
   extra='Requisição simulada:\n'+JSON.stringify(request);params={tool,curso:c.id};steps=['Descobrir ferramenta (simulado)','Construir JSON-RPC','Executar função local','Apresentar resposta simulada'];what='Construiu e processou uma mensagem em formato JSON-RPC.';how='Chamou uma função JavaScript local, simulando um servidor MCP.';risk='Não houve conexão nem negociação real com um servidor MCP.';next='Experimente outras ferramentas e consulte o módulo avançado para o MCP real.';break;
 }
 case 'multiagentes':{
   const budget=n('lab241-budget'),mode=value('lab241-mode');if(budget===null){setOutput('Informe um orçamento válido.');return;}
   const found=courses.filter(c=>c.price<=budget&&c.seats>0);params={budget,mode};
   steps=mode==='single'?['Agente único: filtrar e recomendar']:['Orientador: sugerir','Secretaria: verificar vagas','Verificador: validar'];
   result=found.length?found.map(c=>`${c.name} — ${currency(c.price)}`).join('\n'):'Nenhuma recomendação disponível.';
   what=mode==='single'?'Um único componente fez toda a seleção.':'Três funções especializadas realizaram as etapas em sequência.';how='As duas estratégias aplicaram critérios equivalentes e determinísticos.';risk='Papéis especializados não equivalem, por si só, a agentes LLM autônomos.';next='Compare o resultado e a estrutura do fluxo nas duas estratégias.';break;
 }
 case 'diva':{
   const kind=value('lab241-kind'),desc=value('lab241-desc').trim(),amount=n('lab241-amount');if(!desc){setOutput('Preencha uma descrição fictícia.');return;}
   if(kind==='despesas'&&amount===null){setOutput('Informe um valor válido.');return;}
   const item={kind,desc,amount:kind==='despesas'?amount:0};state.diva.push(item);params={kind,desc,amount:item.amount,persist:checked('lab241-persist')};
   if(checked('lab241-persist')){try{localStorage.setItem('agentia241_diva_demo',JSON.stringify(state.diva));}catch(e){extra='Não foi possível salvar no navegador.';}}
   else {try{localStorage.removeItem('agentia241_diva_demo');}catch(e){}}
   const expenses=state.diva.filter(x=>x.kind==='despesas').reduce((s,x)=>s+x.amount,0);
   result=`Registro adicionado: ${desc}.\n\nDIVA.Dia (demonstração)\nTarefas: ${state.diva.filter(x=>x.kind==='tarefas').length}\nAnotações: ${state.diva.filter(x=>x.kind==='anotacoes').length}\nDespesas registradas: ${currency(expenses)}`;
   steps=['Validar informação','Registrar em memória','Consolidar DIVA.Dia'];what='Registrou um dado e consolidou um resumo.';how='Usou um array de registros e cálculos por função.';risk='localStorage não é criptografado; não insira informações pessoais reais.';next='Registre uma tarefa e uma despesa; observe a atualização do DIVA.Dia.';break;
 }
 case 'comparador':{
   const budget=n('lab241-budget'),hours=n('lab241-hours');if(budget===null||hours===null||hours<1){setOutput('Informe parâmetros válidos.');return;}
   const t1=performance.now(),a=courses.filter(c=>c.price<=budget&&c.hours<=hours&&c.seats>0).sort((x,y)=>x.price-y.price),dt1=performance.now()-t1;
   const t2=performance.now(),b=courses.filter(c=>c.price<=budget&&c.hours<=hours&&c.seats>0).sort((x,y)=>y.seats-x.seats),dt2=performance.now()-t2;
   const fmt=x=>x.length?x.map(c=>c.name).join(', '):'Nenhum';
   result=`Estratégia A — menor preço: ${fmt(a)}\nEstratégia B — maior disponibilidade: ${fmt(b)}`;
   extra=`Tempo medido A: ${dt1.toFixed(3)} ms; B: ${dt2.toFixed(3)} ms. Tokens LLM: 0. Tempos locais de operações pequenas não são benchmarks robustos.`;
   params={budget,hours};steps=['Fixar mesmo catálogo','Aplicar estratégia A','Aplicar estratégia B','Comparar saídas e tempo'];what='Comparou dois algoritmos no mesmo conjunto de dados.';how='Variou apenas o critério de ordenação.';risk='Uma execução isolada e tempos mínimos não representam superioridade de desempenho.';next='Mude o orçamento e a carga horária e repita o teste.';break;
 }
 }
 setOutput(result,extra);finish(type,params,result,steps,what,how,risk,next,start,model);
}
async function runBackend(message){
 const url=value('lab241-url').trim(),key=value('lab241-key');
 if(!url||!key){setOutput('Informe um endpoint autorizado e a chave temporária. Nenhuma requisição foi realizada.');return;}
 let parsed;try{parsed=new URL(url);if(parsed.protocol!=='https:'&&!['localhost','127.0.0.1'].includes(parsed.hostname))throw new Error('HTTPS obrigatório');}catch(e){setOutput('Endereço inválido: use HTTPS, exceto localhost para laboratório.');return;}
 const start=performance.now();try{
   const res=await fetch(parsed.href,{method:'POST',headers:{'content-type':'application/json','x-api-key':key},body:JSON.stringify({message})});const body=await res.json();if(!res.ok)throw Error('HTTP '+res.status+': '+JSON.stringify(body));
   const result=JSON.stringify(body,null,2);setOutput(result,'Resposta recebida do endpoint configurado. Revise as ações antes de executá-las.');finish('backend-plan',{message,endpoint:parsed.origin},result,['Enviar solicitação','Consultar servidor','Receber plano','Exibir plano (sem executar escrita)'],'Consultou um endpoint externo.','O backend interpretou a solicitação e retornou um plano.','As respostas do LLM precisam de validação; o laboratório não executa operações de escrita automaticamente.','Compare com o modo determinístico.',start,'LLM remoto: resposta do servidor');
 }catch(e){setOutput('Não foi possível executar no servidor: '+e.message+'\nUse o modo determinístico ou verifique a implantação.');}
}
function reset(){state.memory=null;state.diva=[];state.last=null;$('lab241-output').textContent='Altere os parâmetros e execute a experiência.';$('lab241-extra').textContent='';$('lab241-trace').textContent='Nenhuma execução ainda.';$('lab241-flow').textContent='Entrada → decisão → ação → resultado';explained('Execute primeiro.','A execução aparecerá aqui.','Consulte as limitações.','Modifique uma entrada e execute novamente.');$('lab241-model').textContent='Nenhum na demonstração local';$('lab241-explain').open=false;$('lab241-brain').open=false;}
$('lab241-run').addEventListener('click',runSync);$('lab241-reset').addEventListener('click',reset);
$('lab241-export').addEventListener('click',()=>{if(!state.last){setOutput('Execute a experiência antes de exportar.');return;}const blob=new Blob([JSON.stringify(state.last,null,2)],{type:'application/json'});const uri=URL.createObjectURL(blob),a=document.createElement('a');a.href=uri;a.download='agenteia-'+type+'-registro.json';a.click();setTimeout(()=>URL.revokeObjectURL(uri),500);});
if(type==='agente-llm')$('lab241-runtime').addEventListener('change',()=>{$('lab241-backend').hidden=value('lab241-runtime')!=='backend';});
if(type==='diva')$('lab241-kind').addEventListener('change',()=>{$('lab241-amount').disabled=value('lab241-kind')!=='despesas';});
if(type==='diva'){$('lab241-amount').disabled=true;}
})();
