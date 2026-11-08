// Optional authorised URL-only observer. Does not collect headers, bodies, prompts or responses.
Java.perform(function () {
  const seen = {};
  function emit(source, value) {
    try {
      const url = String(value);
      if (!/^https?:\/\//i.test(url) && !/^wss?:\/\//i.test(url)) return;
      if (seen[url]) return;
      seen[url] = true;
      send({type:"url-destination",source:source,url:url,observed_at:new Date().toISOString()});
    } catch (_) {}
  }
  try {
    const U=Java.use("java.net.URL"), init=U.$init.overload("java.lang.String");
    init.implementation=function(v){emit("java.net.URL",v);return init.call(this,v);};
  } catch (_) {}
  try {
    const U=Java.use("java.net.URI"), init=U.$init.overload("java.lang.String");
    init.implementation=function(v){emit("java.net.URI",v);return init.call(this,v);};
  } catch (_) {}
  try {
    const B=Java.use("okhttp3.Request$Builder"), url=B.url.overload("java.lang.String");
    url.implementation=function(v){emit("okhttp3.Request.Builder.url",v);return url.call(this,v);};
  } catch (_) {}
  send({type:"observer-ready",note:"Only URL destinations are collected."});
});
