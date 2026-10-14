package com.example.webapp.repository;

import com.example.webapp.entity.Member;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

/**
 * ch03/04_springboot/.../repository/MemberRepository.java
 * Spring Boot Layered MVC - Repository 계층
 * JpaRepository를 상속하면 기본 CRUD 메서드가 자동으로 제공된다.
 */
public interface MemberRepository extends JpaRepository<Member, Long> {

    Optional<Member> findByUsername(String username);
}
