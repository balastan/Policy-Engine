# Policy-Engine
Here is the Dockerized OPA policy engine setup and implementation.

Prerequisites
  This tutorial requires "Docker Compose" to run a demo web server along with OPA.
  Docker Compose : https://docs.docker.com/compose/install/

Steps

1. First, docker-compose.yml file that runs OPA and the demo web server.

    Then run docker-compose to pull and run the containers.

    docker-compose -f docker-compose.yml up

    The Docker container has two servers running on different ports.
    Python server, Which is for receiving the request and creating a formatted input request for the Open Policy Agent. 
    OPA server, Which is doing policy evaluation and generates arbitrary structured data as output.

    Every time the demo web server receives an HTTP request, it asks OPA to decide whether an HTTP API is authorized or not using a single RESTful API call.

2. Load a policy into OPA

    curl -X PUT --data-binary @user_policy.rego localhost:8181/v1/policies/user
  
3. Load the Data into OPA

    curl -X PUT --data-binary @users.json localhost:8181/v1/data
  
4. Then send a request to python server, Which will give a response as either {allow: true} or {allow: false}.

	Curl --request GET -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJrTkNNVGMxTXpCRVJqVTFNVUUyTlVGQ01rWkRNVUpCTUVRNU5EZEJRVFk1TmtFMU9EWTNNdyJ9.eyJodHRwczovL215cm9sZXMuY29tL3JvbGVzIjpbXSwiaXNzIjoiaHR0cHM6Ly9hdXRoLm15LnFhLmNoYXJpdGFibGVpbXBhY3QuY29tLyIsInN1YiI6ImF1dGgwfDk5OTAwMCIsImF1ZCI6WyJodHRwczovL2NoaW1wdGVjaC1xYS5hdXRoMC5jb20vYXBpL3YyLyIsImh0dHBzOi8vY2hpbXB0ZWNoLXFhLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTQzNzY0MDgsImV4cCI6MTU5NDM4MzYwOCwiYXpwIjoiR2FtRHBLcHJuOTZkaHBiOFVabUtEenRLTWVuSFZDbk0iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIn0.NEBVA4EiFvW3eZEOQIBydRk45Yyfaf9zsnNjRewl4dcW_jp17RVDFTCtRo_pTGW67z5S-aZtTBxumlxdEnf_En-h81JBa5_7n21Igl8lKDl33idAVPXvrkwEDBXWBWi87OegNd6RYpp893XxJ2vdQu7hwUJo5QzW4GEHteAHx-K1JZfOLCAVtMpbXRuTtTs-lWZ6ceVGCRbwXcY18INbb1YbOoZ4Y1Dt6Nbj-N7YSL9UTbfVqCXL4Rx9xOzi0KWrOnWNcLhsWQxI5s-Q1OFh7H1X8Nsn5Hj39tekD46qOqfMRRyQQiLQZevUtewnjlCcVzLgfi6MT0iBrMqkfygh-A" localhost:5050/groups/1

