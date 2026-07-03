"""결재 서비스 테스트"""

import unittest
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from storage import DATA_DIR
from sales_report_service import register_report
from approval_service import submit_report, approve_report, reject_report, withdraw_report


class TestApprovalService(unittest.TestCase):
    def setUp(self):
        self.reports_file = os.path.join(DATA_DIR, "sales_reports.json")
        if os.path.exists(self.reports_file):
            os.remove(self.reports_file)
        with open(self.reports_file, "w", encoding="utf-8") as f:
            json.dump([], f)
        # 등록 및 상신 (5자 이상)
        register_report("C001", "2026-06-09", "테스트 보고서")
        submit_report("R001")

    def tearDown(self):
        if os.path.exists(self.reports_file):
            os.remove(self.reports_file)

    def test_submit_report_success(self):
        """상신 성공 (DRAFT -> SUBMITTED)"""
        register_report("C002", "2026-06-10", "두 번째 보고서")
        result = submit_report("R002")
        self.assertTrue(result["success"])
        self.assertEqual(result["report"]["status"], "SUBMITTED")

    def test_submit_report_already_submitted(self):
        """이미 상신된 영업일지 상신 실패"""
        result = submit_report("R001")
        self.assertFalse(result["success"])

    def test_approve_report_success(self):
        """승인 성공 (SUBMITTED -> APPROVED)"""
        result = approve_report("R001")
        self.assertTrue(result["success"])
        self.assertEqual(result["report"]["status"], "APPROVED")

    def test_approve_report_draft(self):
        """DRAFT 상태 승인 실패"""
        register_report("C002", "2026-06-10", "두 번째 보고서")
        result = approve_report("R002")
        self.assertFalse(result["success"])

    def test_reject_report_success(self):
        """반려 성공 (SUBMITTED -> REJECTED)"""
        result = reject_report("R001")
        self.assertTrue(result["success"])
        self.assertEqual(result["report"]["status"], "REJECTED")

    def test_reject_report_draft(self):
        """DRAFT 상태 반려 실패"""
        register_report("C002", "2026-06-10", "두 번째 보고서")
        result = reject_report("R002")
        self.assertFalse(result["success"])

    def test_withdraw_report_success(self):
        """회수 성공 (SUBMITTED -> DRAFT)"""
        result = withdraw_report("R001")
        self.assertTrue(result["success"])
        self.assertEqual(result["report"]["status"], "DRAFT")

    def test_withdraw_report_approved(self):
        """APPROVED 상태 회수 실패"""
        approve_report("R001")
        result = withdraw_report("R001")
        self.assertFalse(result["success"])

    def test_approve_after_withdraw(self):
        """회수 후 재상신 및 승인"""
        withdraw_report("R001")
        submit_report("R001")
        result = approve_report("R001")
        self.assertTrue(result["success"])
        self.assertEqual(result["report"]["status"], "APPROVED")

    def test_report_not_found(self):
        """존재하지 않는 영업일지 처리"""
        result = submit_report("R999")
        self.assertFalse(result["success"])
        result = approve_report("R999")
        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()