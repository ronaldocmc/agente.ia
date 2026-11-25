'use strict';
// DIVA didática: memória estruturada em variáveis locais.
const dados={tarefas:[{titulo:'Preparar aula',concluida:false}],despesas:[{valor:45},{valor:20}]};
function dia(d){return {pendentes:d.tarefas.filter(t=>!t.concluida).length,
                  despesas:d.despesas.reduce((acc,x)=>acc+x.valor,0)};}
console.log(dia(dados));
if(dia(dados).despesas!==65||dia(dados).pendentes!==1) throw Error('Resumo incorreto');

