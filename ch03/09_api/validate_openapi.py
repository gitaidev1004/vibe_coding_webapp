"""
ch03/09_api/validate_openapi.py
openapi_spec.yaml이 CRUD API 명세로서 최소한의 요건(리소스별 CRUD
메서드와 정상/오류 응답 코드)을 갖추었는지 점검하는 예제입니다.
"""
import yaml
from pathlib import Path

REQUIRED_METHODS_FOR_COLLECTION = {"get", "post"}
REQUIRED_METHODS_FOR_ITEM = {"get", "put", "delete"}


def load_spec(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_crud_completeness(spec):
    issues = []
    paths = spec.get("paths", {})

    collection_paths = [p for p in paths if not p.endswith("}")]
    item_paths = [p for p in paths if p.endswith("}")]

    for p in collection_paths:
        methods = set(paths[p].keys())
        missing = REQUIRED_METHODS_FOR_COLLECTION - methods
        if missing:
            issues.append(f"{p} : {', '.join(missing)} 메서드가 없습니다.")

    for p in item_paths:
        methods = set(paths[p].keys())
        missing = REQUIRED_METHODS_FOR_ITEM - methods
        if missing:
            issues.append(f"{p} : {', '.join(missing)} 메서드가 없습니다.")

    return issues


def check_error_responses(spec):
    issues = []
    for path, methods in spec.get("paths", {}).items():
        for method, detail in methods.items():
            responses = detail.get("responses", {})
            has_success = any(code.startswith("2") for code in responses)
            has_error = any(code.startswith("4") for code in responses)
            if not has_success:
                issues.append(f"{method.upper()} {path} : 성공(2xx) 응답이 정의되지 않았습니다.")
            if not has_error:
                issues.append(f"{method.upper()} {path} : 오류(4xx) 응답이 정의되지 않았습니다.")
    return issues


if __name__ == "__main__":
    spec_path = Path(__file__).parent / "openapi_spec.yaml"
    spec = load_spec(spec_path)

    print("=== API 명세 점검 ===")
    print(f"대상 파일: {spec_path.name}")
    print(f"정의된 경로 수: {len(spec['paths'])}개")

    crud_issues = check_crud_completeness(spec)
    print(f"\n[CRUD 완전성 점검] 문제 {len(crud_issues)}건")
    for issue in crud_issues:
        print(f"  - {issue}")
    if not crud_issues:
        print("  모든 리소스가 필요한 CRUD 메서드를 갖추고 있습니다.")

    error_issues = check_error_responses(spec)
    print(f"\n[응답 코드 점검] 문제 {len(error_issues)}건")
    for issue in error_issues:
        print(f"  - {issue}")
    if not error_issues:
        print("  모든 API가 성공/오류 응답 코드를 모두 정의하고 있습니다.")
