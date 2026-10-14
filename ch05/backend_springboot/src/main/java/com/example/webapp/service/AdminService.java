package com.example.webapp.service;

import com.example.webapp.entity.*;
import com.example.webapp.repository.*;
import com.example.webapp.security.ApiException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import java.util.List;

/**
 * ch05/backend_springboot/.../service/AdminService.java
 * 역할(Role), 권한(Permission) 관리 비즈니스 로직
 */
@Service
public class AdminService {

    private final RoleRepository roleRepository;
    private final FunctionRepository functionRepository;
    private final PermissionRepository permissionRepository;

    public AdminService(RoleRepository roleRepository, FunctionRepository functionRepository,
                         PermissionRepository permissionRepository) {
        this.roleRepository = roleRepository;
        this.functionRepository = functionRepository;
        this.permissionRepository = permissionRepository;
    }

    public Role createRole(String roleName, String description) {
        roleRepository.findByRoleName(roleName).ifPresent(r -> {
            throw new ApiException("이미 존재하는 역할입니다.", HttpStatus.BAD_REQUEST);
        });
        return roleRepository.save(new Role(roleName, description));
    }

    public List<Role> getRoles() {
        return roleRepository.findAll();
    }

    public void deleteRole(Long roleId) {
        Role role = roleRepository.findById(roleId)
                .orElseThrow(() -> new ApiException("역할을 찾을 수 없습니다.", HttpStatus.NOT_FOUND));
        roleRepository.delete(role);
    }

    public Permission setPermission(Long roleId, String functionCode, boolean canRead, boolean canWrite) {
        Role role = roleRepository.findById(roleId)
                .orElseThrow(() -> new ApiException("역할을 찾을 수 없습니다.", HttpStatus.NOT_FOUND));
        Function function = functionRepository.findByFunctionCode(functionCode)
                .orElseThrow(() -> new ApiException("기능을 찾을 수 없습니다.", HttpStatus.NOT_FOUND));

        Permission permission = new Permission(role, function, canRead, canWrite);
        return permissionRepository.save(permission);
    }
}
