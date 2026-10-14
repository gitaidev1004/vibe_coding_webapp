package com.example.webapp.config;

import com.example.webapp.entity.*;
import com.example.webapp.repository.*;
import com.example.webapp.security.PasswordUtil;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

/**
 * ch05/backend_springboot/.../config/DataSeeder.java
 * 애플리케이션 최초 구동 시 필요한 기본 데이터(역할, 메뉴, 기능, 권한, 게시판,
 * 관리자 계정)를 생성한다. (FastAPI/Flask의 seed.py와 동일한 데이터)
 */
@Component
public class DataSeeder implements CommandLineRunner {

    private final RoleRepository roleRepository;
    private final MenuRepository menuRepository;
    private final FunctionRepository functionRepository;
    private final PermissionRepository permissionRepository;
    private final BoardRepository boardRepository;
    private final MemberRepository memberRepository;

    public DataSeeder(RoleRepository roleRepository, MenuRepository menuRepository,
                       FunctionRepository functionRepository, PermissionRepository permissionRepository,
                       BoardRepository boardRepository, MemberRepository memberRepository) {
        this.roleRepository = roleRepository;
        this.menuRepository = menuRepository;
        this.functionRepository = functionRepository;
        this.permissionRepository = permissionRepository;
        this.boardRepository = boardRepository;
        this.memberRepository = memberRepository;
    }

    @Override
    public void run(String... args) {
        if (roleRepository.count() > 0) return;

        Role adminRole = roleRepository.save(new Role("ADMIN", "관리자"));
        roleRepository.save(new Role("MEMBER", "일반회원"));

        Menu boardMenu = menuRepository.save(new Menu("게시판 관리", "/board", 1));
        Menu adminMenu = menuRepository.save(new Menu("관리자", "/admin", 2));

        Function postManage = functionRepository.save(new Function("게시글 관리", "POST_MANAGE", boardMenu));
        Function memberManage = functionRepository.save(new Function("회원 관리", "MEMBER_MANAGE", adminMenu));
        Function roleManage = functionRepository.save(new Function("역할 관리", "ROLE_MANAGE", adminMenu));
        Function logView = functionRepository.save(new Function("로그 조회", "LOG_VIEW", adminMenu));

        for (Function f : new Function[]{postManage, memberManage, roleManage, logView}) {
            permissionRepository.save(new Permission(adminRole, f, true, true));
        }

        boardRepository.save(new Board("공지사항", "공지 게시판"));

        memberRepository.save(new Member("admin", PasswordUtil.hash("admin1234!"),
                "admin@example.com", adminRole));
    }
}
