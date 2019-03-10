#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>

#define MYPORT "3490"  // the port users will be connecting to
#define BACKLOG 10     // how many pending connections queue will hold

int main(void)
{
  struct sockaddr_storage their_addr;
  socklen_t addr_size;
  struct addrinfo hints, *res;
  int sockfd, new_fd;

  // !! don't forget your error checking for these calls !!

  // first, load up address structs with getaddrinfo():

  memset(&hints, 0, sizeof hints);
  hints.ai_family = AF_UNSPEC;  // use IPv4 or IPv6, whichever
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_flags = AI_PASSIVE;     // fill in my IP for me

  getaddrinfo(NULL, MYPORT, &hints, &res);

  // make a socket, bind it, and listen on it:

  sockfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
  printf("1-sfd: %d\n", sockfd);
  bind(sockfd, res->ai_addr, res->ai_addrlen);
  listen(sockfd, BACKLOG);

  // now accept an incoming connection:

  addr_size = sizeof their_addr;
  new_fd = accept(sockfd, (struct sockaddr *)&their_addr, &addr_size);
  printf("1-nfd: %d\n", new_fd);

  // ready to communicate on socket descriptor new_fd!
  char *msg = "Beej was here!\n";
  int len, bytes_sent;

  len = strlen(msg);
  bytes_sent = send(new_fd, msg, len, 0);
  printf("1-sen: %d\n", bytes_sent);

  close(new_fd);
  close(sockfd);

  return 0;
}
