
# \ <section:top>
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file
## @file <djmodule:mony>
import os
import sys
# / <section:top>
# \ <section:mid>
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
# / <section:mid>
# \ <section:bot>
if __name__ == '__main__':
	main()
# / <section:bot>