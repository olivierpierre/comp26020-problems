#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/* Fill the array referenced by ptr with random integers with values between
 * 0 and 99 */
void fill_array(int *ptr, int size) {
    srand(time(NULL));
    for(int i = 0; i<size; i++)
        ptr[i] = rand()%100;
}

int main(int argc, char **argv) {
    int bins[5] = {0, 0, 0, 0, 0};

    int *array = malloc(1000 * sizeof(int));
    if(!array) {
        perror("malloc");
        return -1;
    }

    fill_array(array, 1000);

    /* Iterate over the array and accordign to the value of each element,
     * increment the corresponding bin counter */
    for(int i=0; i<1000; i++) {
        int n = array[i];

        if(n < 100/5)
            bins[0]++;
        else if(n >= 100/5 && n < (100/5)*2)
            bins[1]++;
        else if(n >= (100/5)*2 && n < (100/5)*3)
            bins[2]++;
        else if(n >= (100/5)*3 && n < (100/5)*4)
            bins[3]++;
        else
            bins[4]++;
    }

    for(int i=0; i<5; i++) {
        printf("bin %d: [%03d - %03d[ ", i, (100/5)*i, (100/5)*(i+1));
        for(int j=0; j<(bins[i]*100)/1000; j++)
            printf("*");
        printf("\n");
    }

    free(array);
    return 0;
}
