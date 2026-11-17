function avaliar(p){return {status:p.action==='publicar'&&p.role==='editor'&&Number.isInteger(p.version)&&p.version===p.approvedVersion?'ok':'negado'};}
if(typeof module!=="undefined")module.exports=avaliar;
