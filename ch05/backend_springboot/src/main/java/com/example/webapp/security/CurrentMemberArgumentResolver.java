package com.example.webapp.security;

import com.example.webapp.entity.Member;
import com.example.webapp.repository.MemberRepository;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.core.MethodParameter;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.support.WebDataBinderFactory;
import org.springframework.web.context.request.NativeWebRequest;
import org.springframework.web.method.support.HandlerMethodArgumentResolver;
import org.springframework.web.method.support.ModelAndViewContainer;

/**
 * ch05/backend_springboot/.../security/CurrentMemberArgumentResolver.java
 * 컨트롤러 메서드 매개변수에 @CurrentMember Member member 를 선언하면,
 * Authorization 헤더의 토큰으로부터 현재 로그인한 회원을 자동으로 주입해 준다.
 */
@Component
public class CurrentMemberArgumentResolver implements HandlerMethodArgumentResolver {

    private final TokenStore tokenStore;
    private final MemberRepository memberRepository;

    public CurrentMemberArgumentResolver(TokenStore tokenStore, MemberRepository memberRepository) {
        this.tokenStore = tokenStore;
        this.memberRepository = memberRepository;
    }

    @Override
    public boolean supportsParameter(MethodParameter parameter) {
        return parameter.hasParameterAnnotation(CurrentMember.class);
    }

    @Override
    public Object resolveArgument(MethodParameter parameter, ModelAndViewContainer mavContainer,
                                   NativeWebRequest webRequest, WebDataBinderFactory binderFactory) {
        HttpServletRequest request = (HttpServletRequest) webRequest.getNativeRequest();
        String header = request.getHeader("Authorization");
        if (header == null || !header.startsWith("Bearer ")) {
            throw new ApiException("로그인이 필요합니다.", HttpStatus.UNAUTHORIZED);
        }
        String token = header.substring("Bearer ".length()).trim();
        Long memberId = tokenStore.getMemberId(token);
        if (memberId == null) {
            throw new ApiException("유효하지 않은 토큰입니다.", HttpStatus.UNAUTHORIZED);
        }
        return memberRepository.findById(memberId)
                .orElseThrow(() -> new ApiException("회원을 찾을 수 없습니다.", HttpStatus.UNAUTHORIZED));
    }
}
