#include <stdio.h>

char password[128];

void generate_password() {
	FILE *file = fopen("/dev/urandom","r");
	fgets(password, 128, file);
	fclose(file);
}

void main() {
	puts("Welcome to my ultra secure login service!");
	long n_trys=0;
	// no way they can guess my password if it's random!
	while(1){
		generate_password();

		for(int loop = 0; loop < 128; loop++)
	      printf("%d, ", password[loop]);

		char input[128]={0};
		// printf("Enter the password: ");
		// fgets(input, 128, stdin);

		if (strcmp(input, password) == 0) {
			char flag[128];

			FILE *file = fopen("flag.txt","r");
			if (!file) {
			    puts("Error: missing flag.txt.");
					printf("Trys: %d", n_trys);
			    exit(1);
			}

			fgets(flag, 128, file);
			puts(flag);
		} else {
			puts("Wrong!");
		}
		n_trys++;
	}
}
