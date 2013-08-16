#! /usr/bin/python
print '''Content-type: text/html\n\n

<h2>The shotgunator!</h2>

This is a simple script that "shotgun sequences" paragraphs of text,
by producing "reads" of a configurable length, mutation rate, and
coverage.  I use it to demonstrate shotgun sequencing and de novo
assembly to students.  <p> <p align='right'>--titus</font></p>

<p>
<hr>

<form method='POST' action='shotgun.cgi'>
Enter some text to sequence (leave blank for Tale of Two Cities):<br>
<textarea name='text' cols='60' rows='5'></textarea><br>
<font size='-1'><i>Separate paragraphs by a blank line.</i>
</font><br>
<p>
<input type='submit' value='go!'>
<p>
Read length: <input type='text' name='readlen' value='10' size='4'><p>
Mutation rate (# of mutations in 1000 bp): <input type='text' name='mut' value='20' size='4'><p>
Coverage: <input type='text' name='cov' value='10' size='4'><p>
Sort results? <select name='sorted'>
  <option value='yes'> Yes
  <option value='no'> No
</select>
<p>
Paired ends?
<select name='paired'>
  <option value='yes'> Yes
  <option value='no'> No
</select>
If yes, insert size? <input type='text' name='insert' value='25' size='4'>
</select>
<p>
</form>

<hr>
Note, the source code is available <a href='http://github.com/ged-lab/assembly-exercise'>on github</a>.
<p>
<a href='http://ged.msu.edu/'>C. Titus Brown</a>, ctb@msu.edu.
'''


