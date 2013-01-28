#!/usr/bin/python
import ast
import sys
import urllib
import optparse
import datetime
import re

SEARCH_PATTERN = '\[([^\]]+)\] Retrying testcase ([^ ]+)'
PRINT_PATTERN = '%s.%s'

verbose = False
search_pattern = re.compile(SEARCH_PATTERN)

def parse(url, tree=None):
  if url[-1] != "/":
    url += "/"
  url = "%sapi/python" % url
  if tree:
    url += "?tree=%s" % tree
  return ast.literal_eval(urllib.urlopen(url).read())

def get_matched_lines(url):
  lines = urllib.urlopen(url).readlines()
  groups_from_lines = map(lambda line: search_pattern.findall(line), lines)
  matched_lines = filter(lambda line: bool(line), groups_from_lines)
  return map(lambda line: line[0], matched_lines)

def get_date(timestamp):
   return datetime.datetime.fromtimestamp(int(timestamp)/1000)

def find_committers(url):
  job = parse(url, "builds[result,number,timestamp],displayName")
  builds = job['builds']

  for build in builds:
    build_number = build['number']
    console_url = "%s%d/consoleText" % (url, build_number)
    print '#%d - %s - %s - %s' % (build_number, job['displayName'], get_date(build['timestamp']), build['result'])
    print_if_verbose(console_url)
    matched_lines = get_matched_lines(console_url)
    for matched_line in matched_lines:
      print '%s.%s' % matched_line
    print



def print_if_verbose(message):
  if verbose:
    print message

def main():
  global verbose
  parser = optparse.OptionParser(usage="""Usage: %prog VIEW_URL [options]

Gets yellow committers for all jobs in the supplied Jenkins view.""")
  parser.add_option("-v", "--verbose", action="store_true", default=False,
    help="Prints progress, instead of only the revision")
  parser.add_option("-d", "--debug", action="store_true", default=False,
    help="Prints stack traces")
  try:
    (options, (url,)) = parser.parse_args()
    verbose = options.verbose
    find_committers(url)
  except ValueError, e:
    if options.debug:
      raise e, None, sys.exc_info()[2]
    parser.print_help()
    return 1

if __name__ == '__main__':
  sys.exit(main())
