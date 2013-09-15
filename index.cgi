#! /usr/bin/python
print '''Content-type: text/html\n\n

<h2>The Assembly Scavenger Hunt!</h2>

This page is a simple utility for embedding a message in a simulated shotgun sequencing dataset. First text is converted to DNA through a simple lookup table; then, the resulting contig is used to simulate reads at a desired coverage and depth. The idea is to run an assembly 'scavenger hunt' by hiding clues in a read set and having students follow the clues by assembling the reads <i>de novo</i> with a program such as velvet. Of course, if you want to hide messages in DNA reads for some other nefarious reason -- cue spy music! -- nobody's stopping you.

In regards to teaching assembly, I would recommend using it as a way to demonstrate the effects of error profiles and coverage on assembly results. The quality of the results from tuning assembler parameters is a very straight-forward method of showing students that these programs are good heuristics, and that much care needs to be given to their use in order to produce biologically relevant results.

Some of this code was riffed, frankensteined, and hacked from my adviser, C. Titus Brown, and the concept was borrowed from my fellow TA's at our lab's <a href='http://ged.msu.edu/angus/'>NGS course</a>.

<p>
<hr>

<form method='POST' action='scavenge.cgi'>
Enter some text to sequence:<br>
<textarea name='text' cols='60' rows='5'></textarea><br>
<font size='-1'><i>Separate messages by a blank line.</i>
</font><br>
<p>
<input type='submit' value='go!'>
<p>
Read length: <input type='text' name='readlen' value='10' size='4'><p>
Mutation rate (# of mutations in 1000 bp): <input type='text' name='mut' value='20' size='4'><p>
Coverage: <input type='text' name='cov' value='10' size='4'><p>
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
Note, the source code is available <a href='http://github.com/cswelcher/assembly-scavenger-hunt'>on github</a>.
<p>
<a href='http://ged.msu.edu/'>CS Welcher</a>, welcherc@msu.edu.
'''


