from celery import shared_task
import time
from evaluations.models import EvaluationRequest
from django.core.mail import send_mail
import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")


def simulate_llm_evaluation(prompt):
    return f"Simulated response for prompt: {prompt}"

@shared_task
def process_evaluation(eval_id):
    print(f"Starting task for evaluation {eval_id}")
    try:
        evaluation = EvaluationRequest.objects.get(request_id=eval_id)
        print(f"Found evaluation object: {evaluation.request_id}")
        
        time.sleep(5)  # Simulate evaluation delay
        evaluation.result = simulate_llm_evaluation(evaluation.input_prompt)
        evaluation.status = 'completed'
        evaluation.save()

        print(f"Evaluation {eval_id} completed with result: {evaluation.result}")
        # resend api email
        params: resend.Emails.SendParams = {
            "from": "LLM Evaluation <onboarding@resend.dev>",
            "to": ["idrismmchatriwala@gmail.com"],
            "subject": "LLM Evaluation Completed",
            "html": f"""<p>The LLM evaluation has been completed for request.
            </p>
            <p>Request ID: {eval_id}</p>
            <p>Result: {evaluation.result}</p>
            <p>Prompt: {evaluation.input_prompt}</p>
            <p>Response: {evaluation.result}</p>
            <p>Status: {evaluation.status}</p>
            <p>Created at: {evaluation.created_at}</p>
            <p>Updated at: {evaluation.updated_at}</p>
            """,
        }
        resend.Emails.send(params)
        return f"Task completed for evaluation {eval_id}"
    except Exception as e:
        print(f"Error processing evaluation {eval_id}: {str(e)}")
        raise 