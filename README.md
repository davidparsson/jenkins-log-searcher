## Project is deprecated
Use **[jenkins-log-grep](https://github.com/davidparsson/jenkins-log-grep)** instead.


## Overview
Searches for regex patterns in all logs for a Jenkins job and prints the matches in a formatted output.

Usage:

<pre>
./search-logs.py http://url/to/job
</pre>

Sample output:

<pre>
#84 - my-jenkins-job - 2013-01-28 10:44:52 - UNSTABLE
MyTestClass.aTestName
MyTestClass.aTestName
MyTestClass.anotherTestName

#83 - my-jenkins-job - 2013-01-28 10:08:14 - SUCCESS
MyTestClass.aTestName
</pre>
