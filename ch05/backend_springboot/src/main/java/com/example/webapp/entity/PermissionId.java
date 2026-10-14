package com.example.webapp.entity;

import java.io.Serializable;
import java.util.Objects;

/**
 * ch05/backend_springboot/.../entity/PermissionId.java
 * Permission 엔터티의 복합키(role_id + function_id)를 표현하는 클래스
 */
public class PermissionId implements Serializable {
    private Long role;
    private Long function;

    public PermissionId() {}

    public PermissionId(Long role, Long function) {
        this.role = role;
        this.function = function;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof PermissionId)) return false;
        PermissionId that = (PermissionId) o;
        return Objects.equals(role, that.role) && Objects.equals(function, that.function);
    }

    @Override
    public int hashCode() { return Objects.hash(role, function); }
}
