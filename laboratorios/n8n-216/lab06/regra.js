function avaliar(p){const a=Date.parse(p.inicio),b=Date.parse(p.fim);return {status:Number.isFinite(a)&&Number.isFinite(b)&&b>a&&b-a<=7200000?'proposta_valida':'invalido'};}
if(typeof module!=="undefined")module.exports=avaliar;
