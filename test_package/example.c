#include <ogg/ogg.h>
#include <stdio.h>
#include <stdlib.h>

int main() {
    ogg_sync_state og;
    int result = ogg_sync_init(&og);
    printf("OGG sync init result: %d\n", result);
    ogg_sync_clear(&og);
    return EXIT_SUCCESS;
}
