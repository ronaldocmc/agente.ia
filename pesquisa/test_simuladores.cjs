const assert=require('node:assert/strict');const a=require('../assets/simuladores.js');
let n=0;function test(name,fn){fn();console.log('OK',name);n++;}
const run=(id,x={})=>a.evaluate(id,{...a.defaults(id),...x});
test('S01 default US$16',()=>assert.equal(run('s01').metrics[2][1],16));
test('S01 double agents',()=>assert.equal(run('s01',{agents:2}).monthlyBRL,176));
test('S01 retry 25%',()=>assert.equal(run('s01',{retry:25}).metrics[0][1],5000));
test('S02 budget',()=>assert.deepEqual(run('s02').scenarios.map(x=>x.withinBudget),[true,false,false,false]));
test('S02 zero amortization rejected',()=>assert.throws(()=>run('s02',{life:0})));
test('S03 cache doubles',()=>assert.equal(run('s03',{sessions:4}).metrics[1][1],4));
test('S03 positive memory',()=>assert.ok(run('s03').metrics[3][1]>7));
test('S04 sequence and parallel',()=>{assert.equal(run('s04').metrics[0][1],22);assert.equal(run('s04').metrics[1][1],7)});
test('S04 two slots',()=>assert.equal(run('s04',{slots:2}).metrics[1][1],12));
test('S05 fragments',()=>assert.equal(run('s05').metrics[0][1],5000));
test('S05 invalid overlap',()=>assert.throws(()=>run('s05',{overlap:500})));
test('S05 higher top-k',()=>assert.equal(run('s05',{top:10}).metrics[3][1],5000000));
console.log(n+' testes aprovados');
