package com.example.webapp.repository;

import com.example.webapp.entity.Post;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * ch05/backend_springboot/.../repository/PostRepository.java
 * 메서드 이름 규칙만으로 제목 또는 내용에 키워드가 포함된 게시글을
 * 페이징하여 조회하는 검색 쿼리가 자동 생성된다.
 */
public interface PostRepository extends JpaRepository<Post, Long> {
    Page<Post> findByTitleContainingOrContentContaining(String titleKeyword, String contentKeyword, Pageable pageable);
}
