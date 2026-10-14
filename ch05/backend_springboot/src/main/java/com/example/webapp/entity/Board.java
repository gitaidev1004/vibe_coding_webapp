package com.example.webapp.entity;

import jakarta.persistence.*;

/**
 * ch05/backend_springboot/.../entity/Board.java
 * 게시판(board) 엔터티
 */
@Entity
@Table(name = "board")
public class Board {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long boardId;

    @Column(nullable = false, length = 50)
    private String boardName;

    @Column(length = 200)
    private String description;

    protected Board() {}

    public Board(String boardName, String description) {
        this.boardName = boardName;
        this.description = description;
    }

    public Long getBoardId() { return boardId; }
    public String getBoardName() { return boardName; }
}
