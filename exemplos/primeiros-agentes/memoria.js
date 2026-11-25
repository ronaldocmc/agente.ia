'use strict';
// Memória em estado local. Persistência permanente não é demonstrada aqui.
class Memoria {
  constructor(){this.estado=new Map();}
  lembrar(sessao,chave,valor){const s=this.estado.get(sessao)||{}; s[chave]=valor; this.estado.set(sessao,s);}
  recuperar(sessao,chave){return this.estado.get(sessao)?.[chave] ?? null;}
}
const m=new Memoria(); m.lembrar('A','area','IA');
console.log(m.recuperar('A','area'));
if(m.recuperar('B','area')!==null) throw Error('Memória cruzada');

