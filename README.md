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

### 무료 키트(엑셀·PDF) 붙이기
키트 파일은 `downloads/<키트-이름>/`에 넣고, 글의 `meta.json`에 아래처럼 적습니다. 빌드하면 글 맨 위에 "무료 키트 받기" 링크, 출처 위에 다운로드 상자가 생기고 블로그 목록에 "무료 키트" 표시가 붙습니다. 영어 글(en)에는 EN판, 한국어 글(ko)에는 EN_KR판을 연결합니다.
```json
"downloads": {"kit": "car-loan-interest-deduction",
  "en": ["Car_Loan_Interest_Deduction_Calculator_2026_EN.xlsx", "Car_Loan_Interest_Deduction_Guide_2026_EN.pdf"],
  "ko": ["Car_Loan_Interest_Deduction_Calculator_2026_EN_KR.xlsx", "Car_Loan_Interest_Deduction_Guide_2026_EN_KR.pdf"]}
```
엑셀 파일은 올리기 전에 문서 속성(작성자·마지막 수정자)에 개인 이름이 없는지 확인합니다. 글 본문에서는 Etsy·Gumroad 대신 `<a href="#kit">무료 키트 다운로드</a>`로 안내합니다.




