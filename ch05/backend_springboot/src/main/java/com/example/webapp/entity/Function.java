package com.example.webapp.entity;

import jakarta.persistence.*;

/**
 * ch05/backend_springboot/.../entity/Function.java
 * 기능(function) 엔터티 - 메뉴에 속한 세부 기능을 표현한다.
 */
@Entity
@Table(name = "function")
public class Function {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long functionId;

    @Column(nullable = false, length = 50)
    private String functionName;

    @Column(nullable = false, unique = true, length = 50)
    private String functionCode;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "menu_id", nullable = false)
    private Menu menu;

    protected Function() {}

    public Function(String functionName, String functionCode, Menu menu) {
        this.functionName = functionName;
        this.functionCode = functionCode;
        this.menu = menu;
    }

    public Long getFunctionId() { return functionId; }
    public String getFunctionCode() { return functionCode; }
}
