package com.example.webapp.entity;

import jakarta.persistence.*;

/**
 * ch05/backend_springboot/.../entity/Menu.java
 * 메뉴(menu) 엔터티 - parentId로 계층 구조를 표현한다.
 */
@Entity
@Table(name = "menu")
public class Menu {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long menuId;

    @Column(nullable = false, length = 50)
    private String menuName;

    private String url;
    private Long parentId;
    private int sortOrder;

    protected Menu() {}

    public Menu(String menuName, String url, int sortOrder) {
        this.menuName = menuName;
        this.url = url;
        this.sortOrder = sortOrder;
    }

    public Long getMenuId() { return menuId; }
    public String getMenuName() { return menuName; }
}
