import{_ as C}from"./nuxt-link.d93ec307.js";import{_ as O}from"./Shape.vue.6d80f961.js";/* empty css                  */import{a as p,j as x,o as c,c as d,w as u,q as b,u as S,I as B,b as r,p as g,ah as _,e as T,v as D,x as w,f as E,m as I,W as k,l as y,D as L}from"./entry.41cd5b6b.js";/* empty css                */const P={key:0,class:"d-focus-hl__hl--negative-tile"},$={key:2,class:"d-focus-hl__hl--negative-list-item"},H=T("div",{class:"d-focus-hl__hl--negative-list-item"},null,-1),M={name:"DWrapShape"},W=p({...M,props:{linkExact:Boolean,noPassiveLink:Boolean,active:Boolean,variant:{type:String,default:"negative-tile"},tag:{type:String,default:"div"},colorClass:{type:[String,Object],default:"bg-red-600"}},setup(e){const t=e,a=x(()=>t.to||t.href?C:t.tag);return(s,l)=>{const n=O;return c(),d(n,null,{default:u(()=>[(c(),d(b(S(a)),B(t,{class:["d-focus-hl",{"d-focus-hl--exact":e.linkExact,"d-focus-hl--not-exact":!e.linkExact,"d-focus-hl--no-passive-link":e.noPassiveLink,"d-focus-hl--active":e.active}]}),{default:u(()=>[e.variant==="negative-tile"?(c(),r("div",P)):e.variant==="list-item"?(c(),r("div",{key:1,class:g(["d-focus-hl__hl--list-item",e.colorClass])},null,2)):e.variant==="negative-list-item"?(c(),r("div",$)):e.variant==="composite-list-item"?(c(),r(_,{key:3},[T("div",{class:g(["d-focus-hl__hl--list-item",e.colorClass])},null,2),H],64)):D("",!0),w(s.$slots,"default")]),_:3},16,["class"]))]),_:3})}}}),j={name:"DBtn"},G=p({...j,props:{to:{type:String,default:void 0},href:{type:String,default:void 0},exact:Boolean,noPassiveHighlight:Boolean,active:Boolean,noRotate:Boolean,tag:{type:String,default:"button"},highlight:{type:String,default:void 0},colorClass:[String,Object],textTransform:{type:String,default:"uppercase"}},setup(e){const t=e,a=x(()=>t.to||t.href?C:t.tag);return(s,l)=>{const n=W;return c(),d(b(S(a)),B({class:["d-btn",{"-rotate-6":!e.noRotate,uppercase:e.textTransform==="uppercase",capitalize:e.textTransform==="capitalize",lowercase:e.textTransform==="lowercase"}]},t),{default:u(()=>[E(n,{variant:e.highlight,"link-exact":e.exact,"no-passive-link":e.noPassiveHighlight,"color-class":e.colorClass,active:e.active},{default:u(()=>[w(s.$slots,"default")]),_:3},8,["variant","link-exact","no-passive-link","color-class","active"])]),_:3},16,["class"])}}}),z=(e,t,a=500)=>{{let l=a/100;const n=()=>{var i;(i=e.value)!=null&&i.isConnected?t():l>0&&(setTimeout(n,100),l--)};I(()=>{n()})}},N=()=>({showContentTree:k("layout/docs/showContentTree",()=>!1),tableOfContents:k("layout/docs/tableOfContents",()=>null)}),J=e=>{const{tableOfContents:t}=N(),a=new Map,s=y(null),l=y([]);function n(){var h;s.value?s.value.disconnect():s.value=new IntersectionObserver(f=>{f.forEach(o=>{a.set(o.target.id,o.isIntersecting)}),l.value=Array.from(a.keys()).filter(o=>a.get(o))});const i=f=>{f.forEach(o=>{var m;const v=document.getElementById(o.id);v&&((m=s.value)==null||m.observe(v)),o.children&&i(o.children)})};i(((h=t.value)==null?void 0:h.links)??[])}return L(t,()=>{setTimeout(()=>{n()},100)}),z(e,()=>{n()}),l};export{G as _,J as a,N as u};
