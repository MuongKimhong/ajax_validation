# ajax_validation
**ajax_validation** is a django third party that can turn a POST request into an AJAX request and display Django form's validation errors in HTML template without refreshing the page and reduces amount of javascript code that developers need to write.

**Tested with:**
```bash
django == 3.0
python == 3.7
jquery == 3.5.1
```
# Installation
```bash
pip install ajax-validation
```
after the installation add it to your **settings.py**
```python
INSTALLED_APPS = [
    'your_app.apps.YourAppConfig',   
    'ajax_validation', # <----- add this
    
    'django.contrib.admin',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # ...
                'django.contrib.messages.context_processors.messages',
                'ajax_validation.core.write_context_processor', # <----- add this
            ],
        },
    },
]
```
and your html page (test.html) not the layout
```
{% include "ajax_validation/ajax_script.html" %} <---- include this in your html and make sure it's under jquery
```
# Examples of usage
Let's create a simple Django form to understand how to use ajax_validation
```python
# forms.py
from django import forms

class TestForm(forms.Form):
    name   = forms.CharField(widget=forms.TextInput())
    age    = forms.CharField(widget=forms.TextInput())
    
    class Meta:
        fields = ['name', 'age']
        
    def clean_name(self):
        name = self.cleaned_data['name']
        if name != "richard":
            raise forms.ValidationError("Sorry wrong name")
        return name
        
    def clean_age(self):
        age = self.cleaned_data['age']
        if int(age) < 18:
            raise forms.ValidationError("Sorry you're under 18")
        return age    
```
In views.py, import **context_processor** from ajax_validation package
```python
# views.py
from django.http import JsonResponse
from .forms import TestForm

from ajax_validation.core import context_processor # ajax_validation package

def test_view(request):
    form = TestForm()
    
    '''arguments below are required!'''
    
    url     = "{% url 'test' %}" # your post request url
    fields  = ['name', 'age']    # your form fields
    form_id = "#my-form"         # your form's id in html
    # your javascript code that will be executed if the request is successful
    success_code = '''
        alert("Request Success");
    '''
    context_processor(request, url, fields, form_id)
    
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            # Do not return as dict and please set safe to False
            return JsonResponse(success_code, status = 200, safe = False) 
        else:
            # 'form_errors' as dict key is required
            return JsonResponse({'form_errors': form.errors}, status = 400) 
    
    return render(request, 'your_app/test.html', {'form': form})
```
**success_code** is the javascript code that will be executed if the request is successful. In this case, it will alert a message. If you want to do something related to url like changing the url to new page like:
```python
success_code = '''
    window.location = "{% url 'about' %}"
'''
```
Please do not use django url and use actual url instead 
```python
# In case, path('about', about_view, name="about")

success_code = '''
    window.location = '/about/'
'''
```
In test.html
```
<body>
    <form action="{% url 'test' %}" id="my-form" method="POST">
      {% csrf_token %}
      {{form.name}}
      {{name_error}} <---- error response for name
      {{form.age}}
      {{age_error}} <---- error response for age
      <button type="submit">submit</button>
    </form>
    
    {% include "ajax_validation/ajax_script.html" %} <---- include this in your html and make sure it's under jquery
</body>
```
`{{name_error}}` and `{{age_error}}` are the error texts that will be displayed in html if we get error responses. 

**Syntax for it is `{{<field>_error}}`**

By default, `{{<field>_error}}` will be rendered as `<p id="<field>_error"><p>` and will be fade out after 4 seconds.
