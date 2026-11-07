# BIZLEX 블로그 (blog.taxnpaypro.com)

이 저장소가 블로그 사이트입니다. GitHub Pages가 이 파일들을 그대로 보여 줍니다.

- `index.html` : 블로그 글 목록
- `<글 주소>.html` : 글 한 편 (한국어·영어 각각)
- `img/` : 글에 들어가는 그림
- `site.json` : taxnpaypro.com 홈페이지가 읽는 글 목록과 공지

새 글은 Claude 예약 작업이 **변경 요청(Pull Request)** 으로 올립니다. 내용을 보고 **Merge** 를 누르면 몇 분 안에 블로그와 홈페이지에 나타납니다.

## 새 글 추가 방법 (예약 작업용)
1. `src/<YYYY-MM-DD>_<Slug>/` 폴더에 `Blog_<Slug>_KR.html`, `Blog_<Slug>_EN.html`, 그림 `Fig*.png`, `meta.json`을 넣습니다.
2. `python3 tools/build.py` 를 실행합니다. 글 페이지, `img/`, `index.html`, `site.json`이 다시 만들어집니다.
3. 새 브랜치로 커밋하고 변경 요청(Pull Request)을 엽니다. 사장님이 Merge하면 공개됩니다.

`meta.json` 예시:
```json
{"date": "2026-11-07", "category": "accounting",
 "slug": {"ko": "example-korean", "en": "example"},
 "title": {"ko": "한국어 제목", "en": "English title"},
 "excerpt": {"ko": "한 줄 요약", "en": "One-line summary"}}
```
category는 accounting(회계) · tax(세무) · payroll(급여) · quickbooks(QuickBooks Desktop) 중 하나입니다.
