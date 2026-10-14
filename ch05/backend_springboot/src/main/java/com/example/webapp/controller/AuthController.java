package com.example.webapp.controller;

import com.example.webapp.entity.Member;
import com.example.webapp.repository.MemberRepository;
import com.example.webapp.service.MemberService;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

/**
 * ch05/backend_springboot/.../controller/AuthController.java
 * 로그인 API
 */
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final MemberService memberService;
    private final MemberRepository memberRepository;

    public AuthController(MemberService memberService, MemberRepository memberRepository) {
        this.memberService = memberService;
        this.memberRepository = memberRepository;
    }

    @PostMapping("/login")
    public Map<String, String> login(@RequestBody Map<String, String> request) {
        String token = memberService.login(request.get("username"), request.get("password"));
        Member member = memberRepository.findByUsername(request.get("username")).orElseThrow();
        return Map.of("token", token, "username", member.getUsername(),
                "roleName", member.getRole().getRoleName());
    }
}
