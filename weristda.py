#!/usr/bin/python2

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import datetime

LIST_LENGTH = 14
NAME_LIST=["mama", "baba", "lea", "felix"]
MEMORY_NAME = "anwesenheit"
ENTRYS = []

def wochentag(x):
    return {
        0: "Montag",
        1: "Dienstag",
        2: "Mittwoch",
        3: "Donnerstag",
        4: "Freitag",
        5: "Samstag",
        6: "Sonntag"
    }[x]

def load():
    global ENTRYS
    with open(MEMORY_NAME, 'r') as f:
        ENTRYS = f.readlines()
        f.close()
    for i in range(len(ENTRYS)):
        ENTRYS[i] = ENTRYS[i].strip()

def add(input):
    global ENTRYS
    if input not in ENTRYS:
        ENTRYS.append(input)

def remove(input):
    global ENTRYS
    if input in ENTRYS:
        ENTRYS.remove(input)

def save():
    with open(MEMORY_NAME, 'w') as f:
        for entry in ENTRYS: 
            f.write(entry + "\n")
        f.close()


load()
form = cgi.FieldStorage()
print "Content-type: text/html"
print

print """
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">

    <link rel="stylesheet" href="style.css">
    <link rel="icon" href="favicon.png" type="image/x-icon">
    <title>Wer ist da? - Felix Pankratz</title>
  </head>
<body>  
    <center>
        <div class="headline">
            <h1>Felix Pankratz</h1>
        </div>
        <nav class="navbar navbar-expand-sm navbar-inverse">

          <!-- Links -->
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="https://felixpankratz.de">Home</a>
            </li>
            <li class="nav-item active">
              <a class="nav-link" href="https://felixpankratz.de/projects.html">Projects</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://felixpankratz.de/chat/">Chat</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://felixpankratz.de/ez/index.php">Monitoring</a>
            </li>
            <li class="nav-item" >
              <a class="nav-link" href="https://felixpankratz.de/disclaimer.html">Disclaimer</a>
            </li>
          </ul>
        </nav>
"""

table = """
        <form action = \"weristda.py\" method = \"POST\" target = \"_self\">
            <table class=\"whosthere\">"
                <tr>
                    <th>Wochentag</th>
                    <th>Mama</th> 
                    <th>Baba</th> 
                    <th>Lea</th> 
                    <th>Felix</th>
                </tr>
"""

today = datetime.date.today()
days_from_monday = today.weekday()
monday = today - datetime.timedelta(days=days_from_monday)

for i in range(LIST_LENGTH):
    day = monday + datetime.timedelta(days=i)
    dayshort = day.strftime("%Y%m%d")
    datestr = wochentag(day.weekday()) + ', '
    datestr += day.strftime("%d.%m.%Y")
    table += """
                    <tr>
                        <th>%s</th>
    """ % (datestr)

    for name in NAME_LIST:
        combo = name + dayshort
        checkBox = "<th><input type=\"checkbox\" class=\"myCheckbox\" id=\"%s\" name=\"%s\"" % (combo, combo)
        if(len(form)>0):
            if form.getvalue(combo):
                add(combo)
                checkBox += " checked"
            else:
                remove(combo)
        else:
            if combo in ENTRYS:
                add(combo)
                checkBox += " checked"      
        checkBox += " /></th>"
        table += checkBox 
    table += """
                    </tr>
    """
table += """
                <input type = "submit" value = "Speichern" />
            </form>
        """

print table

print """

    </center>
 
   <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/js/bootstrap.min.js" integrity="sha384-h0AbiXch4ZDo7tp9hKZ4TsHbi047NrKGLO3SEJAg45jXxnGIfYzk4Si90RDIqNm1" crossorigin="anonymous"></script>
  </body>
  <footer>
        <div class="footer">
            <p> (c) 2018 Felix Pankratz | <a href="mailto:mail@felixpankratz.de">Contact</a> </p>
        </div>
  </footer>
</html>
"""
save()