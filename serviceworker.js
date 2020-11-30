const cacheName='assets';
const cacheAssets=[
    './',
    'static/css/site.css',
    'static/css/boostrap.min.css',
    'static/css/matrixamode.css',
    'static/css/darkmode.css',
    'static/js/jquery.js',
    'static/js/main.js',
    'static/js/page_renderer.js',
    'static/js/profile.js',
    'static/js/profileupload.js',
    'static/js/friend_profile.js',
    'static/js/friendreq.js',
    'static/js/login.js',
    'static/js/storydetail.js',
    'static/js/likecomment.js',
    'static/js/signup.js',
    'static/js/sw.js',



]
 
self.addEventListener("install", async (e) => {
  const cache = await caches.open(cacheName);
  await cache.addAll(cacheAssets);
  return self.skipWaiting()
});
self.addEventListener("activate", (e) => {
  self.clients.claim();
});
self.addEventListener("fetch", async (e) => {
  const req = e.request;
  const url = new URL(req.url);
  if (url.origin == location.origin) {
    e.respondWith(cacheFirst(req));
  } else {
    e.respondWith(networkAndCache(req));
  }
});

const cacheFirst = async (req) => {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(req);
  return cached || fetch(req);
};
const networkAndCache = async (req) => {
  const cache = await caches.open(cacheName);
  try {
    const fresh = await fetch(reg);
    await cache.put(req, fresh.clone());
    return fresh;
  } catch (e) {
    const cached = await cache.match(req);
    return cached;
  }
};