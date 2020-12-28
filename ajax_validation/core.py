from django.utils.html import format_html


def write_context_processor(request):
    context = {}
    context['url'] = request.session['url']
    context['fields'] = request.session['fields']
    context['form_id'] = request.session['form_id']
    
    for err_field in request.session['fields']:
        context[err_field + "_error"] = request.session[err_field + "_error"]

    return context


def context_processor(request, url, fields, form_id):
    request.session['url'] = url
    request.session['fields'] = fields
    request.session['form_id'] = form_id

    for err_field in fields:
        request.session[err_field + "_error"] = format_html('<p id="{}_error"></p>'.format(err_field))

    write_context_processor(request)

