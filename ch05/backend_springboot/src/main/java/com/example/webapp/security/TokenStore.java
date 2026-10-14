package com.example.webapp.security;

import org.springframework.stereotype.Component;
import java.security.SecureRandom;
import java.util.HexFormat;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * ch05/backend_springboot/.../security/TokenStore.java
 * 로그인 성공 시 발급한 토큰을 서버 메모리에 저장한다.
 * (실제 서비스에서는 Redis 등 공유 저장소나 JWT 자체 서명 검증을 사용한다)
 */
@Component
public class TokenStore {

    private final Map<String, Long> tokenToMemberId = new ConcurrentHashMap<>();
    private final SecureRandom random = new SecureRandom();

    public String issue(Long memberId) {
        byte[] bytes = new byte[16];
        random.nextBytes(bytes);
        String token = HexFormat.of().formatHex(bytes);
        tokenToMemberId.put(token, memberId);
        return token;
    }

    public Long getMemberId(String token) {
        return tokenToMemberId.get(token);
    }
}
