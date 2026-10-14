package com.example.webapp.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * ch05/backend_springboot/.../entity/Post.java
 * 게시글(post) 엔터티
 */
@Entity
@Table(name = "post")
public class Post {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long postId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "board_id", nullable = false)
    private Board board;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "member_id", nullable = false)
    private Member member;

    @Column(nullable = false, length = 200)
    private String title;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String content;

    @Column(nullable = false)
    private int viewCount = 0;

    @Column(nullable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    private LocalDateTime updatedAt;

    protected Post() {}

    public Post(Board board, Member member, String title, String content) {
        this.board = board;
        this.member = member;
        this.title = title;
        this.content = content;
    }

    public Long getPostId() { return postId; }
    public Board getBoard() { return board; }
    public Member getMember() { return member; }
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    public int getViewCount() { return viewCount; }
    public void increaseViewCount() { this.viewCount++; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
