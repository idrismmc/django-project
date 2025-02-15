from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from evaluations.models import EvaluationRequest
from evaluations.tasks import process_evaluation

@csrf_exempt
def submit_evaluation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('input_prompt')

            if not prompt:
                return JsonResponse({'error': 'Input prompt is required'}, status=400)

            # Create a new evaluation record
            evaluation = EvaluationRequest.objects.create(input_prompt=prompt)
            
            # Try to enqueue task and log the result
            try:
                print(f"About to enqueue evaluation {evaluation.request_id}")
                task_result = process_evaluation.delay(evaluation.request_id)
                print(f"Task enqueued with ID: {task_result}")
                
                return JsonResponse({
                    'request_id': evaluation.request_id, 
                    'status': evaluation.status,
                    'task_id': task_result.id
                }, status=201)
            except Exception as e:
                print(f"Error enqueueing task: {str(e)}")
                return JsonResponse({'error': f'Failed to enqueue task: {str(e)}'}, status=500)
                
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_evaluation(request, eval_id):
    try:
        evaluation = EvaluationRequest.objects.get(request_id=eval_id)
        response = {
            'id': evaluation.request_id,
            'status': evaluation.status,
            'result': evaluation.result
        }
        return JsonResponse(response, status=200)
    except EvaluationRequest.DoesNotExist:
        return JsonResponse({'error': 'Evaluation not found'}, status=404)