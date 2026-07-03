"""영업일지 서비스 테스트"""

import unittest
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from storage import DATA_DIR
from sales_report_service import register_report, list_reports, list_reports_by_customer, get_report, update_report


class TestSalesReportService(unittest.TestCase):
    def setUp(self):
        self.reports_file = os.path.join(DATA_DIR, "sales_reports.json")
        if os.path.exists(self.reports_file):
            os.remove(self.reports_file)
        with open(self.reports_file, "w", encoding="utf-8") as f:
            json.dump([], f)

    def tearDown(self):
        if os.path.exists(self.reports_file):
            os.remove(self.reports_file)

    def test_register_report_success(self):
        """영업일지 등록 성공"""
        result = register_report("C001", "2026-06-09", "제품 소개 미팅")
        self.assertTrue(result["success"])
        self.assertEqual(result["report"]["report_id"], "R001")
        self.assertEqual(result["report"]["status"], "DRAFT")

    def test_register_report_empty_date(self):
        """날짜 빈 값 실패"""
        result = register_report("C001", "", "내용")
        self.assertFalse(result["success"])

    def test_register_report_empty_content(self):
        """내용 빈 값 실패"""
        result = register_report("C001", "2026-06-09", "")
        self.assertFalse(result["success"])

    def test_list_reports_empty(self):
        """빈 목록 조회"""
        reports = list_reports()
        self.assertEqual(reports, [])

    def test_list_reports_with_data(self):
        """데이터 있는 목록 조회"""
        register_report("C001", "2026-06-09", "내용1")
        register_report("C002", "2026-06-10", "내용2")
        reports = list_reports()
        self.assertEqual(len(reports), 2)

    def test_get_report_found(self):
        """영업일지 상세 조회 성공"""
        register_report("C001", "2026-06-09", "내용")
        r = get_report("R001")
        self.assertIsNotNone(r)
        self.assertEqual(r["content"], "내용")

    def test_get_report_not_found(self):
        """존재하지 않는 영업일지 조회"""
        r = get_report("R999")
        self.assertIsNone(r)

    def test_update_report_success(self):
        """영업일지 수정 성공"""
        register_report("C001", "2026-06-09", "내용")
        result = update_report("R001", "C002", "2026-06-10", "수정된 내용")
        self.assertTrue(result["success"])
        r = get_report("R001")
        self.assertEqual(r["content"], "수정된 내용")

    def test_update_report_not_found(self):
        """존재하지 않는 영업일지 수정 실패"""
        result = update_report("R999", "C001", "2026-06-09", "내용")
        self.assertFalse(result["success"])

    def test_list_reports_by_customer(self):
        """고객사별 영업일지 목록 조회"""
        register_report("C001", "2026-06-09", "첫 번째 보고서")
        register_report("C001", "2026-06-10", "두 번째 보고서")
        register_report("C002", "2026-06-11", "다른 보고서")
        reports = list_reports_by_customer("C001")
        self.assertEqual(len(reports), 2)
        for r in reports:
            self.assertEqual(r["customer_id"], "C001")

    def test_list_reports_by_customer_not_found(self):
        """존재하지 않는 고객사 영업일지 조회"""
        reports = list_reports_by_customer("C999")
        self.assertEqual(reports, [])


if __name__ == "__main__":
    unittest.main()