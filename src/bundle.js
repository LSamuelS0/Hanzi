const fs=require('fs'),path=require('path');
const root=process.argv[2],entry=process.argv[3],out=process.argv[4];
const mods={};let id=0;const ids={};
function resolve(from,req){let p=path.resolve(path.dirname(from),req);
  for(const c of [p+'.js',path.join(p,'index.js'),p])if(fs.existsSync(c)&&fs.statSync(c).isFile())return c;throw new Error('cannot resolve '+req+' from '+from);}
function add(file){if(ids[file]!=null)return ids[file];const my=ids[file]=id++;let src=fs.readFileSync(file,'utf8');
  src=src.replace(/require\("(\.[^"]+)"\)/g,(m,r)=>`__req(${add(resolve(file,r))})`);mods[my]=src;return my;}
const e=add(path.resolve(root,entry));
let o='/*! Hanzi Writer v3.7.3 | MIT License | (c) David Chanin | https://github.com/chanind/hanzi-writer */\n(function(){var __m={},__c={};function __req(i){if(__c[i])return __c[i].exports;var module={exports:{}};__c[i]=module;__m[i](module,module.exports);return module.exports;}\n';
for(const k in mods)o+=`__m[${k}]=function(module,exports){\n${mods[k]}\n};\n`;
o+=`var HW=__req(${e});window.HanziWriter=HW.default||HW;})();\n`;
fs.writeFileSync(out,o);console.log('modules',id,'bytes',o.length);
