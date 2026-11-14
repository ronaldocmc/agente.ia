// Ferramenta somente leitura. Dados inteiramente fictícios de laboratório.
// query é o texto enviado pelo agente, não uma variável do workflow.
const raw = typeof query === 'string' ? query : JSON.stringify(query);
let value;
try { value = JSON.parse(raw); } catch { value = { curso: raw }; }
if (!value || typeof value !== 'object' || Array.isArray(value)) return JSON.stringify({erro:'entrada invalida'});
const curso = String(value.curso || value.course || '').toLowerCase().trim();
const catalogo = {
  'agentes de ia': {nome:'Agentes de IA',vagas:30,situacao:'inscricoes abertas'},
  'banco de dados': {nome:'Banco de Dados',vagas:25,situacao:'lista de espera'},
  'python': {nome:'Python',vagas:20,situacao:'inscricoes encerradas'}
};
if (typeof raw !== 'string' || raw.length > 200) return JSON.stringify({erro:'entrada extensa'});
if (/ignore|ignore as regras|apague|remova|delete|shell|terminal/i.test(raw))
  return JSON.stringify({erro:'instrucoes nao permitidas; informe somente um nome de curso'});
const chaves = Object.keys(catalogo);
const encontrado = chaves.find(k => curso === k || curso.includes(k));
return JSON.stringify(encontrado ? {encontrado:true,...catalogo[encontrado],fonte:'CATALOGO_SINTETICO'} : {encontrado:false,mensagem:'Curso nao encontrado no catalogo sintetico',fonte:'CATALOGO_SINTETICO'});