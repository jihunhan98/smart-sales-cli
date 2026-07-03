"""영업일지 CRUD 서비스"""

from storage import load_data, save_data

REPORTS_FILE = "sales_reports.json"
VALID_STATUSES = ["DRAFT", "SUBMITTED", "APPROVED", "REJECTED"]


def _get_all_reports() -> list:
    return load_data(REPORTS_FILE)


def _save_all_reports(reports: list) -> None:
    save_data(REPORTS_FILE, reports)


def _next_report_id(reports: list) -> str:
    existing_ids = [r["report_id"] for r in reports]
    num = 1
    while f"R{num:03d}" in existing_ids:
        num += 1
    return f"R{num:03d}"


def register_report(customer_id: str, activity_date: str, content: str) -> dict:
    """영업일지 등록"""
    reports = _get_all_reports()

    if not activity_date.strip():
        return {"success": False, "message": "활동 날짜는 비울 수 없습니다."}
    if not content.strip():
        return {"success": False, "message": "내용은 비울 수 없습니다."}

    report_id = _next_report_id(reports)
    report = {
        "report_id": report_id,
        "customer_id": customer_id.strip(),
        "activity_date": activity_date.strip(),
        "content": content.strip(),
        "status": "DRAFT",
    }
    reports.append(report)
    _save_all_reports(reports)
    return {"success": True, "message": f"영업일지 등록 완료: {report_id}", "report": report}


def list_reports() -> list:
    """영업일지 목록 반환"""
    return _get_all_reports()


def list_reports_by_status(status: str) -> list:
    """특정 상태의 영업일지 목록 조회"""
    reports = _get_all_reports()
    status = status.strip().upper()
    if status not in VALID_STATUSES:
        return []
    return [r for r in reports if r["status"] == status]


def get_report(report_id: str) -> dict:
    """영업일지 상세 조회"""
    reports = _get_all_reports()
    for r in reports:
        if r["report_id"] == report_id.strip():
            return r
    return None


def update_report(report_id: str, customer_id: str, activity_date: str, content: str) -> dict:
    """영업일지 수정 (DRAFT 상태만 가능)"""
    reports = _get_all_reports()
    for r in reports:
        if r["report_id"] == report_id.strip():
            if r["status"] != "DRAFT":
                return {"success": False, "message": "DRAFT 상태에서만 수정 가능합니다."}
            if not activity_date.strip():
                return {"success": False, "message": "활동 날짜는 비울 수 없습니다."}
            if not content.strip():
                return {"success": False, "message": "내용은 비울 수 없습니다."}
            r["customer_id"] = customer_id.strip()
            r["activity_date"] = activity_date.strip()
            r["content"] = content.strip()
            _save_all_reports(reports)
            return {"success": True, "message": "영업일지 수정 완료", "report": r}
    return {"success": False, "message": "존재하지 않는 영업일지입니다."}


def get_recent_reports(limit: int = 5) -> list:
    """최근 영업일지 조회 (activity_date 기준 내림차순, report_id 기준 안정 정렬)"""
    reports = _get_all_reports()
    sorted_reports = sorted(reports, key=lambda r: (r["activity_date"], r["report_id"]), reverse=True)
    return sorted_reports[:limit]