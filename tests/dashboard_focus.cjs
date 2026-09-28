// Minimal DOM fixture; real-browser verification complements this regression.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(process.argv[2], 'utf8');
let document;
class Element {
  constructor(tag) { this.tagName=tag; this.children=[]; this.dataset={}; this.attributes={}; this.textContent=''; }
  setAttribute(key,value) { this.attributes[key]=value; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { if(this.children.includes(document.activeElement)) document.activeElement=document.body; this.children=[...nodes]; }
  contains(el) { return this.children.includes(el); }
  focus() { document.activeElement=this; }
}
const elements=new Map();
document={body:new Element('body'),activeElement:null,createElement:tag=>new Element(tag),querySelector:selector=>{if(!elements.has(selector)) elements.set(selector,new Element('div')); return elements.get(selector);}};
document.activeElement=document.body;
const context=vm.createContext({document,URLSearchParams,location:{hash:'',pathname:'/'},history:{replaceState(){}},setInterval(){},setTimeout(){},console});
vm.runInContext(source,context);
const tasks=[{task_id:'a',contract_revision:1},{task_id:'b',contract_revision:1}];
function render(items) { context.fixtureTasks=items; vm.runInContext('renderTasks(fixtureTasks)',context); }
render(tasks);
const list=document.querySelector('#tasks'), original=list.children[1];
original.focus(); render(tasks);
assert.equal(document.activeElement,original,'unchanged poll preserves the actual focused node');
render([...tasks].reverse());
assert.equal(document.activeElement,original,'reorder restores the same retained node');
assert.equal(list.children[0],original);
render([tasks[0]]);
assert.equal(document.activeElement,document.querySelector('#pause'),'removed task recovers to polling control');
document.querySelector('#filter').focus(); render(tasks);
assert.equal(document.activeElement,document.querySelector('#filter'),'poll must not steal external focus');
assert.equal(list.children[0].attributes['aria-pressed'],'false');
vm.runInContext("selected='a'",context); render(tasks);
assert.equal(list.children[0].attributes['aria-pressed'],'true');
console.log('Dashboard retained/reordered/removed/external focus and selection passed');
