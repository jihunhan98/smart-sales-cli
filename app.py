"""Smart Sales CLI - 메인 메뉴"""

import sys
from customer_service import (
    register_customer, list_customers, get_customer,
    search_customers, update_customer, delete_customer
)
from sales_report_service import (
    register_report, list_reports, get_report, update_report
)
from approval_service import submit_report, approve_report, reject_report, withdraw_report
from summary_service import get_customer_summary, get_all_summaries


def print_menu():
    print("\n" + "=" * 50)
    print("               Smart Sales CLI")
    print("=" * 50)
    print("1. 고객사 등록")
    print("2. 고객사 목록")
    print("3. 고객사 상세 조회")
    print("4. 고객사 검색")
    print("5. 고객사 정보 수정")
    print("6. 고객사 삭제")
    print("7. 영업일지 등록")
    print("8. 영업일지 목록")
    print("9. 영업일지 상세 조회")
    print("10. 영업일지 수정")
    print("11. 영업일지 상신")
    print("12. 영업일지 승인")
    print("13. 영업일지 반려")
    print("14. 영업일지 회수")
    print("15. 고객사 활동 요약")
    print("16. 전체 활동 요약")
    print("0. 종료")
    print("-" * 50)


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("숫자를 입력해 주세요.")


def run():
    while True:
        print_menu()
        try:
            choice = int(input("메뉴를 선택하세요: ").strip())
        except ValueError:
            print("숫자를 입력해 주세요.")
            continue

        if choice == 0:
            print("Smart Sales CLI를 종료합니다.")
            break

        elif choice == 1:
            print("\n[고객사 등록]")
            name = input("고객사명: ").strip()
            manager = input("담당자명: ").strip()
            email = input("이메일: ").strip()
            result = register_customer(name, manager, email)
            print(result["message"])

        elif choice == 2:
            print("\n[고객사 목록]")
            customers = list_customers()
            if not customers:
                print("등록된 고객사가 없습니다.")
            else:
                for c in customers:
                    print(f"  {c['customer_id']} | {c['customer_name']} | {c['manager_name']} | {c['email']}")

        elif choice == 3:
            print("\n[고객사 상세 조회]")
            cid = input("고객사 ID: ").strip()
            c = get_customer(cid)
            if c:
                print(f"  ID: {c['customer_id']}")
                print(f"  고객사명: {c['customer_name']}")
                print(f"  담당자명: {c['manager_name']}")
                print(f"  이메일: {c['email']}")
            else:
                print("존재하지 않는 고객사입니다.")

        elif choice == 4:
            print("\n[고객사 검색]")
            keyword = input("검색어: ").strip()
            results = search_customers(keyword)
            if not results:
                print("검색 결과가 없습니다.")
            else:
                for c in results:
                    print(f"  {c['customer_id']} | {c['customer_name']} | {c['manager_name']} | {c['email']}")

        elif choice == 5:
            print("\n[고객사 정보 수정]")
            cid = input("고객사 ID: ").strip()
            name = input("새 고객사명: ").strip()
            manager = input("새 담당자명: ").strip()
            email = input("새 이메일: ").strip()
            result = update_customer(cid, name, manager, email)
            print(result["message"])

        elif choice == 6:
            print("\n[고객사 삭제]")
            cid = input("고객사 ID: ").strip()
            confirm = input("정말 삭제하시겠습니까? (y/n): ").strip()
            if confirm == "y" or confirm == "Y":
                result = delete_customer(cid)
                print(result["message"])
            else:
                print("삭제가 취소되었습니다.")

        elif choice == 7:
            print("\n[영업일지 등록]")
            cid = input("고객사 ID: ").strip()
            date = input("활동 날짜 (YYYY-MM-DD): ").strip()
            content = input("내용: ").strip()
            result = register_report(cid, date, content)
            print(result["message"])

        elif choice == 8:
            print("\n[영업일지 목록]")
            reports = list_reports()
            if not reports:
                print("등록된 영업일지가 없습니다.")
            else:
                for r in reports:
                    print(f"  {r['report_id']} | {r['customer_id']} | {r['activity_date']} | {r['content'][:30]} | {r['status']}")

        elif choice == 9:
            print("\n[영업일지 상세 조회]")
            rid = input("영업일지 ID: ").strip()
            r = get_report(rid)
            if r:
                print(f"  ID: {r['report_id']}")
                print(f"  고객사 ID: {r['customer_id']}")
                print(f"  활동 날짜: {r['activity_date']}")
                print(f"  내용: {r['content']}")
                print(f"  상태: {r['status']}")
            else:
                print("존재하지 않는 영업일지입니다.")

        elif choice == 10:
            print("\n[영업일지 수정]")
            rid = input("영업일지 ID: ").strip()
            cid = input("새 고객사 ID: ").strip()
            date = input("새 활동 날짜 (YYYY-MM-DD): ").strip()
            content = input("새 내용: ").strip()
            result = update_report(rid, cid, date, content)
            print(result["message"])

        elif choice == 11:
            print("\n[영업일지 상신]")
            rid = input("영업일지 ID: ").strip()
            result = submit_report(rid)
            print(result["message"])

        elif choice == 12:
            print("\n[영업일지 승인]")
            rid = input("영업일지 ID: ").strip()
            result = approve_report(rid)
            print(result["message"])

        elif choice == 13:
            print("\n[영업일지 반려]")
            rid = input("영업일지 ID: ").strip()
            result = reject_report(rid)
            print(result["message"])

        elif choice == 14:
            print("\n[영업일지 회수]")
            rid = input("영업일지 ID: ").strip()
            result = withdraw_report(rid)
            print(result["message"])

        elif choice == 15:
            print("\n[고객사 활동 요약]")
            cid = input("고객사 ID: ").strip()
            summary = get_customer_summary(cid)
            print(f"  고객사 ID: {summary['customer_id']}")
            print(f"  전체 영업일지: {summary['total_reports']}건")
            print(f"  DRAFT: {summary['draft']}건")
            print(f"  SUBMITTED: {summary['submitted']}건")
            print(f"  APPROVED: {summary['approved']}건")
            print(f"  REJECTED: {summary['rejected']}건")

        elif choice == 16:
            print("\n[전체 활동 요약]")
            summaries = get_all_summaries()
            if not summaries:
                print("등록된 고객사가 없습니다.")
            else:
                for s in summaries:
                    print(f"  {s.get('customer_name', s['customer_id'])}: 총 {s['total_reports']}건 "
                          f"(DRAFT:{s['draft']}, SUBMITTED:{s['submitted']}, "
                          f"APPROVED:{s['approved']}, REJECTED:{s['rejected']})")

        else:
            print("존재하지 않는 메뉴입니다. 다시 선택해 주세요.")


if __name__ == "__main__":
    run()