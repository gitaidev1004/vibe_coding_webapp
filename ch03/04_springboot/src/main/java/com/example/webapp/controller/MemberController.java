package com.example.webapp.controller;

import com.example.webapp.entity.Member;
import com.example.webapp.service.MemberService;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

/**
 * ch03/04_springboot/.../controller/MemberController.java
 * Spring Boot Layered MVC - Controller 계층
 * HTTP 요청을 받아 Service 계층으로 전달하고, 결과를 JSON 응답으로 반환한다.
 */
@RestController
@RequestMapping("/api/members")
public class MemberController {

    private final MemberService memberService;

    public MemberController(MemberService memberService) {
        this.memberService = memberService;
    }

    @PostMapping
    public Member signup(@RequestBody Map<String, String> request) {
        return memberService.signup(
                request.get("username"),
                request.get("password"),
                request.get("email")
        );
    }

    @GetMapping
    public List<Member> getMembers() {
        return memberService.getMembers();
    }
}
