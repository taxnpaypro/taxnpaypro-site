#!/usr/bin/env python3
"""Rebuild taxnpaypro.com (homepage + /blog/) from src/<folder>/ and data/.

Each post lives in src/<YYYY-MM-DD>_<Slug>/ with:
  Blog_<Slug>_KR.html, Blog_<Slug>_EN.html   post bodies (inline styles, images by file name)
  Fig*.png                                  figures
  meta.json  {"date","category" (accounting|tax|payroll|quickbooks|qbo),
              "slug":{"ko","en"}, "title":{"ko","en"}, "excerpt":{"ko","en"}}
Run:  python3 tools/build.py
      writes blog/<slug>.html, blog/img/, blog/index.html (blog list),
      index.html (homepage, from data/home_template.html) and site.json
"""
import os, re, json, glob, html, shutil, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, 'tools'))
import clean_blog
DOMAIN = 'taxnpaypro.com'
B = os.path.join(R, 'blog')

def png_size(path):
    # width/height from the PNG header, so pages can reserve image space (prevents layout shift / CLS)
    with open(path, 'rb') as f:
        h = f.read(24)
    if h[:8] != b'\x89PNG\r\n\x1a\n': return None
    return int.from_bytes(h[16:20], 'big'), int.from_bytes(h[20:24], 'big')

def add_img_size(body, folder_dir):
    def fix(m):
        tag = m.group(0)
        if re.search(r'\sheight="', tag): return tag
        sm = re.search(r'src="img/[^/"]+/([^"]+\.png)"', tag)
        sz = png_size(os.path.join(folder_dir, sm.group(1))) if sm else None
        if not sz: return tag
        w, h = sz
        wm = re.search(r'\swidth="(\d+)"', tag)
        if wm:
            dw = int(wm.group(1)); return tag.replace(wm.group(0), ' width="%d" height="%d"' % (dw, round(dw * h / w)), 1)
        return tag.replace('<img', '<img width="%d" height="%d"' % (w, h), 1)
    return re.sub(r'<img\b[^>]*>', fix, body)

PAGE = '''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} · BIZLEX</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://taxnpaypro.com/blog/{slug}.html">
<link rel="alternate" hreflang="{lang}" href="https://taxnpaypro.com/blog/{slug}.html"><link rel="alternate" hreflang="{olang}" href="https://taxnpaypro.com/blog/{oslug}.html">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;800&family=Noto+Sans+KR:wght@400;700&display=swap">
<style>
:root{{color-scheme:light;--navy:#14202E;--gold:#D4A845;--bg:#FFFFFF;--ink:#222;--muted:#5A6573}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:var(--bg);color:var(--ink)}}
body{{font-family:"Noto Sans KR","Manrope","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;word-break:keep-all;overflow-wrap:anywhere}}
.top{{background:var(--navy);padding-block:12px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.top .in{{max-width:820px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}}
.logo{{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-family:Manrope,sans-serif}}
.logo b{{font-weight:800;font-size:22px;letter-spacing:3px}} .logo i{{width:4px;height:26px;background:var(--gold)}} .logo span{{font-weight:400;font-size:22px;letter-spacing:3px}}
.nav{{display:flex;gap:16px;align-items:center}}
.nav a{{color:#C9D3DE;text-decoration:none;font-size:14px;min-height:36px;display:inline-flex;align-items:center}}
.nav a:hover{{color:#fff}}
.nav a.lang{{border:1px solid rgba(255,255,255,.3);border-radius:999px;padding:4px 14px;color:#fff}}
main{{max-width:820px;margin:0 auto;padding-block:36px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.meta{{font-family:ui-monospace,Menlo,monospace;font-size:13px;color:var(--muted);letter-spacing:.06em;text-transform:uppercase;margin:0 0 10px}}
h1.t{{font-family:Manrope,"Noto Sans KR",sans-serif;font-weight:800;font-size:clamp(28px,4.4vw,40px);line-height:1.25;color:#1F3A5F;margin:0 0 18px;text-wrap:balance}}
main img{{max-width:100%;height:auto}}
main table{{display:block;max-width:100%;overflow-x:auto}} main pre,main p{{max-width:100%}}
.conv{{margin-top:36px;padding:16px 18px;border:1px solid #dde3ea;border-left:5px solid var(--gold);border-radius:8px;background:#FBF8F0;display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center}}
.conv b{{color:#1F3A5F}} .conv span{{color:var(--muted);flex:1 1 260px}} .conv a{{color:#fff;background:var(--navy);padding:8px 14px;border-radius:6px;text-decoration:none;font-weight:700;min-height:40px;display:inline-flex;align-items:center}}
.kittop{{margin:0 0 22px}} .kittop a{{display:inline-flex;align-items:center;min-height:40px;padding:8px 14px;border-radius:6px;background:#FBF8F0;border:1px solid var(--gold);color:#1F3A5F;font-weight:700;text-decoration:none}}
.kit{{margin-top:40px;padding:20px 20px 14px;border:2px solid var(--navy);border-radius:10px;background:#F7F9FB;scroll-margin-top:16px}}
.kit h2{{margin:0 0 6px;font-size:22px;color:#1F3A5F}} .kit>p{{margin:0 0 12px;color:var(--muted)}}
.kit ul{{list-style:none;margin:0;padding:0;display:grid;gap:10px}}
.kit li{{display:flex;flex-wrap:wrap;align-items:center;gap:4px 12px;padding:10px 12px;background:#fff;border:1px solid #dde3ea;border-radius:8px}}
.kit li a{{color:#fff;background:var(--navy);padding:8px 14px;border-radius:6px;text-decoration:none;font-weight:700;min-height:40px;display:inline-flex;align-items:center}}
.kit li small{{color:var(--muted);font-size:13px;overflow-wrap:anywhere}}
.kit .fine{{font-size:12.5px;color:var(--muted);margin:12px 0 0}}
.back{{margin-top:40px;padding-top:20px;border-top:1px solid #dde3ea}}
.back a{{color:#1F3A5F;font-weight:700;text-decoration:none}}
a:focus-visible{{outline:2px solid var(--gold);outline-offset:3px}}
</style></head><body>
<header class="top"><div class="in">
<a class="logo" href="/" aria-label="BIZLEX, INC."><b>BIZ</b><i aria-hidden="true"></i><span>LEX</span></a>
<nav class="nav"><a href="/blog/">{blog}</a><a class="lang" href="{other}" lang="{olang}">{oname}</a></nav>
</div></header>
<main>
<p class="meta">{date} · {cat}</p>
<h1 class="t">{title}</h1>
{body}
<aside class="conv"><b>{convh}</b><span>{convt}</span><a href="/csv-to-qbo">{convb}</a></aside>
<p class="back"><a href="/blog/">{backtxt}</a></p>
</main>
</body></html>
'''

def human_size(n):
    return '%d KB' % max(1, round(n / 1024)) if n < 1024 * 1024 else '%.1f MB' % (n / 1048576)

def file_label(name, lang):
    ko = lang == 'ko'
    n = name.lower()
    if n.endswith('.pdf'): return '단계별 가이드 (PDF)' if ko else 'Step-by-step guide (PDF)'
    if n.endswith('.iif'): return 'QuickBooks Desktop 가져오기 예시 (.iif)' if ko else 'QuickBooks Desktop import example (.iif)'
    if n.endswith('.csv'): return 'QuickBooks Online 가져오기 예시 (.csv)' if ko else 'QuickBooks Online import example (.csv)'
    if 'sample' in n: return '예시 데이터가 채워진 Excel' if ko else 'Excel workbook with sample data'
    if 'blank' in n: return '빈 Excel 양식' if ko else 'Blank Excel workbook'
    return 'Excel 계산 도구 (.xlsx)' if ko else 'Excel workbook (.xlsx)'

def kit_boxes(m, lang, folder, errors, qb=False):
    """meta.json "downloads": {"kit": "<folder under /downloads>", "ko": [files], "en": [files]}
    Returns (top link, full box) HTML; ('', '') when the post has no kit."""
    dl = m.get('downloads')
    if not dl: return '', ''
    kit, files = dl.get('kit', ''), dl.get(lang, [])
    if not re.fullmatch(r'[a-z0-9-]+', kit) or not files:
        errors.append('%s: bad downloads entry' % folder); return '', ''
    ko = lang == 'ko'
    items = []
    for f in files:
        p = os.path.join(R, 'downloads', kit, f)
        if '/' in f or not os.path.isfile(p):
            errors.append('%s: missing download downloads/%s/%s' % (folder, kit, f)); continue
        items.append('<li><a href="/downloads/%s/%s" download>%s</a><small>%s · %s</small></li>' % (
            kit, html.escape(f, quote=True), file_label(f, lang), html.escape(f), human_size(os.path.getsize(p))))
    top = '<p class="kittop"><a href="#kit">%s</a></p>' % ('↓ 이 글의 무료 Excel·PDF 키트 받기' if ko else '↓ Get the free Excel + PDF kit for this article')
    box = ('<section class="kit" id="kit"><h2>%s</h2><p>%s</p><ul>%s</ul><p class="fine">%s</p></section>' % (
        '무료 키트 다운로드' if ko else 'Free kit download',
        '글에서 설명한 내용을 그대로 따라 할 수 있는 도구입니다. 가입 없이 바로 받으세요.' if ko else 'Tools to follow this article step by step. No sign-up needed.',
        ''.join(items),
        ('본인과 본인 사업에 무료로 쓰세요. 재판매·재배포는 하지 마세요. 일반 정보이며 세무·법률·회계 자문이 아닙니다. 숫자는 본인 자료로 꼭 확인하세요.' + (' QuickBooks는 Intuit Inc.의 상표이며 BIZLEX는 Intuit과 관련이 없습니다.' if qb else '')) if ko else
        ('Free to use for yourself and your own business; please do not resell or redistribute. General information, not tax, legal or accounting advice; check every figure against your own records.' + (' QuickBooks is a trademark of Intuit Inc.; BIZLEX is not affiliated with Intuit.' if qb else ''))))
    return top, box

CAT = {'accounting': ('회계', 'Accounting'), 'tax': ('세무', 'Tax'), 'payroll': ('급여', 'Payroll'), 'quickbooks': ('QuickBooks Desktop', 'QuickBooks Desktop'), 'qbo': ('QuickBooks Online', 'QuickBooks Online')}

def main():
    base = json.load(open(os.path.join(R, 'data', 'site_base.json'), encoding='utf-8'))
    posts, errors = [], []
    shutil.rmtree(B, ignore_errors=True); os.makedirs(B)
    for d in sorted(glob.glob(os.path.join(R, 'src', '*'))):
        folder = os.path.basename(d)
        mp = os.path.join(d, 'meta.json')
        if not os.path.exists(mp):
            errors.append(folder + ': meta.json missing'); continue
        m = json.load(open(mp, encoding='utf-8'))
        for k in ('date', 'category', 'slug', 'title', 'excerpt'):
            if k not in m: errors.append('%s: meta.json has no %s' % (folder, k))
        if m.get('category') not in CAT: errors.append('%s: bad category %r' % (folder, m.get('category')))
        for lang, L in (('ko', 'KR'), ('en', 'EN')):
            fs = glob.glob(os.path.join(d, 'Blog_*_%s.html' % L))
            if len(fs) != 1:
                errors.append('%s: need exactly one Blog_*_%s.html' % (folder, L)); continue
            if not re.fullmatch(r'[a-z0-9-]+', m['slug'][lang]): errors.append('%s: bad slug %r' % (folder, m['slug'][lang]))
            frag = clean_blog.clean(open(fs[0], encoding='utf-8').read())
            mt = re.match(r'<!-- Title: (.*?) -->\n?', frag)
            title = mt.group(1) if mt else m['title'][lang]
            body = frag[mt.end():] if mt else frag
            for src in re.findall(r'src="([^"]+)"', body):
                if '/' in src or not os.path.exists(os.path.join(d, src)): errors.append('%s: missing image %s' % (folder, src))
            body = re.sub(r'src="([^"/]+\.png)"', lambda x: 'src="img/%s/%s"' % (folder, x.group(1)), body)
            body = add_img_size(body, d)
            o = 'en' if lang == 'ko' else 'ko'
            ktop, kbox = kit_boxes(m, lang, folder, errors, qb='QuickBooks' in body)
            if kbox:
                # put the download box before the Sources heading so readers see it before the reference list
                src_h = [x.start() for x in re.finditer(r'<h2\b[^>]*>\s*(Sources|출처)\s*</h2>', body)]
                body = body[:src_h[-1]] + kbox + body[src_h[-1]:] if src_h else body + kbox
            page = PAGE.format(lang=lang, title=html.escape(title), body=ktop + body, desc=html.escape(m['excerpt'][lang], quote=True), slug=m['slug'][lang], oslug=m['slug'][o],
                               convh='무료 은행 CSV → QBO 변환기' if lang == 'ko' else 'Free bank CSV to QBO converter',
                               convt='은행 CSV를 QuickBooks Desktop용 .qbo·.iif 파일로. 브라우저 안에서만 처리합니다.' if lang == 'ko' else 'Turn bank CSV files into QuickBooks Desktop .qbo or .iif files, right in your browser.',
                               convb='변환기 열기' if lang == 'ko' else 'Open the converter', date=m['date'], cat=CAT[m['category']][0 if lang == 'ko' else 1],
                               blog='블로그' if lang == 'ko' else 'Blog', other='%s.html' % m['slug'][o], olang=o,
                               oname='English' if lang == 'ko' else '한국어', backtxt='← 블로그 글 목록' if lang == 'ko' else '← All articles')
            open(os.path.join(B, m['slug'][lang] + '.html'), 'w', encoding='utf-8').write(page)
        imgdir = os.path.join(B, 'img', folder); os.makedirs(imgdir, exist_ok=True)
        for f in os.listdir(d):
            if f.endswith('.png'): shutil.copy(os.path.join(d, f), os.path.join(imgdir, f))
        posts.append({'date': m['date'], 'category': m['category'], 'title': m['title'], 'excerpt': m['excerpt'],
                      'url': {k: 'https://%s/blog/%s.html' % (DOMAIN, v) for k, v in m['slug'].items()},
                      'previewUrl': {k: 'blog/%s.html' % v for k, v in m['slug'].items()}, 'freeKit': bool(m.get('downloads'))})
    if errors:
        print('ERRORS:'); [print(' -', e) for e in errors]; sys.exit(1)
    posts.sort(key=lambda p: p['date'], reverse=True)
    site = dict(base); site['posts'] = posts; site['blogUrl'] = 'https://%s/blog/' % DOMAIN
    site['updated'] = max([p['date'] for p in posts] + [base.get('updated', '')])
    json.dump(site, open(os.path.join(R, 'site.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    CATN = {c['id']: c['name'] for c in site['categories']}
    rows = {'ko': [], 'en': []}
    for p in posts:
        for lang in ('ko', 'en'):
            rows[lang].append('<a class="post" data-cat="%s" href="%s"><span class="d">%s</span><span class="b"><b>%s</b><em>%s</em></span><span class="c">%s</span></a>' % (
                p['category'], '/blog/' + p['previewUrl'][lang].split('/')[-1], p['date'], html.escape(p['title'][lang]), html.escape(p['excerpt'][lang]),
                ('<i class="k">%s</i>' % ('무료 키트' if lang == 'ko' else 'Free kit') if p.get('freeKit') else '') + html.escape(CATN[p['category']][lang])))
    tabs = lambda lang: ''.join('<button type="button" data-cat="%s">%s</button>' % (k, v) for k, v in [('all', '전체' if lang == 'ko' else 'All')] + [(c['id'], c['name'][lang]) for c in site['categories']])
    INDEX = '''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>BIZLEX Blog · Accounting, Tax, Payroll, QuickBooks Desktop</title>
    <meta name="description" content="회계·세무·급여·QuickBooks Desktop을 한국어와 영어로 쉽게 설명하는 BIZLEX 블로그. Accounting, tax, payroll and QuickBooks Desktop articles in Korean and English.">
    <link rel="canonical" href="https://taxnpaypro.com/blog/">
    <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;800&family=Noto+Sans+KR:wght@400;700&display=swap">
    <style>
    :root{color-scheme:light}*{box-sizing:border-box}html,body{margin:0;background:#F5F6F4;color:#14202E}
    body{font-family:"Noto Sans KR",Manrope,system-ui,sans-serif;word-break:keep-all;overflow-wrap:anywhere}
    .top{background:#14202E;padding:12px max(16px,env(safe-area-inset-left,0px))}
    .top .in,.wrap{max-width:980px;margin:0 auto}
    .top .in{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
    .logo{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-family:Manrope,sans-serif}
    .logo b{font-weight:800;font-size:22px;letter-spacing:3px}.logo i{width:4px;height:26px;background:#D4A845}.logo span{font-size:22px;letter-spacing:3px}
    .lang{display:inline-flex;border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:3px}
    .lang button{font:inherit;font-size:13px;border:0;background:none;color:#C9D3DE;padding:5px 13px;border-radius:999px;cursor:pointer;min-height:32px}
    .lang button[aria-pressed=true]{background:#D4A845;color:#14202E;font-weight:700}
    .wrap{padding:40px max(16px,env(safe-area-inset-left,0px)) 64px}
    h1{font-family:Manrope,"Noto Sans KR",sans-serif;font-weight:800;font-size:clamp(30px,4.6vw,44px);margin:0 0 8px}
    .sub{color:#556170;margin:0 0 28px}
    .tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
    .tabs button{font:inherit;font-size:14px;border:1px solid #D9DDDF;background:#fff;border-radius:999px;padding:7px 14px;cursor:pointer;min-height:40px}
    .tabs button[aria-pressed=true]{background:#14202E;color:#fff;border-color:#14202E}
    .post{display:grid;grid-template-columns:110px minmax(0,1fr) auto;gap:4px 24px;padding:20px 0;border-bottom:1px solid #D9DDDF;color:inherit;text-decoration:none;align-items:baseline}
    @media(max-width:680px){.post{grid-template-columns:minmax(0,1fr)}}
    .post .d{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;color:#556170}
    .post b{display:block;font-size:19px;line-height:1.4}.post em{display:block;font-style:normal;color:#556170;font-size:14.5px;margin-top:4px}
    .post .c{font-size:12.5px;background:#EEF0EE;border-radius:999px;padding:3px 10px;white-space:nowrap;justify-self:start}
    .post:hover b{text-decoration:underline}
    .post .k{font-style:normal;font-weight:700;color:#14202E;background:#D4A845;border-radius:999px;padding:2px 8px;margin-right:6px}
    footer{color:#556170;font-size:13px;margin-top:40px}footer p{margin:4px 0}
    [hidden]{display:none!important}
    :focus-visible{outline:2px solid #D4A845;outline-offset:3px}
    </style></head><body>
    <header class="top"><div class="in"><a class="logo" href="/" aria-label="BIZLEX, INC."><b>BIZ</b><i aria-hidden="true"></i><span>LEX</span></a>
    <div class="lang" role="group" aria-label="Language"><button type="button" id="lk" aria-pressed="true">한국어</button><button type="button" id="le" aria-pressed="false">English</button></div></div></header>
    <main class="wrap">
    <section id="ko"><h1>BIZLEX 블로그</h1><p class="sub">회계·세무·급여·QuickBooks Desktop을 쉬운 한국어로.</p><div class="tabs">%s</div><div class="list">%s</div></section>
    <section id="en" hidden><h1>BIZLEX Blog</h1><p class="sub">Accounting, tax, payroll and QuickBooks Desktop in plain English.</p><div class="tabs">%s</div><div class="list">%s</div></section>
    <footer><p>© 2026 BIZLEX, INC. · taxnpaypro.com</p><p>QuickBooks is a registered trademark of Intuit Inc.; not affiliated with or endorsed by Intuit. Articles are general information, not tax, legal or accounting advice.</p></footer>
    </main>
    <script>
    (function(){
    function lang(l){document.getElementById('ko').hidden=l!=='ko';document.getElementById('en').hidden=l!=='en';document.documentElement.lang=l;
    document.getElementById('lk').setAttribute('aria-pressed',l==='ko');document.getElementById('le').setAttribute('aria-pressed',l==='en');try{localStorage.setItem('bizlex-lang',l)}catch(e){}}
    document.getElementById('lk').onclick=function(){lang('ko')};document.getElementById('le').onclick=function(){lang('en')};
    var s=null;try{s=localStorage.getItem('bizlex-lang')}catch(e){};lang(s==='en'?'en':'ko');
    document.querySelectorAll('section').forEach(function(sec){var bs=sec.querySelectorAll('.tabs button');
    function pick(c){bs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.cat===c)});sec.querySelectorAll('.post').forEach(function(p){p.hidden=!(c==='all'||p.dataset.cat===c)})}
    bs.forEach(function(b){b.onclick=function(){pick(b.dataset.cat)}});pick('all')});
    })();
    </script></body></html>
    ''' % (tabs('ko'), ''.join(rows['ko']), tabs('en'), ''.join(rows['en']))
    open(os.path.join(B, 'index.html'), 'w', encoding='utf-8').write(INDEX)
    home = open(os.path.join(R, 'data', 'home_template.html'), encoding='utf-8').read()
    assert home.count('__FALLBACK__') == 1
    fb = json.dumps(site, ensure_ascii=False).replace('</', '<\\/')
    open(os.path.join(R, 'index.html'), 'w', encoding='utf-8').write(home.replace('__FALLBACK__', fb))
    # sitemap.xml + robots.txt for Google Search Console
    urls = [('https://%s/' % DOMAIN, site['updated']), ('https://%s/csv-to-qbo' % DOMAIN, site['updated']), ('https://%s/blog/' % DOMAIN, site['updated'])]
    for p in posts:
        for lang in ('ko', 'en'): urls.append((p['url'][lang], p['date']))
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        '  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (html.escape(u), d) for u, d in urls) + '</urlset>\n'
    open(os.path.join(R, 'sitemap.xml'), 'w', encoding='utf-8').write(sm)
    open(os.path.join(R, 'robots.txt'), 'w', encoding='utf-8').write('User-agent: *\nAllow: /\nSitemap: https://%s/sitemap.xml\n' % DOMAIN)
    # visitor statistics (Cloudflare Web Analytics): token in data/site_base.json "cfAnalyticsToken"; empty = off
    tok = (base.get('cfAnalyticsToken') or '').strip()
    if tok and not re.fullmatch(r'[0-9a-f]{32}', tok): print('ERRORS:\n - cfAnalyticsToken must be 32 hex characters'); sys.exit(1)
    snip = ("<!--cfwa--><script type=\"module\" src=\"https://static.cloudflareinsights.com/beacon.min.js\" data-cf-beacon='{\"token\": \"%s\"}'></script><!--/cfwa-->" % tok) if tok else ''
    pages = [os.path.join(R, 'index.html'), os.path.join(R, 'csv-to-qbo.html')] + glob.glob(os.path.join(B, '*.html'))
    for f in pages:
        s = open(f, encoding='utf-8').read()
        s = re.sub(r'<!--cfwa-->.*?<!--/cfwa-->', '', s, flags=re.S)
        if snip:
            i = s.rfind('</body>')
            s = s[:i] + snip + s[i:] if i >= 0 else s + snip
        open(f, 'w', encoding='utf-8').write(s)
    print('built %d posts' % len(posts))

if __name__ == '__main__':
    main()
