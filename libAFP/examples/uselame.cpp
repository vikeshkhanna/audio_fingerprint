/* --------------------------------------------------
@authors- Vikesh Khanna, Rishabh Sood, Santosh Kumar
@date: 3rd March 2011
@note: Lame for mp3
-------------------------------------------------------*/

#include <stdio.h>
#include "protocol.h"
#ifdef WIN32
#include "windows.h"
#else
#include <sys/wait.h>
#endif
#include<stdio.h>

AudioData *loadWaveFile(char *file);

//	loadDataUsingLAME
//
//	Opens an audio file and converts it to a temp .wav file
//	Calls loadWaveFile to load the data
//
AudioData* loadDataUsingLAME(char *file) {
    char *temp = "clips/fpTemp.wav";
    //printf("lame test\n");
#ifdef WIN32
    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    char * cmd = new char[1024];
    sprintf(cmd,"lame --decode \"%s\" fpTemp.wav", file);
    if (!CreateProcess(NULL, // No module name (use command line).
		cmd,     // Command line.
		NULL,             // Process handle not inheritable.
		NULL,             // Thread handle not inheritable.
		FALSE,            // Set handle inheritance to FALSE.
		DETACHED_PROCESS, // Creation flags.
		NULL,             // Use parent's environment block.
		NULL,             // Use parent's starting directory.
		&si,              // Pointer to STARTUPINFO structure.
		&pi )             // Pointer to PROCESS_INFORMATION structure.
       )
    {
	return 0;
    }
    delete[] cmd;

    DWORD result = WaitForSingleObject(pi.hProcess, 1000000 /*INFINITE*/);
#else
    pid_t pid = fork();
    char * flag = "--decode";
    char * cmd = "/usr/bin/lame"; // lame path
    char * argv[5] = {cmd, flag, file, temp,(char*)0};
    //char * argv[3] = {cmd, flag, file};

    if (pid==0 && execv(cmd, (char **) argv) == -1) {
        printf("Exec error");
        //char * argv[2]={"/bin/ls",(char*)0}; if(execv("/bin/ls",(char**) argv)==-1) printf("ls error"); else printf("ls succeeded\n");
        return 0;
    }
    int exitCode = -1;
    pid = waitpid(pid, &exitCode, 0); // NYI: Implement timeout
    if (exitCode != 0) {
	return 0;
    }
#endif
    AudioData *data = loadWaveFile(temp);
    //unlink(temp);
    return data;
}

