"""
ch06/04_security/xss_demo.py
XSS(Cross-Site Scripting) 취약점이 발생하는 상황과, HTML 이스케이프로
이를 방어하는 방법을 실제 코드로 확인하는 예제입니다.
"""
import html


def render_unsafe(comment_content: str) -> str:
    """[취약한 코드] 사용자 입력을 이스케이프 없이 그대로 HTML에 삽입한다."""
    return f"<div class='comment'>{comment_content}</div>"


def render_safe(comment_content: str) -> str:
    """[안전한 코드] html.escape()로 특수문자를 이스케이프한 뒤 삽입한다."""
    escaped = html.escape(comment_content)
    return f"<div class='comment'>{escaped}</div>"


if __name__ == "__main__":
    malicious_comment = "<script>alert('당신의 쿠키: ' + document.cookie)</script>"

    print("=== 정상적인 댓글 렌더링 ===")
    print(render_unsafe("안녕하세요! 좋은 글 감사합니다."))

    print("\n=== 악성 스크립트가 담긴 댓글 (취약한 렌더링) ===")
    unsafe_html = render_unsafe(malicious_comment)
    print(unsafe_html)
    contains_script_tag = "<script>" in unsafe_html
    print(f"  -> 브라우저가 실행 가능한 <script> 태그가 그대로 포함됨: {contains_script_tag}")

    print("\n=== 동일한 악성 댓글 (안전한 렌더링) ===")
    safe_html = render_safe(malicious_comment)
    print(safe_html)
    contains_script_tag_safe = "<script>" in safe_html
    print(f"  -> <script> 태그가 텍스트로 무력화됨(실행 불가능): {contains_script_tag_safe}")
