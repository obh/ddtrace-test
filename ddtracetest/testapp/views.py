import asyncio
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rest_framework.decorators import api_view

# A simple async function that we'll call with async_to_sync
async def dummy_async_operation():
    # Simulate some async work
    await asyncio.sleep(1)
    return "Hello World"

@api_view(['GET'])
def test_async_view(request):
    """
    A test view that uses async_to_sync to demonstrate the ddtrace issue.
    This should fail when run with ddtrace-run but work normally otherwise.
    """
    try:
        # This is the line that will trigger the error with ddtrace-run
        result = async_to_sync(dummy_async_operation)()
        
        # Return a success response
        return JsonResponse({
            "status": "success",
            "message": result,
            "details": "async_to_sync call completed successfully"
        })
    except Exception as e:
        # Return the error details for debugging
        import traceback
        traceback.print_exc()
        return JsonResponse({
            "status": "error",
            "error_type": str(type(e)),
            "message": str(e),
            "details": "Error occurred during async_to_sync call"
        }, status=500)