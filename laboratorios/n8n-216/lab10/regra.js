function avaliar(p){return {status:['inscricao','certificado','outro'].includes(p.categoria)&&Number.isFinite(p.confianca)&&p.confianca>=0.8&&p.confianca<=1?'ok':'revisao'};}
if(typeof module!=="undefined")module.exports=avaliar;
