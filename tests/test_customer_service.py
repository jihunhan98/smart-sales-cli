"""고객사 서비스 테스트"""

import unittest
import json
import os
import sys

# 테스트 환경에서 모듈 import를 위해 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from storage import DATA_DIR
from customer_service import (
    register_customer, list_customers, get_customer,
    search_customers, update_customer, delete_customer
)


class TestCustomerService(unittest.TestCase):
    def setUp(self):
        """테스트 전 데이터 초기화"""
        self.customers_file = os.path.join(DATA_DIR, "customers.json")
        if os.path.exists(self.customers_file):
            os.remove(self.customers_file)
        # 빈 파일 생성
        with open(self.customers_file, "w", encoding="utf-8") as f:
            json.dump([], f)

    def tearDown(self):
        """테스트 후 정리"""
        if os.path.exists(self.customers_file):
            os.remove(self.customers_file)

    def test_register_customer_success(self):
        """고객사 등록 성공"""
        result = register_customer("테스트고객사", "홍길동", "hong@example.com")
        self.assertTrue(result["success"])
        self.assertEqual(result["customer"]["customer_id"], "C001")

    def test_register_customer_empty_name(self):
        """고객사명 빈 값 실패"""
        result = register_customer("", "홍길동", "hong@example.com")
        self.assertFalse(result["success"])

    def test_register_customer_empty_manager(self):
        """담당자명 빈 값 실패"""
        result = register_customer("테스트고객사", "", "hong@example.com")
        self.assertFalse(result["success"])

    def test_register_customer_invalid_email(self):
        """이메일 형식 오류 실패"""
        result = register_customer("테스트고객사", "홍길동", "invalid-email")
        self.assertFalse(result["success"])

    def test_list_customers_empty(self):
        """빈 목록 조회"""
        customers = list_customers()
        self.assertEqual(customers, [])

    def test_list_customers_with_data(self):
        """데이터 있는 목록 조회"""
        register_customer("고객사A", "김철수", "a@example.com")
        register_customer("고객사B", "이영희", "b@example.com")
        customers = list_customers()
        self.assertEqual(len(customers), 2)

    def test_list_customers_sorted(self):
        """고객사 목록이 customer_name 오름차순 정렬되는지 확인"""
        register_customer("b고객사", "김철수", "b@example.com")
        register_customer("a고객사", "이영희", "a@example.com")
        register_customer("c고객사", "박영수", "c@example.com")
        customers = list_customers()
        self.assertEqual(customers[0]["customer_name"], "a고객사")
        self.assertEqual(customers[1]["customer_name"], "b고객사")
        self.assertEqual(customers[2]["customer_name"], "c고객사")

    def test_list_customers_sorted_case_insensitive(self):
        """대소문자 구분 없는 정렬 확인"""
        register_customer("B고객사", "김철수", "b@example.com")
        register_customer("a고객사", "이영희", "a@example.com")
        customers = list_customers()
        self.assertEqual(customers[0]["customer_name"], "a고객사")
        self.assertEqual(customers[1]["customer_name"], "B고객사")

    def test_get_customer_found(self):
        """고객사 상세 조회 성공"""
        register_customer("고객사A", "김철수", "a@example.com")
        c = get_customer("C001")
        self.assertIsNotNone(c)
        self.assertEqual(c["customer_name"], "고객사A")

    def test_get_customer_not_found(self):
        """존재하지 않는 고객사 조회"""
        c = get_customer("C999")
        self.assertIsNone(c)

    def test_search_customers(self):
        """고객사 검색"""
        register_customer("삼성전자", "김철수", "sam@example.com")
        register_customer("LG전자", "이영희", "lg@example.com")
        results = search_customers("삼성")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["customer_name"], "삼성전자")

    def test_search_customers_empty_keyword(self):
        """빈 검색어"""
        register_customer("삼성전자", "김철수", "sam@example.com")
        results = search_customers("")
        self.assertEqual(results, [])

    def test_update_customer_success(self):
        """고객사 수정 성공"""
        register_customer("고객사A", "김철수", "a@example.com")
        result = update_customer("C001", "고객사A수정", "박영희", "b@example.com")
        self.assertTrue(result["success"])
        c = get_customer("C001")
        self.assertEqual(c["manager_name"], "박영희")

    def test_update_customer_not_found(self):
        """존재하지 않는 고객사 수정 실패"""
        result = update_customer("C999", "이름", "담당자", "e@example.com")
        self.assertFalse(result["success"])

    def test_delete_customer_success(self):
        """고객사 삭제 성공"""
        register_customer("고객사A", "김철수", "a@example.com")
        result = delete_customer("C001")
        self.assertTrue(result["success"])
        customers = list_customers()
        self.assertEqual(len(customers), 0)

    def test_delete_customer_not_found(self):
        """존재하지 않는 고객사 삭제 실패"""
        result = delete_customer("C999")
        self.assertFalse(result["success"])


if __name__ == "__main__":
    unittest.main()