function avaliar(p){return {status:p.id&&p.nome&&typeof p.email==='string'&&/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(p.email)&&p.curso?'recebido':'invalido',id:p.id};}
if(typeof module!=="undefined")module.exports=avaliar;
