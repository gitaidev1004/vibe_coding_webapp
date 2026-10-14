package com.example.webapp.entity;

import jakarta.persistence.*;
import java.util.List;

/**
 * ch05/backend_springboot/.../entity/Role.java
 * 역할(role) 엔터티
 */
@Entity
@Table(name = "role")
public class Role {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long roleId;

    @Column(nullable = false, unique = true, length = 30)
    private String roleName;

    @Column(length = 200)
    private String description;

    protected Role() {}

    public Role(String roleName, String description) {
        this.roleName = roleName;
        this.description = description;
    }

    public Long getRoleId() { return roleId; }
    public String getRoleName() { return roleName; }
    public String getDescription() { return description; }
}
