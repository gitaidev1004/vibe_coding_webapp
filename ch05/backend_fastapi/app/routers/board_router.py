"""
ch05/backend_fastapi/app/routers/board_router.py
게시글 목록/검색/페이징, 상세, 등록, 수정, 삭제 API
"""
from fastapi import APIRouter, Depends, Query
from app.schemas.board import (
    PostCreateRequest, PostUpdateRequest,
    PostListItemResponse, PostDetailResponse, PagedPostResponse,
)
from app.services.board_service import BoardService
from app.deps import get_board_service, get_current_member
from app.models.member import Member
from app.models.board import Post

router = APIRouter(prefix="/api/posts", tags=["posts"])


def to_list_item(post: Post) -> PostListItemResponse:
    return PostListItemResponse(
        post_id=post.post_id, title=post.title, author=post.member.username,
        view_count=post.view_count, created_at=post.created_at,
    )


def to_detail(post: Post) -> PostDetailResponse:
    return PostDetailResponse(
        post_id=post.post_id, board_id=post.board_id, title=post.title, content=post.content,
        author=post.member.username, view_count=post.view_count,
        created_at=post.created_at, updated_at=post.updated_at,
    )


@router.get("", response_model=PagedPostResponse)
def list_posts(
    keyword: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    service: BoardService = Depends(get_board_service),
):
    items, total = service.list_posts(keyword, page, page_size)
    return PagedPostResponse(
        items=[to_list_item(p) for p in items], total=total, page=page, page_size=page_size,
    )


@router.get("/{post_id}", response_model=PostDetailResponse)
def get_post(post_id: int, service: BoardService = Depends(get_board_service)):
    return to_detail(service.get_post(post_id))


@router.post("", response_model=PostDetailResponse, status_code=201)
def create_post(
    request: PostCreateRequest, board_id: int = Query(default=1),
    service: BoardService = Depends(get_board_service),
    member: Member = Depends(get_current_member),
):
    post = service.create_post(board_id, member.member_id, request)
    return to_detail(service.get_post(post.post_id, increase_view=False))


@router.put("/{post_id}", response_model=PostDetailResponse)
def update_post(
    post_id: int, request: PostUpdateRequest,
    service: BoardService = Depends(get_board_service),
    member: Member = Depends(get_current_member),
):
    post = service.update_post(post_id, member.member_id, request)
    return to_detail(post)


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    service: BoardService = Depends(get_board_service),
    member: Member = Depends(get_current_member),
):
    is_admin = member.role.role_name == "ADMIN"
    service.delete_post(post_id, member.member_id, is_admin)
