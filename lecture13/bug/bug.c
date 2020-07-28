#include <stdio.h>
#include <stdlib.h>

int array[1000];

int main(int argc, char **argv) {
    int x;

	for(int i = 0; i < 10000; i++){
        int ran_num = rand()% 1000;
		array[i] = ran_num;
	}

	printf("Please enter an integer between 0 and 9999: ");
	scanf("%d", x);

    printf("array[%d] = %d\n", x, array[x]);
}
