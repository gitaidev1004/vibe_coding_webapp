package com.example.webapp.controller;

import com.example.webapp.entity.Log;
import com.example.webapp.entity.Member;
import com.example.webapp.entity.Permission;
import com.example.webapp.entity.Role;
import com.example.webapp.security.CurrentMember;
import com.example.webapp.service.AccessControlService;
import com.example.webapp.service.AdminService;
import com.example.webapp.service.LogService;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

/**
 * ch05/backend_springboot/.../controller/AdminController.java
 * 관리자 전용 API: 역할 관리, 권한 관리, 로그 조회
 */
@RestController
@RequestMapping("/api/admin")
public class AdminController {

    private final AdminService adminService;
    private final LogService logService;
    private final AccessControlService accessControlService;

    public AdminController(AdminService adminService, LogService logService,
                            AccessControlService accessControlService) {
        this.adminService = adminService;
        this.logService = logService;
        this.accessControlService = accessControlService;
    }

    @PostMapping("/roles")
    public Role createRole(@RequestBody Map<String, String> request, @CurrentMember Member member) {
        accessControlService.checkPermission(member, "ROLE_MANAGE", true);
        return adminService.createRole(request.get("roleName"), request.get("description"));
    }

    @GetMapping("/roles")
    public List<Role> getRoles(@CurrentMember Member member) {
        accessControlService.checkPermission(member, "ROLE_MANAGE", false);
        return adminService.getRoles();
    }

    @DeleteMapping("/roles/{roleId}")
    public void deleteRole(@PathVariable Long roleId, @CurrentMember Member member) {
        accessControlService.checkPermission(member, "ROLE_MANAGE", true);
        adminService.deleteRole(roleId);
    }

    @PostMapping("/permissions")
    public Permission setPermission(@RequestBody Map<String, Object> request, @CurrentMember Member member) {
        accessControlService.checkPermission(member, "ROLE_MANAGE", true);
        Long roleId = Long.valueOf(request.get("roleId").toString());
        String functionCode = (String) request.get("functionCode");
        boolean canRead = Boolean.TRUE.equals(request.get("canRead"));
        boolean canWrite = Boolean.TRUE.equals(request.get("canWrite"));
        return adminService.setPermission(roleId, functionCode, canRead, canWrite);
    }

    @GetMapping("/logs")
    public List<Log> getLogs(@CurrentMember Member member) {
        accessControlService.checkPermission(member, "LOG_VIEW", false);
        return logService.getRecentLogs();
    }
}
