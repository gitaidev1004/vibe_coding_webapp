package com.example.webapp.repository;

import com.example.webapp.entity.Permission;
import com.example.webapp.entity.PermissionId;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PermissionRepository extends JpaRepository<Permission, PermissionId> {
}
