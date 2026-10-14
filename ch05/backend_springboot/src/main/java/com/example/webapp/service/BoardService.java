package com.example.webapp.service;

import com.example.webapp.entity.Board;
import com.example.webapp.entity.Member;
import com.example.webapp.entity.Post;
import com.example.webapp.repository.PostRepository;
import com.example.webapp.security.ApiException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;

/**
 * ch05/backend_springboot/.../service/BoardService.java
 * 게시글 목록/검색/페이징, 상세 조회(조회수 증가), 등록, 수정, 삭제 비즈니스 로직
 */
@Service
public class BoardService {

    private final PostRepository postRepository;

    public BoardService(PostRepository postRepository) {
        this.postRepository = postRepository;
    }

    public Page<Post> listPosts(String keyword, int page, int pageSize) {
        if (page < 1) throw new ApiException("페이지 번호는 1 이상이어야 합니다.", HttpStatus.BAD_REQUEST);
        Pageable pageable = PageRequest.of(page - 1, pageSize, Sort.by(Sort.Direction.DESC, "postId"));
        String kw = keyword == null ? "" : keyword;
        return postRepository.findByTitleContainingOrContentContaining(kw, kw, pageable);
    }

    public Post getPost(Long postId, boolean increaseView) {
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ApiException("게시글을 찾을 수 없습니다.", HttpStatus.NOT_FOUND));
        if (increaseView) {
            post.increaseViewCount();
            postRepository.save(post);
        }
        return post;
    }

    public Post createPost(Board board, Member member, String title, String content) {
        return postRepository.save(new Post(board, member, title, content));
    }

    public Post updatePost(Long postId, Long memberId, String title, String content) {
        Post post = getPost(postId, false);
        if (!post.getMember().getMemberId().equals(memberId)) {
            throw new ApiException("작성자만 수정할 수 있습니다.", HttpStatus.FORBIDDEN);
        }
        post.setTitle(title);
        post.setContent(content);
        post.setUpdatedAt(LocalDateTime.now());
        return postRepository.save(post);
    }

    public void deletePost(Long postId, Long memberId, boolean isAdmin) {
        Post post = getPost(postId, false);
        if (!post.getMember().getMemberId().equals(memberId) && !isAdmin) {
            throw new ApiException("작성자 또는 관리자만 삭제할 수 있습니다.", HttpStatus.FORBIDDEN);
        }
        postRepository.delete(post);
    }
}
