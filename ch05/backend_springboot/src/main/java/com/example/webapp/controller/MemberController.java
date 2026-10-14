package com.example.webapp.controller;

import com.example.webapp.entity.Member;
import com.example.webapp.security.CurrentMember;
import com.example.webapp.service.AccessControlService;
import com.example.webapp.service.MemberService;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

/**
 * ch05/backend_springboot/.../controller/MemberController.java
 * 회원가입, 내 정보 조회, 회원 목록/수정/삭제(관리자) API
 */
@RestController
@RequestMapping("/api/members")
public class MemberController {

    private final MemberService memberService;
    private final AccessControlService accessControlService;

    public MemberController(MemberService memberService, AccessControlService accessControlService) {
        this.memberService = memberService;
        this.accessControlService = accessControlService;
    }

    @PostMapping
    public Member signup(@RequestBody Map<String, String> request) {
        return memberService.signup(request.get("username"), request.get("password"), request.get("email"));
    }

    @GetMapping("/me")
    public Member getMe(@CurrentMember Member member) {
        return member;
    }

    @GetMapping
    public List<Member> getMembers(@CurrentMember Member member) {
        accessControlService.checkPermission(member, "MEMBER_MANAGE", false);
        return memberService.getMembers();
    }

    @PutMapping("/{memberId}")
    public Member updateMember(@PathVariable Long memberId, @RequestBody Map<String, Object> request,
                                @CurrentMember Member member) {
        accessControlService.checkPermission(member, "MEMBER_MANAGE", true);
        String email = (String) request.get("email");
        Boolean isActive = (Boolean) request.get("isActive");
        return memberService.updateMember(memberId, email, isActive);
    }

    @DeleteMapping("/{memberId}")
    public void deleteMember(@PathVariable Long memberId, @CurrentMember Member member) {
        accessControlService.checkPermission(member, "MEMBER_MANAGE", true);
        memberService.deleteMember(memberId);
    }
}
