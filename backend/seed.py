from backend.app import create_app,db
from backend.app.models.user import User
from backend.app.models.assessment import Assessment
from backend.app.models.question import Question
from backend.app.models.invitation import Invitation
from backend.app.models.response import Response
from backend.app.models.submission import Submission
from backend.app.models.result import Result
from backend.app.models.feedback import Feedback
from datetime import datetime

app=create_app()
with app.app_context():
    print("Dropping all tables")
    db.drop_all()
    print("Creating all tables")
    db.create_all()

    recruiter=User(username="Renee",email="renee@gmail.com",password="1234",role="recruiter")
    interviewee=User(username="Sapphire",email="sapphire@gmail.com",password="sappy1234",role="interviewee")
    db.session.add_all([recruiter,interviewee])
    db.session.commit()


    assessment=Assessment(
        title="Python Basics",
        description="A basic python assessment testing knowledge.",
        time_limit=60,
        recruiter_id=recruiter.id

    )
    db.session.add(assessment)
    db.session.commit()

    q1=Question(question_text="What is a list comprehension?",question_type="subjective",assessment_id=assessment.id,content="Explain what list comprehension are and give an example.")
    q2=Question(question_text="Print numbers 1 to 10 using a loop.",question_type="code",assessment_id=assessment.id,content="Use a for loop to print numbers 1 through 10.")
    db.session.add_all([q1,q2])
    db.session.commit()

    invitation=Invitation(
        interviewee_id=1,
        assessment_id=1,
        recruiter_id=1,
        status="pending",
        scheduled_at=datetime(2025,7,25,14,0)

    )
    db.session.add(invitation)
    db.session.commit()

    submission=Submission(
        interviewee_id=interviewee.id,
        assessment_id=assessment.id,
        start_time=datetime(2025,7,25,14,0),
        end_time=datetime(2025,7,25,15,0),
        submitted_at=datetime.utcnow()
    )
    db.session.add(submission)
    db.session.commit()


    r1=Response(question_id=q1.id,submission_id=submission.id,recruiter_id=recruiter.id,interviewee_id=interviewee.id,answer_text="It's a way to write loops in one line.",is_correct=None,score_awarded=None)
    r2=Response(question_id=q2.id,submission_id=submission.id,recruiter_id=recruiter.id,interviewee_id=interviewee.id,answer_text="for i in range(1,11): print(i)",is_correct=None,score_awarded=None)
    db.session.add_all([r1,r2])
    db.session.commit()


    result=Result(
        submission_id=submission.id,
        total_score=87.0,
        feedback_summary="Room for improvement,more context needed.",
        released=True,
        max_score=100
    )
    db.session.add(result)
    db.session.commit()


    f1=Feedback(response_id=r1.id,comment="Great progress!",recruiter_id=recruiter.id,submission_id=submission.id)
    f2=Feedback(response_id=r2.id,comment="Room for improvement!",recruiter_id=recruiter.id,submission_id=submission.id)
    db.session.add_all([f1,f2])
    db.session.commit()


    print("Seeding complete")