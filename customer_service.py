"""고객사 CRUD 서비스"""

from storage import load_data, save_data
from validators import validate_email, validate_customer_id, validate_not_empty

CUSTOMERS_FILE = "customers.json"


def _get_all_customers() -> list:
    return load_data(CUSTOMERS_FILE)


def _save_all_customers(customers: list) -> None:
    save_data(CUSTOMERS_FILE, customers)


def _next_customer_id(customers: list) -> str:
    existing_ids = [c["customer_id"] for c in customers]
    num = 1
    while f"C{num:03d}" in existing_ids:
        num += 1
    return f"C{num:03d}"


def register_customer(customer_name: str, manager_name: str, email: str) -> dict:
    """고객사 등록"""
    customers = _get_all_customers()

    if not validate_not_empty(customer_name):
        return {"success": False, "message": "고객사명은 비울 수 없습니다."}
    if not validate_not_empty(manager_name):
        return {"success": False, "message": "담당자명은 비울 수 없습니다."}
    if not validate_email(email):
        return {"success": False, "message": "이메일 형식이 올바르지 않습니다."}

    customer_id = _next_customer_id(customers)
    customer = {
        "customer_id": customer_id,
        "customer_name": customer_name.strip(),
        "manager_name": manager_name.strip(),
        "email": email.strip(),
    }
    customers.append(customer)
    _save_all_customers(customers)
    return {"success": True, "message": f"고객사 등록 완료: {customer_id}", "customer": customer}


def list_customers() -> list:
    """고객사 목록 반환"""
    return _get_all_customers()


def get_customer(customer_id: str) -> dict:
    """고객사 상세 조회"""
    customers = _get_all_customers()
    for c in customers:
        if c["customer_id"] == customer_id.strip():
            return c
    return None


def search_customers(keyword: str) -> list:
    """고객사 검색 (고객사명, 담당자명, 이메일)"""
    customers = _get_all_customers()
    keyword = keyword.strip().lower()
    if not keyword:
        return []
    result = []
    for c in customers:
        if (keyword in c["customer_name"].lower() or
                keyword in c["manager_name"].lower() or
                keyword in c["email"].lower()):
            result.append(c)
    return result


def update_customer(customer_id: str, customer_name: str, manager_name: str, email: str) -> dict:
    """고객사 정보 수정"""
    customers = _get_all_customers()
    for c in customers:
        if c["customer_id"] == customer_id.strip():
            if not validate_not_empty(customer_name):
                return {"success": False, "message": "고객사명은 비울 수 없습니다."}
            if not validate_not_empty(manager_name):
                return {"success": False, "message": "담당자명은 비울 수 없습니다."}
            if not validate_email(email):
                return {"success": False, "message": "이메일 형식이 올바르지 않습니다."}
            c["customer_name"] = customer_name.strip()
            c["manager_name"] = manager_name.strip()
            c["email"] = email.strip()
            _save_all_customers(customers)
            return {"success": True, "message": "고객사 정보 수정 완료", "customer": c}
    return {"success": False, "message": "존재하지 않는 고객사입니다."}


def delete_customer(customer_id: str) -> dict:
    """고객사 삭제"""
    customers = _get_all_customers()
    for i, c in enumerate(customers):
        if c["customer_id"] == customer_id.strip():
            deleted = customers.pop(i)
            _save_all_customers(customers)
            return {"success": True, "message": f"고객사 삭제 완료: {deleted['customer_name']}"}
    return {"success": False, "message": "존재하지 않는 고객사입니다."}