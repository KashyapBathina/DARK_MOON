# DarkMoon Grading
#### Video Demo:  <https://www.youtube.com/watch?v=_cEZMz6Iv24>
#### Description:

The program I created is a grading application that students, teachers, and gaurdians can use. From the teacher view it includes a grading system that automatically calculates and updates grades. It does this by using an sql database that saves all user, assignment, student, and class data. There are 4 tables in this database: users, classes, students, and gradebook. You can also add students and classes. From any other view you are able to see the student's grades and classes. Also, thanks to bootstrap and W3Schools for their html styling help and courier for their emailing service which allowed me to style emails. But now, allow me to go into more depth of each file in this project.

The app.py makes my website avtive and allows for errors to be given, buttons to be directed, forms to be submitted, and data to be stored. It is the longest file by far totaling to almost 400 lines of code.

Next is my index page which appears differntly based on the user type. A teacher is allowed to see more as they have more tabs and areas to go to. In contrast a student is only allowed to see grades and their classes. I do this by using and if statment in jinja.

I'll summarize a few files briefly. Both the login and registrtaion page is from the finance assignment. However, the registrtaion further changes its fields based on the user type. After submsission, the user is then sent to a verification tab that sends an email to them giving a code. This is so we are able to verify that user is not impersonating someone else and makes my program safer.

My students and classes file are similar in that they both show and allow for more data to be inputted. It is not anything complicated and it took me only a day in total to finish both.

My grading system however was much more complicated. One of the most difficult aspects of this assignment was being able to show and update students in the class that is selected only. I had trouble with jinja and nesting but finally figured it out. Furthermore, once submitted, the grades are immediately calculated and inputted into the students gradebook and class grade. It does this by using the formula, weight * grade/ weight, for each grade for each student.

Lastly, there is the gradebook. On the teacher view, it shows all the students and assignments in that class that is selected. On the student view, it shows all the classes and the student's grades in each classes.

Although this was a fun project, it took 1 and a half weeks which prevented me from coding a statistics tab for the teacher and a setting tab that allowed how dark mode changes. Furthermore, I ran out of time and was prevented from creating code that allowed for updating or changing grades and also deleting students, classes, and grades.