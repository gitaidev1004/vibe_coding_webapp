package com.example.webapp.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * ch05/backend_springboot/.../entity/Log.java
 * 사용자 활동 이력을 저장하는 로그(log) 엔터티
 */
@Entity
@Table(name = "log")
public class Log {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long logId;

    private Long memberId;

    @Column(nullable = false, length = 50)
    private String action;

    private String target;

    @Column(nullable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    protected Log() {}

    public Log(Long memberId, String action, String target) {
        this.memberId = memberId;
        this.action = action;
        this.target = target;
    }

    public Long getLogId() { return logId; }
    public Long getMemberId() { return memberId; }
    public String getAction() { return action; }
    public String getTarget() { return target; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
