#include<stdlib.h>
#include<stdio.h>
#include<string.h>

// gcc -O3 sam-to-coverage.c -o sam-to-coverage

#define NameLength 256


int compare(const void*a,const void*b){
	char*aa=(char*)a;
	char*bb=(char*)b;
	return strcmp(aa,bb);
}

/*
 * like bsearch, but returns an index instead of a pointer.
 */
int bSearch(char*newName,char*names,int count,int size,int ( * comparator ) ( const void *, const void * )){
	int left=0;
	int right=count;
	while(left<=right){
		int middle=(left+right)/2;
		char*value=names+middle*size;
		int comparison=strcmp(value,newName);

		if(comparison>0){
			right=middle-1;
		}else if(comparison<0){
			left=middle+1;
		}else{
			return middle;
		}
	}
	return -1;
}

void insert(char*names,int*count,char*newName){
	int i;
	
	if(bSearch(newName,names,*count,NameLength,compare)!=-1){
		return;
	}
	char*destination=names+((*count)*NameLength);
	strcpy(destination,newName);
	(*count)++;
	qsort(names,*count,NameLength,compare);

	return;
}

void printNames(char*names,int count,int*lengths){
	printf("%i\n",count);
	int i;
	for(i=0;i<count;i++){
		printf("%s\t%i\n",names+i*NameLength,lengths[i]);
	}
}



void readChromosomeNames(char*samFile,char*names,int*count){
	FILE*f=fopen(samFile,"r");
	char buffer[4096];
	while(fgets(buffer,4096,f)){
		if(buffer[0]=='@')
			continue;
		char chromosomeName[NameLength];
		int i=0;
		int numberOfTabulations=0;
		int j=0;
		while(1){
			char currentCharacter=buffer[i];
			if(currentCharacter=='\0'){
				break;
			}
			if(currentCharacter=='\t'){
				numberOfTabulations++;
				if(numberOfTabulations==3){
					chromosomeName[j]='\0';
				}
			}else if(numberOfTabulations==2){
				chromosomeName[j]=currentCharacter;
				j++;
			}
			
			i++;
		}
		if(strcmp(chromosomeName,"*")!=0){
			insert(names,count,chromosomeName);
		}
	}
	fclose(f);
}

void getMaximumPositions(char*samFile,char*names,int count,int*lengths){
	FILE*f=fopen(samFile,"r");
	char buffer[4096];
	while(fgets(buffer,4096,f)){
		if(buffer[0]!='@'){
			continue;
		}
		// @SQ     SN:psu|Lmjchr1  LN:268984
		char chromosomeName[NameLength];
		char theVeryLength[100];
		int i=0;
		int numberOfTabulations=0;
		int j=0;
		int k=0;
		while(1){
			char currentCharacter=buffer[i];
			if(currentCharacter=='\0'){
				break;
			}
			if(currentCharacter=='\t'){
				numberOfTabulations++;
				if(numberOfTabulations==2){
					chromosomeName[j]='\0';
				}
			}else if(numberOfTabulations==1){
				chromosomeName[j++]=currentCharacter;
			}else if(numberOfTabulations==2){
				theVeryLength[k++]=currentCharacter;
			}else if(currentCharacter=='\n'){
				theVeryLength[k]='\0';
			}
			
			i++;
		}
		char*realName=chromosomeName+3;
		char*realLength=theVeryLength+3;

		
		int index=bSearch(realName,names,count,NameLength,compare);
		int p=atoi(realLength);
		//printf("%s %i\n",realName,p);
		if(p>lengths[index]){
			lengths[index]=p;
		}
	}
	fclose(f);
}

void readCoverage(char*samFile,char*names,int count,int*lengths,int**coverages){
	FILE*f=fopen(samFile,"r");
	char buffer[4096];
	while(fgets(buffer,4096,f)){
		if(buffer[0]=='@')
			continue;
		char chromosomeName[NameLength];
		char position[100];
		char read[512];
		int l=0;
		int i=0;
		int numberOfTabulations=0;
		int j=0;
		int k=0;
		while(1){
			char currentCharacter=buffer[i];
			if(currentCharacter=='\0'){
				break;
			}
			if(currentCharacter=='\t'){
				numberOfTabulations++;
				if(numberOfTabulations==3){
					chromosomeName[j]='\0';
				}
				if(numberOfTabulations==4){
					position[k]='\0';
				}
				if(numberOfTabulations==10){
					read[l]='\0';
				}
			}else if(numberOfTabulations==2){
				chromosomeName[j++]=currentCharacter;
			}else if(numberOfTabulations==3){
				position[k++]=currentCharacter;
			}else if(numberOfTabulations==9){
				read[l++]=currentCharacter;
			}
			
			i++;
		}
		
		int index=bSearch(chromosomeName,names,count,NameLength,compare);
		if(index==-1){ // not mapped
			continue;
		}
		int p=atoi(position); 
		p--;// 0-based

		int width=strlen(read);
		int g;
		for(g=0;g<width;g++){
			int superPosition=p+g;
			if(superPosition<lengths[index]){
				coverages[index][superPosition]++;
			}
		}
	}
	fclose(f);


}

void printCoverage(char*names,int count,int*lengths,int**coverages){
	int i;
	for(i=0;i<count;i++){
		int j;
		for(j=0;j<lengths[i];j++){
			char*chromosomeName=names+i*NameLength;
			int positionOnTheGenome=j+1;
			int coverage=coverages[i][j];
			printf("%s\t%i\t%i\n",chromosomeName,positionOnTheGenome,coverage);
		}
	}
}

int main(int argc,char**argv){
	if(argc==1){
		printf("Provide a sam file.\n");
		return 0;
	}
	char*samFile=argv[1];
//GA6_00013:1:1:1070:945#0        16      psu|Lmjchr34    230956  37      76M     *       0       0       CGGAGTCTGTGTTGGGCCAGGTAGAGTGGAGAATGACTCCTCTTCTACAGCGGAGAATGGACACNTCGAAAAGAGN    @<<::3@3@@@:::::::<<<@1@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@3-0,0/,2#,2**/.'+(*#    XT:A:U  NM:i:2  X0:i:1  X1:i:0  XM:i:2  XO:i:0  XG:i:0  MD:Z:64A10A0

	char names[12000000];
	int count=0;

	readChromosomeNames(samFile,names,&count);
	

	int*lengths=(int*)malloc(count*sizeof(int));
	int i;
	for(i=0;i<count;i++){
		lengths[i]=0;
	}
	getMaximumPositions(samFile,names,count,lengths);

	//printNames(names,count,lengths);
	int**coverages=(int**)malloc(sizeof(int*)*count);
	for(i=0;i<count;i++){
		coverages[i]=(int*)malloc(sizeof(int)*lengths[i]);
		int p;
		int total=lengths[i];
		for(p=0;p<total;p++){
			coverages[i][p]=0;
		}
	}
	
	
	readCoverage(samFile,names,count,lengths,coverages);

	printCoverage(names,count,lengths,coverages);

	return 0;
}


