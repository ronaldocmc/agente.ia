(() => {
'use strict';
const $ = (id) => document.getElementById(id);
const H = (str) => String(str ?? '').replace(/[&<>"']/g,(c)=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const link=(name,url)=>`<a href="${H(url)}">${H(name)}</a>`;
const C={
  conceitos:'conceitos.html',conceitosAgente:'capitulos/02.html',bases:'capitulos/01.html',autonomia:'dimensoes.html',arquitetura:'arquitetura.html',roadmap:'roadmap.html',matriz:'matriz.html',skills:'skills.html',seguranca:'seguranca.html',cerebro:'cerebro.html',tools:'capitulos/06.html',laboratorio:'capitulos/08.html',mcp:'conceitos.html#mcp',rag:'conceitos.html#rag',memoria:'conceitos.html#memoria',agentes:'capitulos/05.html',integracao:'capitulos/03.html',github:'capitulos/07.html',avaliacao:'capitulos/10.html',implementacao:'capitulos/08.html'
};
const T={
 n8n:['n8n','fichas/n8n.html'],python:['Python','capitulos/08.html'],openclaw:['OpenClaw','fichas/openclaw.html'],hermes:['Hermes Agent','fichas/hermes-agent.html'],crewai:['CrewAI','fichas/crewai.html'],adk:['Google ADK','fichas/google-adk.html'],agents:['OpenAI Agents SDK','fichas/openai-agents-sdk.html'],pydantic:['PydanticAI','fichas/pydanticai.html'],langgraph:['LangGraph','fichas/langgraph.html'],maf:['Microsoft Agent Framework','fichas/microsoft-agent-framework.html'],mastra:['Mastra','fichas/mastra.html'],postgres:['PostgreSQL','fichas/postgresql.html'],pgvector:['pgvector','fichas/pgvector.html'],qdrant:['Qdrant','fichas/qdrant.html'],llamaindex:['LlamaIndex Workflows','fichas/llamaindex-workflows.html'],haystack:['Haystack Agents','fichas/haystack-agents.html'],flowise:['Flowise','fichas/flowise.html'],dify:['Dify','fichas/dify.html'],temporal:['Temporal','fichas/temporal.html'],mcp:['MCP','fichas/mcp.html'],a2a:['A2A','fichas/a2a.html'],minio:['MinIO','fichas/minio.html'],whisper:['Whisper','tecnologias/multimodalidade-e-canais.html'],redis:['Redis','fichas/redis.html'],neo4j:['Neo4j','fichas/neo4j.html']
};
for(const e of (window.AGENTEIA_SEMANTICA?.entities||[])){if(e.type==='tecnologia')T[e.id.slice(2)]=[e.label,e.href];}
const PROFILES={
 observar:{name:'Observar.IA — Observatório Inteligente',objective:'Receber fontes, verificar evidências e preparar publicações para curadoria.',flags:['docs','multi','channels','approval','automation'],example:'Receber uma notícia, conferir sua procedência, registrar evidências e preparar um boletim para o curador.',case:'estudos/observar.html',skill:'verificar-fonte-observar'},
 assistente:{name:'Assistente pessoal',objective:'Organizar tarefas, documentos e compromissos sob controle do usuário.',flags:['memory','channels','skills','approval'],example:'Receber uma mensagem, consultar compromissos, propor horários e solicitar confirmação.',case:'estudos/assistente-pessoal.html',skill:'preparar-compromisso'},
 escritorio:{name:'Escritório virtual da FCT/UNESP',objective:'Apoiar gestores na triagem documental, processos e elaboração de minutas.',flags:['docs','multi','memory','approval','skills'],example:'Analisar uma solicitação, recuperar normas, preparar minuta e encaminhar para aprovação.',case:'estudos/escritorio.html',skill:'preparar-parecer'},
 varejo:{name:'Varejo/CRM',objective:'Integrar dados operacionais e apoiar atendimento, estoque e recomendações.',flags:['automation','multi','docs'],example:'Consultar estoque e vendas, sugerir reposição e solicitar aprovação de compra.',case:'estudos/varejo.html',skill:'analisar-reposicao'},
 educacao:{name:'Assistente educacional',objective:'Consultar materiais didáticos com rastreabilidade e apoiar docentes e estudantes.',flags:['docs','approval','skills'],example:'Responder a dúvida citando o material da disciplina e sinalizar lacunas.',case:'capitulos/09.html',skill:'responder-com-fontes'},
 custom:{name:'Projeto autoral',objective:'Desenvolver uma aplicação de agentes com escopo e controles definidos.',flags:[],example:'Receber uma tarefa, escolher a menor solução adequada e validar o resultado antes de agir.',case:'roadmap.html',skill:'procedimento-do-projeto'}
};
const ROLES=[
 ['01','Fundamentos da IA e agentes','Diferenciar LLM, assistente, agente, ferramenta e automação.','bases','Identificar o que poderia ser resolvido por regras, IA generativa ou agente.','Mapa de atores, problema e limites.'],
 ['02','Definição do problema','Definir objetivo, entradas, saídas, atores, riscos e critérios de aceite.','conceitosAgente','Especificar cenário positivo, falhas e uma decisão que não deve ser delegada ao modelo.','Requisitos, casos de uso e critérios de sucesso.'],
 ['03','Planejamento da solução','Desenhar responsabilidades, eventos, decisão, estado, interfaces e aprovações.','arquitetura','Desenhar fluxo simples antes de decompor em múltiplos agentes.','Arquitetura candidata e justificativas de escolha.'],
 ['04','Dados e conhecimento','Definir fontes, qualidade, recuperação, permissões e persistência.','tools','Criar base de teste com documentos e consultas rastreáveis.','Esquema de dados e teste de recuperação.'],
 ['05','Construção do agente','Implementar ferramentas, procedimentos e validação de resultados.','implementacao','Construir uma função testável antes de adicionar planejamento autônomo.','Protótipo com testes e contratos.'],
 ['06','Integração e automação','Integrar APIs, eventos, canais e serviços externos.','integracao','Simular entrada por Web/API e persistência antes de conectar contas reais.','Fluxo ponta a ponta com tratamento de erro.'],
 ['07','Avaliação, segurança e governança','Executar baselines, testes de abuso, autorização, métricas e revisão.','seguranca','Testar uma tentativa de prompt injection e uma chamada de ferramenta sem permissão.','Matriz de riscos, relatório de testes e critérios de aprovação.'],
 ['08','Aplicação e impacto','Implantar por incrementos, observar resultados e revisar continuamente.','roadmap','Comparar produtividade, precisão, custo, riscos e intervenção humana.','Plano piloto, métricas, decisão de evolução.']
];
const selectedFlag=(name,flags)=>flags.has(name);
function config(){let profile=PROFILES[$('project').value]||PROFILES.custom;return {profile,level:$('level').value,stack:$('stack').value,goal:$('objective').value.trim().slice(0,400),flags:new Set([...document.querySelectorAll('.adapt-checks input:checked')].map(x=>x.value))};}
function recommend(c){
 let f=c.flags; let list=[]; let add=(k,why)=>{if(T[k] && !list.some(x=>x.k===k))list.push({k,why})};
 if(c.stack==='visual'){add('n8n','Integração visual e processos repetíveis.');add('flowise','Protótipos visuais com LLM e recuperação.');}
 else if(c.stack==='typescript'){add('mastra','Desenvolvimento de agentes em TypeScript.');add('n8n','Integrações operacionais e webhooks.');}
 else if(c.stack==='runtime'){add('openclaw','Runtime de assistente com canais e ferramentas.');add('hermes','Runtime de agente com skills e trabalho local.');}
 else if(c.stack==='python'){add('pydantic','Agentes Python com contratos tipados.');add('adk','Agentes e workflows programáveis.');}
 else {add('python','Baseline determinístico, boa opção inicial.');add('n8n','Integração e eventos, caso necessários.');}
 if(selectedFlag('channels',f)){add('openclaw','Canais, sessões e ferramentas de assistente.');add('n8n','Webhooks e integrações entre aplicações.');}
 if(selectedFlag('multi',f)){add('crewai','Papéis especializados e tarefas colaborativas.');add('adk','Coordenação programável e workflows.');}
 if(selectedFlag('memory',f)){add('postgres','Estado, usuários e trilha transacional.');add('langgraph','Candidato a fluxos com retomada e checkpoints.');}
 if(selectedFlag('docs',f)){add('pgvector','Busca vetorial integrada a dados relacionais.');add('llamaindex','Workflows e recuperação de documentos.');}
 if(selectedFlag('automation',f)){add('n8n','Agenda, webhooks e processos previsíveis.');}
 if(selectedFlag('approval',f)){add('postgres','Registro durável de aprovações e identidade.');add('temporal','Candidato a fluxos de longa duração com retentativas.');}
 if(selectedFlag('skills',f)){add('hermes','Documentos de procedimentos sob demanda.');add('openclaw','Skills e canais integrados.');}
 if(selectedFlag('local',f)){add('hermes','Candidato para execução local, exigindo sandbox e políticas.');add('postgres','Armazenamento sob gestão própria.');}
 if(!list.length)add('agents','Agente simples com ferramentas, após baseline determinístico.');
 const d=window.AGENTEIA_SEMANTICA?.implantacao_custos, req=window.AGENTEIA_REQUISITOS;
 if(!d||!req)return list;
 const goals={assistente:'personal',escritorio:'team',observar:'app',varejo:'automation',educacao:'app',custom:'app'};
 const group=goals[c.profile===PROFILES.assistente?'assistente':Object.keys(PROFILES).find(k=>PROFILES[k]===c.profile)]||'app';
 const own=$('adapt-env').value==='own',cloud=$('adapt-env').value==='cloud';
 const required=[...(own?['proprio']:[]),...($('adapt-free').checked?['sem_assinatura']:[]),...($('adapt-local').checked?['local']:[]),...($('adapt-offline').checked?['offline']:[])];
 const alias={hermes:'hermes-agent',agents:'openai-agents-sdk',adk:'google-adk',pydantic:'pydanticai',grok:'grok-bot'};
 const idFor=k=>'t:'+(alias[k]||k);
 const pool=d.goal_candidates[group]||[];
 const styles={visual:['Visual / baixo código'],python:['Programação Python','Programação'],typescript:['Programação'],runtime:['Configuração de runtime','Configuração de agentes','Configuração e integração']};
 let candidates=pool.map(id=>({k:id.slice(2),why:d.profiles[id].finalidade,profile:d.profiles[id],id})).filter(x=>T[x.k]);
 if(styles[c.stack])candidates=candidates.filter(x=>styles[c.stack].includes(x.profile.modo));
 c.requirements=required;c.candidateReports=candidates.map(x=>({...x,result:required.length?req.evaluate(x.id,required):'Candidato pelo objetivo'}));
 c.candidateReports.sort((a,b)=>Number(b.id==='t:grok-bot'&&cloud)-Number(a.id==='t:grok-bot'&&cloud));
 let eligible=c.candidateReports.filter(x=>!['Não atende','Informação pendente'].includes(x.result));
 c.auxiliary=list.filter(x=>!pool.includes(idFor(x.k)));
 return eligible.map(x=>({k:x.k,why:x.why+' — '+x.result}));
}
function stageContent(n,c,rec){let f=c.flags,items=[];
 switch(n){
 case 1:items=[['Conceitos essenciais',C.conceitosAgente],['Dimensões dos agentes',C.autonomia],['Cérebro do agente',C.cerebro]];break;
 case 2:items=[['Definição de problema e baselines',C.bases],['Matriz de decisão',C.matriz],['Estudo de caso',c.profile.case]];break;
 case 3:items=[['Arquitetura de referência',C.arquitetura],['Comparador de tecnologias',C.matriz],['Tipos de agentes',C.autonomia]];break;
 case 4:items=[['RAG e ferramentas',C.tools],['Memória e estado',C.conceitos],['Catálogo de dados e RAG','tecnologias/memoria-dados-e-rag.html']];break;
 case 5:items=[['Implementação e laboratórios',C.implementacao],['Skill: do conceito ao SKILL.md',C.skills],['Frameworks e SDKs',C.matriz]];break;
 case 6:items=[['Automação × orquestração',C.integracao],['Protocolo MCP',C.mcp],['Skills reutilizáveis',C.skills]];break;
 case 7:items=[['Segurança e guardrails',C.seguranca],['Governança e avaliação',C.avaliacao],['Riscos de skills de terceiros',C.skills+'#seguranca']];break;
 default:items=[['Roadmap completo',C.roadmap],['Estudo de caso',c.profile.case],['Comparação de tecnologias',C.matriz]];
 }
 if(n===4 && !f.has('docs'))items=[['Dados, estado e qualidade',C.tools],['Quando não utilizar RAG',C.matriz],['Fontes e rastreabilidade',C.conceitos]];
 if(n===5 && !f.has('skills'))items[1]=['Quando uma skill agrega valor',C.skills];
 return items;
}
function stageTools(n,c,rec){let keys=n===1?[]:n===2?[]:n===3?rec.slice(0,4):n===4?rec.filter(x=>['pgvector','postgres','qdrant','llamaindex','langgraph'].includes(x.k)):n===5?rec.filter(x=>['agents','pydantic','adk','crewai','hermes','openclaw','mastra','flowise'].includes(x.k)):n===6?rec.filter(x=>['n8n','openclaw','hermes','temporal'].includes(x.k)):n===7?rec.filter(x=>['postgres','temporal','langgraph'].includes(x.k)):rec.slice(0,3);return keys.slice(0,5);}
function reset(){ $('project').value='observar'; $('level').value='iniciante'; $('stack').value='indiferente'; $('objective').value='';$('adapt-env').value='any';for(const id of ['adapt-free','adapt-local','adapt-offline'])$(id).checked=false; const wanted=new Set(PROFILES.observar.flags);document.querySelectorAll('.adapt-checks input').forEach(x=>x.checked=wanted.has(x.value)); $('adapt-result').innerHTML='<p>Escolha seu cenário e clique em <strong>Gerar meu percurso</strong>. O plano aparecerá aqui.</p>'; }
function render(e){if(e)e.preventDefault();let c=config(), rec=recommend(c),f=c.flags;let beginner=c.level==='iniciante';let notice=`O plano é uma hipótese didática. Confirme requisitos funcionais, custo, maturidade, permissões, licença e versões de cada tecnologia.`;
 let html=`<div class="adapt-result-head"><h2>Seu percurso: ${H(c.profile.name)}</h2><p><strong>Objetivo:</strong> ${H(c.goal||c.profile.objective)}</p><p><strong>Exemplo contínuo:</strong> ${H(c.profile.example)}</p><div>${[...f].map(x=>`<span class="adapt-chip">${H(({docs:'Documentos e RAG',memory:'Memória',multi:'Multiagentes',channels:'Canais',automation:'Automação',skills:'Skills',approval:'Aprovação humana',local:'Execução local'})[x])}</span>`).join('')}</div><p>${beginner?'Percurso guiado: priorizar conceitos e laboratórios simulados.':c.level==='avancado'?'Percurso de engenharia: acrescentar contratos, testes, rastreabilidade e baselines.':'Percurso aplicado: construir pequenas integrações e comparar alternativas.'}</p></div>`;
 html+=`<h2 >Tecnologias candidatas (não são obrigatórias)</h2><p>Comece por componentes simples. Use as opções abaixo somente quando o requisito justificar:</p><ul class="adapt-tech">${rec.slice(0,10).map(x=>`<li>${link(T[x.k][0],T[x.k][1])}: ${H(x.why)}</li>`).join('')}</ul>`;
 if(c.candidateReports){html+='<h3>Por que estas alternativas?</h3><p>As opções são avaliadas conforme os requisitos marcados. Via integração exige os componentes descritos na ficha; informação pendente não é incompatibilidade.</p>';if(!rec.length)html+='<p><strong>Nenhuma alternativa com evidência suficiente para todos os critérios.</strong> Revise as restrições ou consulte as fichas pendentes antes de escolher.</p>';for(const x of c.candidateReports){html+='<div class="req-summary"><strong>'+link(T[x.k][0],T[x.k][1])+' — '+H(x.result)+'</strong><p>'+H(x.profile.instalacao_detalhada)+'</p>';for(const k of c.requirements){html+='<p><strong>'+H(window.AGENTEIA_REQUISITOS.labels[k])+': '+H(x.profile.estados[k])+'</strong> — '+H(x.profile.condicoes[k])+'</p>'}html+='</div>'}if(c.auxiliary.length)html+='<p><strong>Componentes auxiliares a investigar separadamente:</strong> '+c.auxiliary.map(x=>link(T[x.k][0],T[x.k][1])).join(' · ')+'. Não foram aprovados automaticamente pelos filtros.</p>';html+='<p><a href="ciclo-engenharia.html">Consultar o ciclo de engenharia de nove etapas</a></p>';}
if(f.has('multi'))html+='<p><strong>Critério:</strong> compare um agente único com vários especialistas; só mantenha múltiplos agentes se houver ganho mensurável.</p>';
 if(f.has('docs'))html+='<p><strong>Critério RAG:</strong> comece pela recuperação lexical; avalie vetores e reranking com conjunto de perguntas e citações verificáveis.</p>';
 if(f.has('skills'))html+='<p><strong>Critério de skills:</strong> documente um procedimento reutilizável e valide políticas e ferramentas fora do texto da skill.</p>';
 html+='<h2 >As oito etapas recomendadas</h2>';
 for(let i=0;i<ROLES.length;i++){
  let [num,title,desc,core,activity,deliver]=ROLES[i], resources=stageContent(i+1,c,rec), tools=stageTools(i+1,c,rec);
  let example=i===4?`Implemente uma primeira função para “${c.profile.skill}” com entradas e saídas controladas.`:i===6?'Aplique um teste de acesso negado e outro com conteúdo externo malicioso.':i===3?(f.has('docs')?'Use documentos sintéticos e compare recuperação lexical e vetorial.':'Registre o estado mínimo e os dados exigidos sem incluir RAG por obrigação.'):activity;
  html+=`<section class="adapt-stage" id="percurso-${i+1}"><h3><span class="adapt-number">${num}</span>${H(title)}</h3><p>${H(desc)}</p><p><strong>Exemplo / atividade:</strong> ${H(example)}</p><p><strong>Conceitos e laboratórios:</strong> ${resources.map(x=>link(...x)).join(' · ')}</p>${tools.length?`<p><strong>Tecnologias relacionadas:</strong> ${tools.map(x=>link(T[x.k][0],T[x.k][1])).join(' · ')}</p>`:''}<p class="adapt-done"><strong>Entregável:</strong> ${H(deliver)}</p><p><a href="roadmap.html#etapa-${i+1}">Ver etapa completa do roadmap →</a></p></section>`;
 }
 html+=`<div class="adapt-warning"><strong>Controle transversal:</strong> autenticação, segregação de dados, permissões, validação de ferramenta, guardrails, observabilidade e aprovação para ações críticas não podem depender apenas do prompt ou de uma skill. ${H(notice)} <a href="seguranca.html">Estudar segurança</a>.</div>`;
 html+='<div class="adapt-output-actions"><button type="button" id="adapt-copy">Copiar resumo</button><button class="secondary-btn" type="button" id="adapt-print">Imprimir percurso</button><a href="skills.html">Aprofundar skills →</a></div>';
 $('adapt-result').innerHTML=html;
 $('adapt-copy').addEventListener('click',()=>{let text=`Agente.IA — Roadmap adaptativo\nProjeto: ${c.profile.name}\nObjetivo: ${c.goal||c.profile.objective}\nTecnologias candidatas:\n${rec.map(x=>'- '+T[x.k][0]+': '+x.why).join('\n')}\nEtapas:\n${ROLES.map(r=>r[0]+'. '+r[1]+' — '+r[5]).join('\n')}\nRevisão: validar versões, políticas e segurança.`;if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(text).then(()=>{ $('adapt-copy').textContent='Resumo copiado'; }).catch(()=>fallbackCopy(text))}else fallbackCopy(text)});
 $('adapt-print').addEventListener('click',()=>window.print());
 function fallbackCopy(text){let area=document.createElement('textarea');area.value=text;area.style.position='fixed';area.style.left='-9999px';document.body.appendChild(area);area.select();let ok=false;try{ok=document.execCommand('copy')}catch(e){}area.remove();$('adapt-copy').textContent=ok?'Resumo copiado':'Selecione e copie o texto do plano';}
 $('adapt-result').focus({preventScroll:true});$('adapt-result').scrollIntoView({behavior:'smooth',block:'start'});
}
$('adapt-form').addEventListener('submit',render);$('adapt-reset').addEventListener('click',reset);$('project').addEventListener('change',()=>{let p=PROFILES[$('project').value];let want=new Set(p.flags);document.querySelectorAll('.adapt-checks input').forEach(x=>x.checked=want.has(x.value));});reset();
})();