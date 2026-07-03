"""결재 상태 전이 서비스"""

from storage import load_data, save_data

REPORTS_FILE = "sales_reports.json"


def _get_all_reports() -> list:
    return load_data(REPORTS_FILE)


def _save_all_reports(reports: list) -> None:
    save_data(REPORTS_FILE, reports)


def submit_report(report_id: str) -> dict:
    """DRAFT -> SUBMITTED"""
    reports = _get_all_reports()
    for r in reports:
        if r["report_id"] == report_id.strip():
            if r["status"] == "DRAFT":
                r["status"] = "SUBMITTED"
                _save_all_reports(reports)
                return {"success": True, "message": "영업일지가 상신되었습니다.", "report": r}
            else:
                return {"success": False, "message": f"DRAFT 상태에서만 상신 가능합니다. (현재: {r['status']})"}
    return {"success": False, "message": "존재하지 않는 영업일지입니다."}


def approve_report(report_id: str) -> dict:
    """SUBMITTED -> APPROVED"""
    reports = _get_all_reports()
    for r in reports:
        if r["report_id"] == report_id.strip():
            if r["status"] == "SUBMITTED":
                r["status"] = "APPROVED"
                _save_all_reports(reports)
                return {"success": True, "message": "영업일지가 승인되었습니다.", "report": r}
            else:
                return {"success": False, "message": f"SUBMITTED 상태에서만 승인 가능합니다. (현재: {r['status']})"}
    return {"success": False, "message": "존재하지 않는 영업일지입니다."}


def reject_report(report_id: str) -> dict:
    """SUBMITTED -> REJECTED"""
    reports = _get_all_reports()
    for r in reports:
        if r["report_id"] == report_id.strip():
            if r["status"] == "SUBMITTED":
                r["status"] = "REJECTED"
                _save_all_reports(reports)
                return {"success": True, "message": "영업일지가 반려되었습니다.", "report": r}
            else:
                return {"success": False, "message": f"SUBMITTED 상태에서만 반려 가능합니다. (현재: {r['status']})"}
    return {"success": False, "message": "존재하지 않는 영업일지입니다."}


def withdraw_report(report_id: str) -> dict:
    """SUBMITTED -> DRAFT"""
    reports = _get_all_reports()
    for r in reports:
        if r["report_id"] == report_id.strip():
            if r["status"] == "SUBMITTED":
                r["status"] = "DRAFT"
                _save_all_reports(reports)
                return {"success": True, "message": "영업일지가 회수되었습니다.", "report": r}
            else:
                return {"success": False, "message": f"SUBMITTED 상태에서만 회수 가능합니다. (현재: {r['status']})"}
    return {"success": False, "message": "존재하지 않는 영업일지입니다."}