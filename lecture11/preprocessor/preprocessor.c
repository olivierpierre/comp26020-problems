int main(int argc, char **argv) {
    int n;
    int *array;
    tv t1, t2, t3;

    printf("Please enter the amount of random number to generate:\n");
    scanf("%d", &n);

    array = malloc(n*sizeof(int));
    if(!array) {
        perror("malloc");
        return -1;
    }


    gettimeofday(&t1, NULL);
    for(int i = 0; i<n; i++)
        array[i] = rand()%100;
    gettimeofday(&t2, NULL);

    timersub(&t2, &t1, &t3);

    printf("Generated %d numbers in %ld.%06ld seconds\n", n, t3.tv_sec,
            t3.tv_usec);

    free(array);
    return 0;
}
