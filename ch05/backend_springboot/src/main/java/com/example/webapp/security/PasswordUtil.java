package com.example.webapp.security;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;

/**
 * ch05/backend_springboot/.../security/PasswordUtil.java
 * 비밀번호 해시 유틸리티. FastAPI/Flask 예제와 동일하게 SHA-256을 사용하여
 * 세 프레임워크의 결과를 비교하기 쉽게 하였다. (실무에서는 BCryptPasswordEncoder 권장)
 */
public class PasswordUtil {

    public static String hash(String rawPassword) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hashBytes = digest.digest(rawPassword.getBytes("UTF-8"));
            return HexFormat.of().formatHex(hashBytes);
        } catch (NoSuchAlgorithmException | java.io.UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        }
    }

    public static boolean verify(String rawPassword, String hashedPassword) {
        return hash(rawPassword).equals(hashedPassword);
    }
}
