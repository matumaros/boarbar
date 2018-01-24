# servare
The Django code for the website www.servare.org

## <u>English</u>
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


<b>Copyright ©2018</b>

#### Configure

Create a config.json file to keep private credentials to use by settings files:
```
{

        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "DB_NAME": "your database name",
        "DB_USER": "your database user",
        "DB_PASS": "your database password",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "SECRET_KEY": "your secret key"
}
```