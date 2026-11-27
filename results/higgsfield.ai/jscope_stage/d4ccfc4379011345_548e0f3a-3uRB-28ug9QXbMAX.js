!function(){try{var e="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof globalThis?globalThis:"undefined"!=typeof self?self:{},n=(new e.Error).stack;n&&(e._posthogChunkIds=e._posthogChunkIds||{},e._posthogChunkIds[n]="ee5c180a-303f-561c-a8a7-0c589d12777d")}catch(e){}}();import{a as e,n as t,o as n,s as r}from"./548e0f3a-ogOdE30g8Jc45kfx.js";import{Ht as i,Pt as a}from"./548e0f3a-PSrx40HdAYKQsbQF.js";import{gr as o}from"./548e0f3a-WOu4fIxit5_rekPW.js";import{i as s,n as c,r as l,t as u}from"./548e0f3a-9-QLpDuddgvlPtfA.js";import{SO as d,xO as f}from"./548e0f3a-Z02c23EjO5rx6Ir3.js";e(`get-media-scroll-root-m6AtLybd`,(e=>{function r(e){let t=f(e);return t!==document.documentElement&&t!==document.scrollingElement&&t.clientHeight>0&&t.clientHeight<=window.innerHeight&&t.scrollHeight>t.clientHeight?t:null}function i(){return(i=t((()=>{d()})))()}n(e,{n:()=>i,t:()=>r})}));var p=r(`get-media-scroll-root-m6AtLybd`),m;function h(){return(h=t((()=>{m=`html:has([data-explore-layout]) {
  scroll-behavior: auto;
}

[data-explore-layout] {
  container-type: inline-size;
  overflow-anchor: none;
  column-count: auto;
  --explore-columns: 2;
  --explore-gap: var(--spacing-q-400, 1rem);
  --explore-row-gap: var(--spacing-q-400, 1rem);
}

[data-explore-layout='2'] {
  --explore-gap: var(--spacing-q-200, 0.5rem);
}

[data-explore-layout='5'],
[data-explore-layout='6'] {
  --explore-gap: var(--spacing-q-200, 0.5rem);
  --explore-row-gap: var(--spacing-q-200, 0.5rem);
}

[data-explore-layout] > [data-explore-grid] {
  --explore-column-width: calc((100cqw - (var(--explore-columns) - 1) * var(--explore-gap)) / var(--explore-columns));
  position: relative;
  column-gap: var(--explore-gap);
  row-gap: var(--explore-row-gap);
  height: var(--explore-height-2);
}

[data-explore-grid] > [data-explore-item] {
  position: absolute;
  width: var(--explore-column-width);
  left: calc(var(--explore-x-2) * (var(--explore-column-width) + var(--explore-gap)));
  top: var(--explore-y-2);
}

@container (max-width: 24rem) {
  [data-explore-layout] > [data-explore-grid] {
    --explore-columns: 1;
    height: var(--explore-height-1);
  }

  [data-explore-layout] > [data-explore-grid] > [data-explore-item] {
    left: 0;
    top: var(--explore-y-1);
  }
}

/* Three columns already in a narrow pane, where layout 4 would still show two. */
@container (min-width: 32rem) {
  [data-explore-layout='3'] > [data-explore-grid] {
    --explore-columns: 3;
    height: var(--explore-height-3);
  }

  [data-explore-layout='3'] > [data-explore-grid] > [data-explore-item] {
    left: calc(var(--explore-x-3) * (var(--explore-column-width) + var(--explore-gap)));
    top: var(--explore-y-3);
  }
}

@container (min-width: 40rem) {
  :is([data-explore-layout='4'], [data-explore-layout='5'], [data-explore-layout='6']) > [data-explore-grid] {
    --explore-columns: 3;
    height: var(--explore-height-3);
  }

  :is([data-explore-layout='4'], [data-explore-layout='5'], [data-explore-layout='6']) > [data-explore-grid] > [data-explore-item] {
    left: calc(var(--explore-x-3) * (var(--explore-column-width) + var(--explore-gap)));
    top: var(--explore-y-3);
  }
}

@container (min-width: 64rem) {
  [data-explore-layout='4'] > [data-explore-grid] {
    --explore-columns: 4;
    height: var(--explore-height-4);
  }

  [data-explore-layout='5'] > [data-explore-grid] {
    --explore-columns: 5;
    height: var(--explore-height-5);
  }

  [data-explore-layout='4'] > [data-explore-grid] > [data-explore-item] {
    left: calc(var(--explore-x-4) * (var(--explore-column-width) + var(--explore-gap)));
    top: var(--explore-y-4);
  }

  [data-explore-layout='5'] > [data-explore-grid] > [data-explore-item] {
    left: calc(var(--explore-x-5) * (var(--explore-column-width) + var(--explore-gap)));
    top: var(--explore-y-5);
  }
}

/* The home's six columns, from the xl container width; below it the 40rem rule keeps three. */
@container (min-width: 72rem) {
  [data-explore-layout='6'] > [data-explore-grid] {
    --explore-columns: 6;
    height: var(--explore-height-6);
  }

  [data-explore-layout='6'] > [data-explore-grid] > [data-explore-item] {
    left: calc(var(--explore-x-6) * (var(--explore-column-width) + var(--explore-gap)));
    top: var(--explore-y-6);
  }
}
`})))()}function g(e,t){var n,r,i,a,o,u,d;let f=(0,_.useRef)(null),[m,h]=(0,_.useState)(null);(0,_.useLayoutEffect)(()=>{var e;let t=f.current;if(!t||typeof ResizeObserver>`u`)return;let n=()=>{let e=t.getBoundingClientRect(),n=(0,p.t)(t),r=n instanceof HTMLElement?n:null,i=getComputedStyle(t),a={width:e.width,columns:Number.parseInt(i.getPropertyValue(`--explore-columns`))||2,gap:Number.parseFloat(i.columnGap)||8,rowGap:Number.parseFloat(i.rowGap)||16,margin:r?e.top-r.getBoundingClientRect().top+r.scrollTop:e.top+window.scrollY,root:r};h(e=>(e==null?void 0:e.width)===a.width&&e.columns===a.columns&&e.gap===a.gap&&e.rowGap===a.rowGap&&e.margin===a.margin&&e.root===a.root?e:a)};n();let r=new ResizeObserver(n);r.observe(t),t.parentElement&&r.observe(t.parentElement);let i=(e=(0,p.t)(t))==null?window:e;return i.addEventListener(`scroll`,n,{passive:!0}),window.addEventListener(`resize`,n),()=>{r.disconnect(),i.removeEventListener(`scroll`,n),window.removeEventListener(`resize`,n)}},[e.length]);let g=(n=m==null?void 0:m.columns)==null?2:n,v=Math.max(0,(((r=m==null?void 0:m.width)==null?0:r)-(g-1)*((i=m==null?void 0:m.gap)==null?0:i))/g),y=(0,_.useCallback)(t=>{var n,r;let[i,a]=((n=(r=e[t])==null?void 0:r.aspect)==null?`16/9`:n).split(`/`).map(Number);return v*a/i},[e,v]),b=(0,_.useCallback)(t=>e[t].id,[e]),x=e.findIndex(e=>e.id===t),S=(0,_.useCallback)(e=>{let t=s(e);return x<0||t.includes(x)?t:[...t,x].sort((e,t)=>e-t)},[x]),C=m!==null,w={count:e.length,lanes:g,estimateSize:y,getItemKey:b,rangeExtractor:S,gap:(a=m==null?void 0:m.rowGap)==null?16:a,scrollMargin:(o=m==null?void 0:m.margin)==null?0:o,overscan:2,useFlushSync:!1},T=c({...w,initialOffset:()=>{var e,t;return(e=m==null||(t=m.root)==null?void 0:t.scrollTop)==null?0:e},enabled:C&&v>0&&!!(m!=null&&m.root),getScrollElement:()=>{var e;return(e=m==null?void 0:m.root)==null?null:e}}),E=l({...w,enabled:C&&v>0&&!(m!=null&&m.root)}),D=m!=null&&m.root?T:E;return(0,_.useLayoutEffect)(()=>{C&&D.measure()},[C,v,g,D]),{enabled:C,gridRef:f,items:D.getVirtualItems(),totalHeight:D.getTotalSize(),columnWidth:v,gap:(u=m==null?void 0:m.gap)==null?0:u,scrollMargin:(d=m==null?void 0:m.margin)==null?0:d}}var _;function v(){return(v=t((()=>{p.n(),u(),_=i()})))()}function y(e){let t=e.map(()=>({})),n={},r=e.map((e,t)=>{var n;let[r,i]=((n=e.aspect)==null?`16/9`:n).split(`/`).map(Number);return{index:t,ratio:i/r}});for(let e of[1,2,3,4,5,6]){let i=o(r,e,e=>e.ratio).map((n,r)=>{let i=0;return n.forEach((n,a)=>{t[n.index][`--explore-x-${e}`]=r,t[n.index][`--explore-y-${e}`]=`calc(var(--explore-column-width) * ${i} + var(--explore-row-gap) * ${a})`,i+=n.ratio}),`calc(var(--explore-column-width) * ${i} + var(--explore-row-gap) * ${n.length})`});n[`--explore-height-${e}`]=`max(${i.join(`,`)})`}return{style:n,itemStyles:t}}function b(){return(b=t((()=>{})))()}function x({cards:e,children:t,className:n,maxColumns:r=4,keepMountedId:i}){let a=g(e,i),{style:o,itemStyles:s}=(0,S.useMemo)(()=>a.enabled?{style:void 0,itemStyles:[]}:y(e),[e,a.enabled]);return(0,C.jsxs)(`div`,{"data-explore-masonry":``,"data-explore-layout":r,className:n,children:[(0,C.jsx)(`style`,{href:`higgsfield-explore-masonry`,precedence:`default`,children:m}),(0,C.jsx)(`div`,{ref:a.gridRef,"data-explore-grid":``,style:a.enabled?{height:a.totalHeight}:o,children:a.enabled?a.items.map(e=>(0,C.jsx)(`div`,{"data-explore-item":``,style:{width:a.columnWidth,left:e.lane*(a.columnWidth+a.gap),top:e.start-a.scrollMargin},children:t[e.index]},e.key)):t.map((t,n)=>{var r;return(0,C.jsx)(`div`,{"data-explore-item":``,style:s[n],children:t},(r=e[n])==null?void 0:r.id)})})]})}var S,C;function w(){return(w=t((()=>{S=i(),v(),b(),h(),C=a()})))()}export{w as n,x as t};
//# debugId=ee5c180a-303f-561c-a8a7-0c589d12777d

//# chunkId=ee5c180a-303f-561c-a8a7-0c589d12777d