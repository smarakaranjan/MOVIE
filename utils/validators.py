from rest_framework.exceptions import ValidationError

def validate_query_params(request, allowed_params: list):
    """
    Validate that the query parameters in the request are allowed.

    :param request: DRF request object
    :param allowed_params: List of allowed query param names
    :raises ValidationError: if any unknown query param is present
    """
    unknown_params = [key for key in request.query_params if key not in allowed_params]
    if unknown_params:
        raise ValidationError({
            "error": "Invalid query parameters",
            "invalid_params": unknown_params,
            "allowed_params": allowed_params
        })
