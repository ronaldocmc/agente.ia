'use strict';
// Comparação sintética de duas estratégias. NÃO representa benchmark real.
const casos=[{vagas:10},{vagas:0},{vagas:5}];
const estrategiaA=c=>c.vagas>0?'disponivel':'indisponivel';
const estrategiaB=c=>c.vagas>=5?'disponivel':'indisponivel';
const resultados=casos.map(c=>({vagas:c.vagas,A:estrategiaA(c),B:estrategiaB(c)}));
console.table(resultados);
if(resultados.length!==3) throw Error('Amostra incompleta');

