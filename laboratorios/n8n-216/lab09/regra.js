function avaliar(p){return !/^P[0-9]{3}$/.test(p.sku||'')?{status:'invalido'}:p.sku==='P001'?{status:'ok',quantidade:8,fonte:'estoque_sintetico_v1'}:p.sku==='P002'?{status:'ok',quantidade:0,fonte:'estoque_sintetico_v1'}:{status:'nao_encontrado'};}
if(typeof module!=="undefined")module.exports=avaliar;
