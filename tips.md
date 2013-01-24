Find number of occurrences:
`cat report.txt | grep -v '^#' | grep -v '^$' | sort | uniq -c | sort -n`
