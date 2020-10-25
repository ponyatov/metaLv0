// powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
// \ <section:top>
#include <NMEA.h>
// / <section:top>
// \ <section:bot>
int main(int argc, char *argv[]) {
    
// open file
  assert(argc == 2);
  for (int i = 0; i < argc; i++)
    printf("\nargv[%i] = <%s>", i, argv[i]);
  FILE *fh = fopen(argv[1], "r"); assert(fh);

// scan loop
  unsigned char *line_buf = NULL;
  ssize_t line_size = 0;
  size_t line_buf_size = 0;
  #define LSZ (line_size = getline(&line_buf, &line_buf_size, fh))
  for (LSZ; line_size >= 0; LSZ) {
    // printf("\nline size:%i", line_size);
    parse(&line_buf[0],&line_buf[line_size]);
    // printf("\n");
  }

// close session
  fclose(fh);
  free(line_buf);

    return 0;
}
// / <section:bot>
