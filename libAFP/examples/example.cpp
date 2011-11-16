/* ------------------------------------------------------------------

  @authors - Rishabh, Santosh, Vikesh
  @date - 24th January, 2011
  @note - Example program

-------------------------------------------------------------------*/
#include<stdio.h>
#include<cstring>
#include<iostream>
#include<fstream>
#include "../include/util.h"
#include "protocol.h"
using namespace std;


#define FLAG_MAX 10
#define FP_MAX 2000
#define FOR(i,n) for(int i=0;i<n;i++)
FILE * ofp = stdout;

AudioData* loadWaveFile(char *file);
AudioData* loadDataUsingLAME(char *file);

int main(int argc, char **argv) {
    AudioData *data = 0;
    bool debug=false,metadata=false, fingerprint=false, append=false, ext_file=false, file_name=false;

    for(int i=1;i<argc;i++)
    {
        if(strlen(argv[i])<2) err_sys("ERROR: BAD ARGUMENTS. Usage: ./example [-d] <clip-name>");

        if(argv[i][0]==DELIM)
        {
            bool found=false;
            if(argv[i][1]=='d') debug=true, found=true;
            if(argv[i][1]=='m') metadata=true, found=true;
            if(argv[i][1]=='p') fingerprint=true, found=true;
            if(argv[i][1]=='a') append=true, found=true;
            if(argv[i][1]=='f') file_name=true, found=true;

            if(argv[i][1]==DELIM)
            {
                    if(argv[i][2]=='f' && argv[i][3]=='i' && argv[i][4]=='l' && argv[i][5]=='e')
                    {
                        ext_file=found=true;
                        char str[100];
                        int j;
                        for( j=7;j<strlen(argv[i]);j++)
                            str[j-7]=argv[i][j];
                        str[j-7] = 0;
                        if(append)
                            ofp = fopen(str,"a");
                        else
                            ofp = fopen(str,"w");

                        if(!ofp)
                            err_sys("Output file not found");
                    }

            }

            if(!found) err_sys("ERROR: BAD ARGUMENTS. Usage: ./example [-d] <clip-name>");
        }
    }

    for (int i = 1; i < argc; ++i) { // Go through each filename passed on the command line

        //Skip if it is a flag
         if(argv[i][0]=='-') continue;

          char *file = argv[i];

	// Get the extension
    	char fext[100] = "";
    	char *p = strrchr(file, '.');
    	if ( p != NULL ) {
    	    strcpy(fext, p+1);

    	    // Lowercase the extension
    	    p = fext;
    	    while ( *p ) {
    		*p = tolower(*p);
    		p++;
    	    }
   	}

	if ( strstr(fext, "wav") ) {
	    // Process a Wave file
	     if(debug) fprintf(ofp,"Wave file format\n");
	     data = loadWaveFile(file);
	} else {
	    // Handle anything else
	    /* Passe' printf("The codec layer only supports wav format as of now\n"); */
        if(debug) fprintf(ofp,"Decoding file %s\n", file);
	    data = loadDataUsingLAME(file);
	}

	if (!data) {
	    fprintf(ofp,"** Failed to load file %s\n",file);
	    continue;
	}

   /* Debug */
    if(debug) fprintf(ofp,"Checking file %s\n", file);

    if(data && debug){
        fprintf(ofp,"File size: %0.2f MB\n",(float)data->getSize()*2/1000000);
        fprintf(ofp,"Sample rate: %d samples/second\n",data->getSRate());
        fprintf(ofp,"Is the audio stereo? %s\n",(data->getStereo()?"Yes":"No"));
        fprintf(ofp,"The number of samples: %d\n",data->getSize());
    }

    // Get the fingerprint
	if (!data->createPrint()){
	    fprintf(ofp,"** Failed to generate print.\n");
	    delete data;
	    continue;
	}

    if(file_name)
        fprintf(ofp,"%s\n",file);


    if(fingerprint){
        string fprint = (data->info).getPrint();
        char str[FP_MAX];

        int i, len=fprint.length();

        for(i=0;i<len;i++)
            str[i] = fprint[i];
        str[i]=0;
        //cout<<str;
        fprintf(ofp,"%s\n\n",str);
    }


	// Get the metadata.
    TrackInformation *info = data->getMetadata("a7f6063296c0f1c9b75c7f511861b89b", "Example 0.9.3", true);
	if (!info) {
	    printf("** Failed to get metadata.\n");
	} else if(metadata) {
	    // Print results.
	    fprintf(ofp,"%s\n", info->getTrack().c_str());
	    fprintf(ofp,"%s\n", info->getArtist().c_str());
	    fprintf(ofp,"%s\n", info->getPUID().c_str());
	}

	delete data;


    }

    #ifdef WIN32
           system("Pause");
    #endif

    if(ext_file)
        close((int)ofp);

    return 0;
}

