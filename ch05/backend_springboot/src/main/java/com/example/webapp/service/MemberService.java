package com.example.webapp.service;

import com.example.webapp.entity.Member;
import com.example.webapp.entity.Role;
import com.example.webapp.repository.MemberRepository;
import com.example.webapp.repository.RoleRepository;
import com.example.webapp.security.ApiException;
import com.example.webapp.security.PasswordUtil;
import com.example.webapp.security.TokenStore;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import java.util.List;

/**
 * ch05/backend_springboot/.../service/MemberService.java
 * 회원가입, 로그인, 회원 조회·수정·삭제(사용 여부 포함) 비즈니스 로직
 */
@Service
public class MemberService {

    private final MemberRepository memberRepository;
    private final RoleRepository roleRepository;
    private final TokenStore tokenStore;
    private final LogService logService;

    public MemberService(MemberRepository memberRepository, RoleRepository roleRepository,
                          TokenStore tokenStore, LogService logService) {
        this.memberRepository = memberRepository;
        this.roleRepository = roleRepository;
        this.tokenStore = tokenStore;
        this.logService = logService;
    }

    public Member signup(String username, String password, String email) {
        memberRepository.findByUsername(username).ifPresent(m -> {
            throw new ApiException("이미 사용 중인 아이디입니다.", HttpStatus.BAD_REQUEST);
        });
        Role defaultRole = roleRepository.findByRoleName("MEMBER")
                .orElseThrow(() -> new ApiException("기본 역할(MEMBER)이 설정되어 있지 않습니다.", HttpStatus.INTERNAL_SERVER_ERROR));

        Member member = new Member(username, PasswordUtil.hash(password), email, defaultRole);
        return memberRepository.save(member);
    }

    public String login(String username, String password) {
        Member member = memberRepository.findByUsername(username)
                .orElseThrow(() -> new ApiException("아이디 또는 비밀번호가 올바르지 않습니다.", HttpStatus.UNAUTHORIZED));

        if (!PasswordUtil.verify(password, member.getPassword())) {
            throw new ApiException("아이디 또는 비밀번호가 올바르지 않습니다.", HttpStatus.UNAUTHORIZED);
        }
        if (!member.isActive()) {
            throw new ApiException("사용이 중지된 계정입니다.", HttpStatus.FORBIDDEN);
        }

        String token = tokenStore.issue(member.getMemberId());
        logService.record(member.getMemberId(), "LOGIN", member.getUsername());
        return token;
    }

    public Member getMember(Long memberId) {
        return memberRepository.findById(memberId)
                .orElseThrow(() -> new ApiException("회원을 찾을 수 없습니다.", HttpStatus.NOT_FOUND));
    }

    public List<Member> getMembers() {
        return memberRepository.findAll();
    }

    public Member updateMember(Long memberId, String email, Boolean isActive) {
        Member member = getMember(memberId);
        if (email != null) member.setEmail(email);
        if (isActive != null) member.setActive(isActive);
        return memberRepository.save(member);
    }

    public void deleteMember(Long memberId) {
        memberRepository.delete(getMember(memberId));
    }
}
