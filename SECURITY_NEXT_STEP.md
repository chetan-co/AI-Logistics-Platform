# Next Step: Security Hardening & Reliability

## Problems Found
1. **Passwords stored in plain text** — Critical security flaw
2. **No input validation** — Weight can be negative, dates can be garbage
3. **No rate limiting** — Login endpoint vulnerable to brute force
4. **No CORS configuration** — Missing cross-origin support
5. **Missing tests** — Register, PUT, DELETE endpoints untested
6. **No request logging** — No audit trail for operations
7. **Fragile error handling** — Some exceptions leak stack traces

## Plan
### 1. Password Security (bcrypt hashing)
- Add `bcrypt` to requirements
- Hash passwords on registration
- Verify hashed passwords on login

### 2. Backend Input Validation
- Add Pydantic validators: weight > 0, dates format, string lengths
- Validate origin/destination are non-empty strings

### 3. Rate Limiting
- Add simple IP-based rate limiting for `/login` and `/register`
- Max 10 attempts per minute per IP

### 4. CORS Middleware
- Add FastAPI CORS middleware allowing all origins in dev

### 5. Comprehensive Tests
- Tests for register, register duplicate, PUT, DELETE, 404 cases

### 6. Request Logging
- Add structured logging middleware
- Log all API requests with method, path, status, duration
</create_file>
