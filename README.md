# BIZLEX 홈페이지 · 블로그 (taxnpaypro.com)

이 저장소가 taxnpaypro.com 사이트 전체입니다. GitHub Pages가 이 파일들을 그대로 보여 줍니다.

- `index.html` : 홈페이지 (taxnpaypro.com) — `data/home_template.html`에서 자동으로 만들어집니다
- `csv-to-qbo.html` : 무료 은행 CSV → QBO·IIF 변환기 (taxnpaypro.com/csv-to-qbo)
- `blog/index.html` : 블로그 글 목록 (taxnpaypro.com/blog/)
- `blog/<글 주소>.html` : 글 한 편 (한국어·영어 각각), `blog/img/` : 글 그림
- `site.json` : 홈페이지가 읽는 글 목록과 공지

새 글은 Claude 예약 작업이 **변경 요청(Pull Request)** 으로 올립니다. 내용을 보고 **Merge** 를 누르면 몇 분 안에 블로그와 홈페이지에 나타납니다.

## 새 글 추가 방법 (예약 작업용)
1. `src/<YYYY-MM-DD>_<Slug>/` 폴더에 `Blog_<Slug>_KR.html`, `Blog_<Slug>_EN.html`, 그림 `Fig*.png`, `meta.json`을 넣습니다.
2. `python3 tools/build.py` 를 실행합니다. `blog/` 글 페이지와 그림, 블로그 목록, 홈페이지 `index.html`, `site.json`이 다시 만들어집니다. 루트의 `index.html`은 직접 고치지 말고 `data/home_template.html`을 고칩니다.
3. 새 브랜치로 커밋하고 변경 요청(Pull Request)을 엽니다. 사장님이 Merge하면 공개됩니다.

`meta.json` 예시:
```json
{"date": "2026-11-07", "category": "accounting",
 "slug": {"ko": "example-korean", "en": "example"},
 "title": {"ko": "한국어 제목", "en": "English title"},
 "excerpt": {"ko": "한 줄 요약", "en": "One-line summary"}}
```
category는 accounting(회계) · tax(세무) · payroll(급여) · quickbooks(QuickBooks Desktop) · qbo(QuickBooks Online) 중 하나입니다.
