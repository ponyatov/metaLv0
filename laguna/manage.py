#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
import os
import sys
import config
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
