package com.example.webapp.service;

import com.example.webapp.entity.Member;
import com.example.webapp.repository.MemberRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;

/**
 * ch03/04_springboot/.../service/MemberService.java
 * Spring Boot Layered MVC - Service 계층
 * 회원가입 시 아이디 중복 검사와 같은 비즈니스 로직을 처리한다.
 */
@Service
public class MemberService {

    private final MemberRepository memberRepository;

    public MemberService(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }

    public Member signup(String username, String password, String email) {
        memberRepository.findByUsername(username).ifPresent(m -> {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "이미 사용 중인 아이디입니다.");
        });
        // 실제 서비스에서는 password를 반드시 해시로 변환한 뒤 저장해야 한다.
        Member member = new Member(username, password, email);
        return memberRepository.save(member);
    }

    public java.util.List<Member> getMembers() {
        return memberRepository.findAll();
    }
}
