"""고객사별 활동 요약 서비스"""

from storage import load_data
from customer_service import CUSTOMERS_FILE
from sales_report_service import REPORTS_FILE


def get_customer_summary(customer_id: str) -> dict:
    """특정 고객사의 영업일지 활동 요약"""
    reports = load_data(REPORTS_FILE)
    customer_reports = [r for r in reports if r["customer_id"] == customer_id.strip()]

    total = len(customer_reports)
    draft_count = sum(1 for r in customer_reports if r["status"] == "DRAFT")
    submitted_count = sum(1 for r in customer_reports if r["status"] == "SUBMITTED")
    approved_count = sum(1 for r in customer_reports if r["status"] == "APPROVED")
    rejected_count = sum(1 for r in customer_reports if r["status"] == "REJECTED")

    return {
        "customer_id": customer_id.strip(),
        "total_reports": total,
        "draft": draft_count,
        "submitted": submitted_count,
        "approved": approved_count,
        "rejected": rejected_count,
    }


def get_all_summaries() -> list:
    """전체 고객사의 활동 요약"""
    customers = load_data(CUSTOMERS_FILE)
    summaries = []
    for c in customers:
        summary = get_customer_summary(c["customer_id"])
        summary["customer_name"] = c["customer_name"]
        summaries.append(summary)
    return summaries