#A/B Testing Application

Simple app to:

- Demonstrate one approach to doing [A/B Testing](http://en.wikipedia.org/wiki/A/B_testing) in a [Django](http://djangoproject.com) application


##Why

I wanted to play around with some ideas to learn more about A/B testing.  It's
far from complete.  It mainly serves as a platform for demonstrating one way to
automate scheduling an A/B test for a given portion of time.

Using this approach, admin users could login and 'schedule' an A/B test.  Then,
the designer/developer could discuss the test goals with the admin and execute
the code for the test with very minimal effort.

###Install

This application can be installed simply by installing the requirements
designated in the
[requirements.txt](https://github.com/durden/split_testing_playground/blob/master/requirements.txt)
file.

    - pip install -r requirements.txt
    - pip install -r chart_requirements.txt

Currently [PIL](http://www.pythonware.com/products/pil/) and
[ReportLab](http://www.reportlab.com/software/opensource/) are specified in the
[chart_requirements.txt](https://github.com/durden/split_testing_playground/blob/master/chart_requirements.txt)
file.  These requirements are not stricly necessary to run the application.
However, they allow the application to show a veritcal bar chart for conversion
rates.

###Deploy

The application can easily be deployed to [heroku](http://heroku.com) by:

    - git clone git://github.com/durden/split_testing_playground.git
    - 'cd' into the appliction directory
    - heroku create --stack cedar
    - git push heroku master
    - heroku run python manage.py syncdb

####Usage

Run the application:

- git clone git://github.com/durden/split_testing_playground.git
- 'cd' into the appliction directory
- Setup the database
    - python manage.py syncdb (make sure to create admin account)
- python manage.py runserver
- Browse to http://127.0.0.1:8000/
- Login
- [Create](http://127.0.0.1:8000/admin/registration/abtest/add/) an A/B
    test
- [Add A/B choices](http://127.0.0.1:8000/admin/registration/testchoice/)
- Use the database IDs from these choices to show them in the template
- For example see [example](https://github.com/durden/split_testing_playground/blob/master/templates/registration/register.html)

I've provided a sample database that will demonstrate the basic use of the
application.  It includes a single A/B with a few choices.  You can run the
existing test by modifying the start/end dates of the test.  You can also see
that there are already 'fake' results included for demonstration.

#####Technologies Used

- [Twitter Bootstrap](http://twitter.github.com/bootstrap/)
    - Nice and easy layouts, icon sets, etc.

#####Improvement Ideas

- Might be able to turn the main split testing view code into a decorator and
  more easily scale the idea to multiple views in the future
    - See [main view](https://github.com/durden/split_testing_playground/blob/master/registration/views.py#L46)
- Add a template tag to somehow more gracefully handle the switching on/off
  different UI choices for the actual test in the template.  I'm not too crazy
  about having to litter the code with a bunch of if statements, just haven't
  found a really good way to do it yet.
    - See [here](https://github.com/durden/split_testing_playground/blob/master/templates/registration/register.html#L31)
