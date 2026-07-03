"""입력값 검증 모듈"""

import re


def validate_email(email: str) -> bool:
    """이메일 형식 검증"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def validate_customer_id(customer_id: str, existing_ids: list) -> bool:
    """고객사 ID 중복 검증"""
    return customer_id.strip() not in existing_ids


def validate_not_empty(value: str) -> bool:
    """빈 문자열 또는 공백만 있는지 검증"""
    return bool(value.strip())