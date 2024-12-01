#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int cmp(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

int count(int* arr, int len, int ref) {
    int cnt = 0;
    for (int i = 0; i < len; i++){
        if (arr[i] == ref) cnt++;
    }
    return cnt;
}

int main() {
    // reading file
    FILE *f = fopen("./inp.txt", "r");
    fseek(f, 0, SEEK_END);
    long fsize = ftell(f);
    fseek(f, 0, SEEK_SET);

    char *str = malloc(fsize+1);
    fread(str, fsize, 1, f);
    fclose(f);

    // here str is "a   b\nc   d\n ..."
    // so we do some parsint into l and r arrays
    
    int *l = malloc(fsize);
    int *r = malloc(fsize);

    char *line, *part;

    int linen = 0;

    while ((line = strsep(&str, "\n"))) {
        if (line[0] == '\0') break;
        for (int i = 0; (part = strsep(&line, "   ")); i++) {
            if (i == 0) {
                l[linen] = atoi(part);
            } else {
                r[linen] = atoi(part);
            }
        }
        linen++;
    }

    free(str);

    qsort(l, linen, sizeof(int), cmp);
    qsort(r, linen, sizeof(int), cmp);

    int res = 0;
    for (int i = 0; i < linen; i++) {
        int cnt = count(r, linen, l[i]);
        res += cnt*l[i];
    }
    printf("result: %d\n", res);

    free(l);
    free(r);
}
