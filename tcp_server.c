/* A simple server in the internet domain using TCP
 * Answer the questions below in your writeup
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[])
{
    /* 1. What is argc and *argv[]?
     *The argc parameter is the number of command line arguments.
     *The *argv[] parameter is an array of pointers that each point to a cstring. 
     These cstrings are the arguments that are passed to the program via command line.
     */
    int sockfd, newsockfd, portno;
    /* 2. What is a UNIX file descriptor and file descriptor table?
     * A file descriptor is a number that will uniquely identify an open
     file within the operating system. The file descriptor table is basically a table which
     orders the file descriptors into a table, where the elements are pointers to those
     open files.
     */
    socklen_t clilen;

    struct sockaddr_in serv_addr, cli_addr;
    /* 3. What is a struct? What's the structure of sockaddr_in?
     * A struct is a user-defined data type in C. Basically, the idea is that we get to now
     use one variable name that houses member data types. I looked into sockaddr_in on 
     stackoverflow, and its structure is defined in netinet/in.h. Basically, it houses
     data members that help specify a transport address and port for the AF_INET address
     family The line of code here will basically create two structs of type sockaddr_in 
     called serv_addr and cli_addr. 
     */
    
    int n;
    if (argc < 2) {
        fprintf(stderr,"ERROR, no port provided\n");
        exit(1);
    }
    
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    /* 4. What are the input parameters and return value of socket()
     * The return value of socket() is an int. The socket() function takes
     arguments that specify domain, type and protocol. Domain specifies the address family
     to be used in communication. Type specifies the socket type. Protocol specifies a
     specific protocol to be used with the socket.
     */
    
    if (sockfd < 0) 
       error("ERROR opening socket");
    bzero((char *) &serv_addr, sizeof(serv_addr));
    portno = atoi(argv[1]);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = htons(portno);
    
    if (bind(sockfd, (struct sockaddr *) &serv_addr,
             sizeof(serv_addr)) < 0) 
             error("ERROR on binding");
    /* 5. What are the input parameters of bind() and listen()?
     * bind() parameters include a socket name, a pointer to that socket,
     and the size of its memory address in bytes. listen() takes two integers. One
     helps identify a socket and the other is used for backlog on servers that have multiple
     connection requests at a time. 
     */
    
    listen(sockfd,5);
    clilen = sizeof(cli_addr);
    
    while(1) {
        /* 6.  Why use while(1)? Based on the code below, what problems might occur if there are multiple simultaneous connections to handle?
        * The while(1) is an infinite while loop that continuously iterates. The problem is that
        each iteration can only handle one connection. If multiple connections occur, they will
        interfere with each other because the loop commands cannot be given to multiple 
        processes.
        */
        
	char buffer[256];
        newsockfd = accept(sockfd, 
                    (struct sockaddr *) &cli_addr, 
                    &clilen);
	/* 7. Research how the command fork() works. How can it be applied here to better handle
	multiple connections?
         * Fork() allows for multiple processes to execute instructions after being called.
         this would help handle multiple connections because each process would be able to
         separately connect and execute instructions without interfering with each other.*/  
        
	if (newsockfd < 0) 
             error("ERROR on accept");
	bzero(buffer,256);
        
	n = read(newsockfd,buffer,255);
        if (n < 0) 
            error("ERROR reading from socket");
        printf("Here is the message: %s\n",buffer);
        n = write(newsockfd,"I got your message",18);
        if (n < 0) 
            error("ERROR writing to socket");
        close(newsockfd);
    }
    close(sockfd);
    return 0; 
}
  
/* This program makes several system calls such as 'bind', and 'listen.' What exactly is a system call?
 * System calls allow the code to basically ask the operating system of the hardware that the
 code is running on to perform certain actions. 
 */
