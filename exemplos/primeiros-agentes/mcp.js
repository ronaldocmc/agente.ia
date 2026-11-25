'use strict';
// Emulação didática de chamada JSON-RPC. NÃO conecta servidor MCP real.
const ferramentas={listar_cursos:()=>[{id:'C01',nome:'IA'}]};
function responder(mensagem){
 if(mensagem.method!=='tools/call') return {jsonrpc:'2.0',id:mensagem.id,error:{code:-32601,message:'Método desconhecido'}};
 const fn=ferramentas[mensagem.params?.name];
 if(!fn) return {jsonrpc:'2.0',id:mensagem.id,error:{code:-32602,message:'Ferramenta desconhecida'}};
 return {jsonrpc:'2.0',id:mensagem.id,result:fn()};
}
console.log(responder({jsonrpc:'2.0',id:1,method:'tools/call',params:{name:'listar_cursos'}}));
if(!responder({jsonrpc:'2.0',id:2,method:'tools/call',params:{name:'inexistente'}}).error) throw Error('Teste falhou');

