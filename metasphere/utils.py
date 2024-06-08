def is_ajax(request):
    """
    Determines if the incoming request is an AJAX request.
    This function checks for the 'X-Requested-With' header, which is commonly set to 'XMLHttpRequest' by many JavaScript libraries when making AJAX requests.
    """
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'
