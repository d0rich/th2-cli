import{u as p}from"./asyncData.0726c62f.js";import{a as l,Y as d,j as v,W as c,a7 as m,a8 as y,$ as g,J as x,L as i}from"./entry.50cd521b.js";import{_ as f}from"./nuxt-link.3ca30643.js";/* empty css                    *//* empty css                  *//* empty css                  *//* empty css                 *//* empty css                            *//* empty css                */import"./Icon.vue.0852d47a.js";/* empty css                   *//* empty css                      *//* empty css                            *//* empty css                    *//* empty css                    *//* empty css                    *//* empty css                    *//* empty css                    *//* empty css                    *//* empty css                    *//* empty css                    *//* empty css                     *//* empty css                    *//* empty css                    *//* empty css                   *//* empty css                        *//* empty css                       *//* empty css                    *//* empty css                    *//* empty css                       *//* empty css                    *//* empty css                    *//* empty css                    */import"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs";const ee=l({name:"ContentNavigation",props:{query:{type:Object,required:!1,default:void 0}},async setup(s){const{query:e}=d(s),_=v(()=>{var t;return typeof((t=e.value)==null?void 0:t.params)=="function"?e.value.params():e.value});if(!_.value&&c("dd-navigation").value){const{navigation:t}=m();return{navigation:t}}const{data:o}=await p(`content-navigation-${g(_.value)}`,()=>y(_.value));return{navigation:o}},render(s){const e=x(),{navigation:_}=s,o=n=>i(f,{to:n._path},()=>n.title),t=(n,r)=>i("ul",r?{"data-level":r}:null,n.map(a=>a.children?i("li",null,[o(a),t(a.children,r+1)]):i("li",null,o(a)))),u=n=>t(n,0);return e!=null&&e.default?e.default({navigation:_,...this.$attrs}):u(_)}});export{ee as default};
