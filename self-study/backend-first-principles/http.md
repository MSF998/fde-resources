## HTTP

- HTTP states that communication must always begin from the client
- TCP is the medium by which HTTP communicates with the client and server
- HTTP methods define the intent of the interaction
- GET, POST, PUT, PATCH, DELETE
- Idempotent states that when you call a method any number of times the result will always be the same. GET will always return the same result for the same requests
- CORS: It is a security mechanism enforced by browsers that control how web apps interact with resources hosted on differnt domains.
- CORS Specify how and who can interact

- Request

```
PUT /api/users/12345 HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82
Safari/537.36
Content-Type: application/json
Content-Length: 123
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: https://example.com/dashboard
Cookie: sessionId=abc123xyz456; lang=en-US

// a blank line here means, everything has been sent

{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "age": 30
}
```

- Response

```
HTTP/1.1 200 OK
Date: Fri, 20 Sep 2024 12:00:00 GMT
Content-Type: application/json
Content-Length: 85
Server: Apache/2.4.41 (Ubuntu)
Cache-Control: no-store
X-Request-ID: abcdef123456
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Set-Cookie: sessionId=abc123xyz456; Path=/; Secure; HttpOnly
Vary: Accept-Encoding
Connection: keep-alive

// a blank line here means, everything has been sent

{
  "message": "User updated successfully",
  "userId": 12345,
  "status": "success"
}
```
