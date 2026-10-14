package com.example.webapp.controller;

import com.example.webapp.entity.Board;
import com.example.webapp.entity.Member;
import com.example.webapp.entity.Post;
import com.example.webapp.repository.BoardRepository;
import com.example.webapp.security.ApiException;
import com.example.webapp.security.CurrentMember;
import com.example.webapp.service.BoardService;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

/**
 * ch05/backend_springboot/.../controller/PostController.java
 * 게시글 목록/검색/페이징, 상세, 등록, 수정, 삭제 API
 */
@RestController
@RequestMapping("/api/posts")
public class PostController {

    private final BoardService boardService;
    private final BoardRepository boardRepository;

    public PostController(BoardService boardService, BoardRepository boardRepository) {
        this.boardService = boardService;
        this.boardRepository = boardRepository;
    }

    @GetMapping
    public Page<Post> listPosts(@RequestParam(required = false) String keyword,
                                 @RequestParam(defaultValue = "1") int page,
                                 @RequestParam(defaultValue = "10") int pageSize) {
        return boardService.listPosts(keyword, page, pageSize);
    }

    @GetMapping("/{postId}")
    public Post getPost(@PathVariable Long postId) {
        return boardService.getPost(postId, true);
    }

    @PostMapping
    public Post createPost(@RequestParam(defaultValue = "1") Long boardId,
                            @RequestBody Map<String, String> request,
                            @CurrentMember Member member) {
        Board board = boardRepository.findById(boardId)
                .orElseThrow(() -> new ApiException("게시판을 찾을 수 없습니다.", HttpStatus.NOT_FOUND));
        return boardService.createPost(board, member, request.get("title"), request.get("content"));
    }

    @PutMapping("/{postId}")
    public Post updatePost(@PathVariable Long postId, @RequestBody Map<String, String> request,
                            @CurrentMember Member member) {
        return boardService.updatePost(postId, member.getMemberId(), request.get("title"), request.get("content"));
    }

    @DeleteMapping("/{postId}")
    public void deletePost(@PathVariable Long postId, @CurrentMember Member member) {
        boolean isAdmin = member.getRole().getRoleName().equals("ADMIN");
        boardService.deletePost(postId, member.getMemberId(), isAdmin);
    }
}
