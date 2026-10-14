package com.example.webapp.entity;

import jakarta.persistence.*;

/**
 * ch05/backend_springboot/.../entity/Permission.java
 * 권한(permission) 엔터티 - role과 function의 N:M 관계를 복합키로 표현한다.
 */
@Entity
@Table(name = "permission")
@IdClass(PermissionId.class)
public class Permission {

    @Id
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "role_id")
    private Role role;

    @Id
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "function_id")
    private Function function;

    private boolean canRead;
    private boolean canWrite;

    protected Permission() {}

    public Permission(Role role, Function function, boolean canRead, boolean canWrite) {
        this.role = role;
        this.function = function;
        this.canRead = canRead;
        this.canWrite = canWrite;
    }

    public Role getRole() { return role; }
    public Function getFunction() { return function; }
    public boolean isCanRead() { return canRead; }
    public boolean isCanWrite() { return canWrite; }
}
