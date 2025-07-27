from backend.app import create_app,db
from backend.app.models.user import User
from backend.app.models.assessment import Assessment
from backend.app.models.question import Question
from backend.app.models.invitation import Invitation
from backend.app.models.response import Response
from backend.app.models.feedback import Feedback
from backend.app.models.result import Result
from backend.app.models.submission import Submission

def run_tests():
    print("Smart Recruiter Minitests running...")

    app=create_app()

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
                print(f"{assess.title} | Time_Limit: {assess.time_limit} mins | Owner: {assess.recruiter_id}")


            print("\n Running Question Tests...")
            questions=Question.query.all()
            assert questions, "No questions found!"
            for q in questions:
                print(f"{q.question_text} [{q.question_type}] | Assessment ID: {q.assessment_id}")


            print("\n Running Invitation Tests")    
            invites=Invitation.query.all()
            assert invites, "No invitations found!"
            for i in invites:
                print(f"Invite to user {i.interviewee_id} for Assessment {i.assessment_id} | Status: {i.status}")
                

            print("\n Running Response Tests")    
            responses=Response.query.all()
            if responses:
                for r in responses:
                    print(f"Response by user {r.interviewee_id} on Q{r.question_id}: {r.answer_text}")
            else:
                print("No responses found!")   

              
            print("\n Running Submission Tests")       
            submissions=Submission.query.all()
            if submissions:
                for s in submissions:
                    print(f"Submission ID {s.id} by Interviewee {s.interviewee_id}  for Assessment {s.assessment_id} | Submitted: {s.submitted_at}")
            else:
                print("No submissions found!")        


            print("\n Running Result Tests")    
            results=Result.query.all()
            if results:
                for r in results:
                    print(f"Result ID {r.id} for Submission {r.submission_id} | Score: {r.total_score}")
            else:
                print("No results found!")        


            print("\n Running Feedback Tests")    
            feedbacks=Feedback.query.all()
            if feedbacks:
                for f in feedbacks:
                    print(f"Feedback ID {f.id} by Recruiter {f.recruiter_id} on Submission {f.submission_id} | Comment: {f.comment}")
            else:
                print("No feedbacks found!")   


            print("\n All Smart Recruiter Minitests Passed.")



        except AssertionError as e:
            print(f"\n Test Failed: {str(e)}")
        except Exception as e:
            print(f"\n Error: {str(e)}")    



if __name__=='__main__':
    run_tests()

