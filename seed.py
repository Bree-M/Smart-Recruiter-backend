from datetime import datetime,timedelta
from backend.app import db
from backend.app.models.user import User
from backend.app.models.assessment import Assessment
from backend.app.models.question import Question
from backend.app.models.invitation import Invitation
from backend.app import create_app

app=create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    def users():
        user1=User(username="Renee",email="renee@dev.com",role="recruiter")
        user2=User(username="Sapphire",email="sapphire@info.com",role="interviewee")
        db.session.add_all(user1,user2)
        db.session.commit()
        return user1,user2
    
    def assessments(recruiter):
        assessment1=Assessment(
            title="Python Basics",
            description="Assessment on basic python knowledge",
            duration_minutes=45,
            created_by=recruiter.id
        )
        db.session.add(assessment1)
        db.session.commit()
        return assessment1
    
    def questions(assessment):
        q1=Question(
            question="What is the output of the print(2**3)?",
            question_type="multiple_choice",
            correct_answer="8",
            difficulty="easy",
            assessment_id=assessment.id
        )
        db.session.add(q1)
        db.session.commit()
        return q1
    
    def invitations(interviewee,recruiter,assessment):
        invite=Invitation(
            interviewee_id=interviewee.id,
            recruiter_id=recruiter.id,
            assessment_id=assessment.id,
            sent_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=3)

        )
        db.session.add(invite)
        db.session.commit()
        return invite
        
        recruiter,interviewee=users()
        assessments=assessments(recruiter)
        questions=questions(assessment)
        invite=invitations(interviewee,recruiter,assessment)
        

        print("Seeding complete")