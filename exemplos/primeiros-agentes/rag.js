'use strict';
// Recuperação lexical. Ainda NÃO é RAG completo: não há geração por LLM.
const docs=[{id:'regulamento',texto:'Certificação exige frequência mínima de 70%.'},
            {id:'catalogo',texto:'O curso de IA possui 20 horas.'}];
function buscar(termo){return docs.filter(d=>d.texto.toLowerCase().includes(termo.toLowerCase()));}
console.log(buscar('frequência'));
if(buscar('frequência')[0]?.id!=='regulamento') throw Error('Fonte incorreta');

