#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <errno.h>

#define MYPORT "3490"  // the port users will be connecting to

int main(void)
{
  struct addrinfo hints, *res;
  int sockfd;

  // first, load up address structs with getaddrinfo():
  memset(&hints, 0, sizeof hints);
  hints.ai_family = AF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;

  getaddrinfo("127.0.0.1", MYPORT, &hints, &res);

  // make a socket:
  sockfd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
  printf("2-sfd: %d\n", sockfd);

  // connect!
  int c = connect(sockfd, res->ai_addr, res->ai_addrlen);
  printf("2-con: %d\n", c);
  if(c == -1) {printf("errno: %d\n", errno);}

  const int size = 15;
  char buf[16] = {0};
  int r = recv(sockfd, buf, size, 0);
  buf[size] = '\0';

  printf("2-rec: %d\n", r);
  if(r == -1) {printf("errno: %d\n", errno);}
  printf("%s", buf);

  close(sockfd);

  return 0;
}
