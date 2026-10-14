package com.example.webapp.security;

import java.lang.annotation.*;

/** 컨트롤러 매개변수에 현재 로그인한 회원을 주입하기 위한 커스텀 어노테이션 */
@Target(ElementType.PARAMETER)
@Retention(RetentionPolicy.RUNTIME)
public @interface CurrentMember {
}
