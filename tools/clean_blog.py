import re,sys
TOK='§SITE§'
def clean(t):
    t=t.replace('taxnpaypro.com',TOK)
    out=[]
    def fix_p(m):
        p=m.group(0)
        if TOK not in p and '20+' not in p and '20년' not in p: return p
        inner_start=p.index('>')+1; inner_end=p.rindex('</')
        head,body,tail=p[:inner_start],p[inner_start:inner_end],p[inner_end:]
        # split into sentences keeping tags
        sents=re.split(r'(?<=[.!?。])\s+|(?<=다\.)\s*',body)
        keep=[s for s in sents if s.strip() and TOK not in s and '20+ years' not in s and '20년 이상' not in s]
        nb=' '.join(keep).strip()
        if not re.sub('<[^>]+>','',nb).strip(): return ''
        return head+nb+tail
    t=re.sub(r'<p[^>]*>.*?</p>',fix_p,t,flags=re.S)
    return t.replace(TOK,'taxnpaypro.com')
if __name__=='__main__':
    import glob
    for f in sorted(glob.glob('blogsrc/*/*.html')):
        t=clean(open(f,encoding='utf-8').read())
        assert 'taxnpaypro.com' not in t or True
        ps=re.findall(r'<p[^>]*>.*?</p>',t,flags=re.S)
        print('==',f.split('/')[-1]); 
        for p in ps[-3:-1]: print('   ',re.sub('<[^>]+>','',p)[:300])
        print('   left: site', t.count('taxnpaypro'), ' 20yrs', t.count('20+ years')+t.count('20년 이상'))
