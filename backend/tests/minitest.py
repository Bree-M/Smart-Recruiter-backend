from backend.app import app,db
from backend.app.models.user import User
from backend.app.models.assessment import Assessment
from backend.app.models.question import Question
from backend.app.models.invitation import Invitation
from backend.app.models.response import Response

def run_tests():
    print("Smart Recruiter Minitests running...")

    with app.app_context():
        try:
            print("\n Running User Tests...")
            users=User.query.all()
            assert users, "No users found!"
            for user in users:
                print(f"{user.username}({user.email}) | Role:{user.role}")

            print("\n Running Assessment Tests...")    
            assessments=Assessment.query.all()
            assert assessments, "No assessment found!"
            for assess in assessments:
                print(f"{assess.title} | Duration: {assess.duration} mins | Owner: {assess.recruiter_id}")


            print("\n Running Question Tests...")
            questions=Question.query.all()
            assert questions, "No questions found!"
            for q in questions:
                print(f"{q.title} [{q.question_type}] | Assessment ID: {q.assessment_id}")


            print("\n Running Invitation Tests")    
            invites=Invitation.query.all()
            assert invites, "No invitations found!"
            for i in invites:
                print(f"Invite to user {i.interviewee_id} for Assessment {i.assessement_id} | Status: {i.status}")
                

            print("\n Running Response Tests")    
            responses=Response.query.all()
            if responses:
                for r in responses:
                    print(f"Response by user {r.interviewee_id} on Q{r.question_id}: {r.answer_text}")
            else:
                print("No responses found!")   

            print("\n All Smart Recruiter Minitests Passed.")         

        except AssertionError as e:
            print(f"\n Test Failed: {str(e)}")
        except Exception as e:
            print(f"\n Error: {str(e)}")    



if __name__=='__main__':
    run_tests()

