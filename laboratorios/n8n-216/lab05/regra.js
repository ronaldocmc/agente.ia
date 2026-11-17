function avaliar(p){return {status:typeof p.id==='string'&&/^REQ-[0-9]+$/.test(p.id)&&/^C[0-9]{3}$/.test(p.curso||'')?'ok':'invalido',id:p.id};}
if(typeof module!=="undefined")module.exports=avaliar;
