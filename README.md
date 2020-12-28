# ajax_validation
ajax_validation is a package that's used to display django form's validation errors in html templates without refreshing the pages.

# Installation
```bash
pip install ajax-validation
```
after the installation add it to your **settings.py**
```python
INSTALLED_APPS = [
    'your_app.apps.YourAppConfig',   
    'ajax_validation', # add this
    
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
                'ajax_validation.core.write_context_processor', # add this
            ],
        },
    },
]
```
# Examples of usage
```python

```
