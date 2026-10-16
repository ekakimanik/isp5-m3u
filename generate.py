import re, urllib.request

UA = "Mozilla/5.0 (Linux; Android 16; RMX3853) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Mobile Safari/537.36"
B = "http://10.100.100.10"

def get(path):
    req = urllib.request.Request(B + path, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "ignore")

page = get("/web-player/watch/sf-1-t-sports-l-sports-1")
home = get("/")

paths = []
for p in re.findall(r"/_sf-node-media/[^\"' <>]+/index\.m3u8", page):
    if p not in paths:
        paths.append(p)

logos = {}
for base, ext in re.findall(r"/channel-logos/([^\"' <>/]+?)\.(png|jpg|jpeg|webp)", home):
    logos[base] = "/channel-logos/%s.%s" % (base, ext)

lines = ["#EXTM3U"]
for p in paths:
    slug = p.split("/")[-2]
    name = re.sub(r"^sf-\d+-", "", slug)
    title = name.replace("-", " ").title()
    logo = ' tvg-logo="%s%s"' % (B, logos[name]) if name in logos else ""
    lines.append('#EXTINF:-1 tvg-id="%s"%s,%s' % (name, logo, title))
    lines.append(B + p)

if not paths:
    print("No channels found")
    raise SystemExit(1)

open("playlist.m3u", "w").write("\n".join(lines) + "\n")
print(len(paths), "channels")
