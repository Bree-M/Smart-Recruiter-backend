#Register recruiter
# curl -X POST http://127.0.0.1:5000/auth/register \
# -H "Content-Type: application/json" \
# -d '{
#   "username": "recruiter_john",
#   "email": "john@company.com",
#   "password": "test123",
#   "role": "recruiter"
# }'


#Register candidate
# curl -X POST http://127.0.0.1:5000/auth/register \
# -H "Content-Type: application/json" \
# -d '{
#   "username": "candidate_jane",
#   "email": "jane@email.com",
#   "password": "test123",
#   "role": "candidate"
# }'


#Login recruiter
# curl -X POST http://127.0.0.1:5000/auth/login \
# -H "Content-Type: application/json" \
# -d '{
#   "email": "john@company.com",
#   "password": "test123"
# }'


#Login candidate
# curl -X POST http://127.0.0.1:5000/auth/login \
# -H "Content-Type: application/json" \
# -d '{
#   "email": "jane@email.com",
#   "password": "test123"
# }'


#Get recriter profile
# curl -X GET http://127.0.0.1:5000/auth/me \
# -H "User-ID: RECRUITER_ID"


#Get candidate profile
# curl -X GET http://127.0.0.1:5000/auth/me \
# -H "User-ID: CANDIDATE_ID"

#Recruiter dashboard 
# curl -X GET http://127.0.0.1:5000/auth/dashboard \
# -H "User-ID: RECRUITER_ID"


#Candidate dashboard 
# curl -X GET http://127.0.0.1:5000/auth/dashboard \
# -H "User-ID: CANDIDATE_ID"

#Recruiter only
# curl -X GET http://127.0.0.1:5000/auth/recruiter-area \
# -H "User-ID: RECRUITER_ID"

#Recruiter-only area
# curl -X GET http://127.0.0.1:5000/auth/recruiter-area \
# -H "User-ID: CANDIDATE_ID"

#Candidate-only area
# curl -X GET http://127.0.0.1:5000/auth/candidate-area \
# -H "User-ID: CANDIDATE_ID"

#candidate-only area
# curl -X GET http://127.0.0.1:5000/auth/candidate-area \
# -H "User-ID: RECRUITER_ID"


#logout
# curl -X POST http://127.0.0.1:5000/auth/logout







