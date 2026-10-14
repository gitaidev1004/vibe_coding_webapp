package com.example.webapp.service;

import com.example.webapp.entity.Function;
import com.example.webapp.entity.Member;
import com.example.webapp.entity.Permission;
import com.example.webapp.entity.PermissionId;
import com.example.webapp.repository.FunctionRepository;
import com.example.webapp.repository.PermissionRepository;
import com.example.webapp.security.ApiException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

/**
 * ch05/backend_springboot/.../service/AccessControlService.java
 * 접근제어(Access Control) 서비스.
 * 사용자 확인 -> 역할 확인 -> 권한 확인 -> 기능 실행/접근 차단의 흐름을 구현한다.
 */
@Service
public class AccessControlService {

    private final FunctionRepository functionRepository;
    private final PermissionRepository permissionRepository;
    private final LogService logService;

    public AccessControlService(FunctionRepository functionRepository,
                                 PermissionRepository permissionRepository, LogService logService) {
        this.functionRepository = functionRepository;
        this.permissionRepository = permissionRepository;
        this.logService = logService;
    }

    public void checkPermission(Member member, String functionCode, boolean needWrite) {
        // ① 사용자 확인
        if (!member.isActive()) deny(member, functionCode, "사용 중지된 계정");

        // ② 역할 확인
        if (member.getRole() == null) deny(member, functionCode, "역할 없음");

        // ③ 권한 확인
        Function function = functionRepository.findByFunctionCode(functionCode)
                .orElse(null);
        if (function == null) { deny(member, functionCode, "존재하지 않는 기능"); return; }

        Permission permission = permissionRepository
                .findById(new PermissionId(member.getRole().getRoleId(), function.getFunctionId()))
                .orElse(null);
        if (permission == null) { deny(member, functionCode, "권한 없음"); return; }

        if (needWrite && !permission.isCanWrite()) deny(member, functionCode, "쓰기 권한 없음");
        if (!needWrite && !permission.isCanRead()) deny(member, functionCode, "읽기 권한 없음");

        // ④ 기능 실행 허용
        logService.record(member.getMemberId(), "ACCESS_GRANTED", functionCode);
    }

    private void deny(Member member, String functionCode, String reason) {
        // ⑥ 접근 차단
        logService.record(member.getMemberId(), "ACCESS_DENIED", functionCode + " (" + reason + ")");
        throw new ApiException("접근 권한이 없습니다: " + reason, HttpStatus.FORBIDDEN);
    }
}
