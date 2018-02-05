# servare
The Django code for the website www.servare.org

### What is this project about?
It is a website to preserve, standardize and teach endangered languages.

### Why did you start this project?
The Bavarian Language is slowly being replaced by German. The reasons for that are immigrants, media and education majorly in German and because there is no standard for Bavarian. Many other languages are in a similar situation. I believe that the only way to counter that is to standardize these languages and give them a platform to show their legitimacy.

### Why did you choose "servare"?
"servare" is Latin and means "to keep", "to save" or "guard", which is very fitting for this project as I think.

### Can I contribute?
Yes! The more contributors the better.
If you want to contribute to the source code, just fork the repository and create pull requests.
If you want to contribute to anything else, please write me at mat@pyfection.com.
Currently you can't register on the website since it's still being tested, but once it's up and running everybody can contribute.

### How do I set it up locally?
```git clone https://github.com/pyfection/servare.git servare```

Create custom settings to adjust to your environment. By convention it's called "custom_settings" and it is placed in the same location as the normal settings. This file should look something like this:
```
from .settings import *


SECRET_KEY = '<your secret key here>'

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<your database name here>',
        'USER': '<your database user here>,
        'PASSWORD': '<your database password here>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

<b>Copyright ©2018</b>
