# Smart Sales CLI

Python으로 만든 간단한 영업 관리 CLI 애플리케이션입니다.

## 프로젝트 개요

고객사 관리와 영업일지를 기록하고, 결재 흐름을 처리하는 콘솔 기반 프로그램입니다.

## 실행 방법

```bash
python app.py
```

## unittest 실행 방법

```bash
python -m unittest discover -s tests -v
```

## 주요 메뉴

| 번호 | 기능 |
|------|------|
| 1 | 고객사 등록 |
| 2 | 고객사 목록 |
| 3 | 고객사 상세 조회 |
| 4 | 고객사 검색 |
| 5 | 고객사 정보 수정 |
| 6 | 고객사 삭제 |
| 7 | 영업일지 등록 |
| 8 | 영업일지 목록 |
| 9 | 영업일지 상세 조회 |
| 10 | 영업일지 수정 |
| 11 | 영업일지 상신 |
| 12 | 영업일지 승인 |
| 13 | 영업일지 반려 |
| 14 | 영업일지 회수 |
| 15 | 고객사 활동 요약 |
| 16 | 전체 활동 요약 |
| 0 | 종료 |

## 메뉴 사용 예시

자세한 사용 예시는 [docs/menu-examples.md](docs/menu-examples.md)를 참고하세요.

## Git 실습 흐름

```bash
# 작업 시작
git switch main
git pull origin main
git switch -c ai/실습-브랜치명

# 작업 후 확인
git status --short
git diff --stat
python -m unittest discover -s tests -v

# commit (사람이 직접)
git add .
git commit -m "feat: 실습 기능 설명"
git push origin ai/실습-브랜치명
```

## 기술 제약

- Python 3.10 이상
- Python 표준 라이브러리만 사용

## 구현된 기능

- 고객사 CRUD (등록, 목록, 상세, 수정, 삭제)
- 고객사 검색
- 영업일지 CRUD (등록, 목록, 상세, 수정)
- 영업일지 결재 흐름 (상신, 승인, 반려, 회수)
- 활동 요약 통계

## 아직 구현되지 않은 기능

- 고객사 등급 관리
- 고객사별/상태별 영업일지 필터링
- CSV 내보내기
- 반려 사유 입력