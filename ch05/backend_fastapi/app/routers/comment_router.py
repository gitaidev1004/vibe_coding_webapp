"""
ch05/backend_fastapi/app/routers/comment_router.py
댓글 등록/조회/삭제 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.comment import CommentCreateRequest, CommentResponse
from app.services.comment_service import CommentService
from app.repositories.comment_repository import CommentRepository
from app.repositories.board_repository import PostRepository
from app.deps import get_current_member
from app.models.member import Member

router = APIRouter(prefix="/api/posts/{post_id}/comments", tags=["comments"])


def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(CommentRepository(db), PostRepository(db))


def to_response(comment) -> CommentResponse:
    return CommentResponse(
        comment_id=comment.comment_id, author=comment.member.username,
        content=comment.content, created_at=comment.created_at,
    )


@router.get("", response_model=list[CommentResponse])
def get_comments(post_id: int, service: CommentService = Depends(get_comment_service)):
    return [to_response(c) for c in service.get_comments(post_id)]


@router.post("", response_model=CommentResponse, status_code=201)
def add_comment(post_id: int, request: CommentCreateRequest,
                 service: CommentService = Depends(get_comment_service),
                 member: Member = Depends(get_current_member)):
    comment = service.add_comment(post_id, member.member_id, request.content)
    return to_response(comment)


@router.delete("/{comment_id}", status_code=204)
def delete_comment(post_id: int, comment_id: int,
                    service: CommentService = Depends(get_comment_service),
                    member: Member = Depends(get_current_member)):
    service.delete_comment(comment_id, member.member_id)
