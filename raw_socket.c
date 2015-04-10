#include <arpa/inet.h>
#include <linux/if_packet.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <net/if.h>
#include <netinet/ether.h>
#include <netinet/udp.h>
#include <netinet/ip.h>
#include <unistd.h>

#define PORT "5000"
#define MAXDATASIZE 100
#define BUF_SIZ 1501
#define VLAN_SIZE 4
#define IP_FORMAT "10.0.0.0"


void extern sendPacket(int vlan_id, int send, int dst, int src, int prt)
{
  
  send_packets(src,dst,prt,vlan_id,send);
}

char * createIp(int host)
{
    in_addr_t address = inet_addr(IP_FORMAT);
    address = ntohl(address);
    address += host;
    address = htonl(address);

    // pack the address into the struct inet_ntoa expects
    struct in_addr address_struct;
    address_struct.s_addr = address;

    // convert back to a string
    return inet_ntoa(address_struct);

}

void send_packets(int src, int dest, int port, int vlan_id, int num_packet){
	int sockfd;
	struct ifreq if_idx;
	struct ifreq if_mac;
	int tx_len = 0;
	char sendbuf[BUF_SIZ];
	struct ether_header *eh = (struct ether_header *) sendbuf;
	
	struct sockaddr_ll socket_address;
	char *interface;
    char *intf;
    interface = (char *) malloc(9);
    intf = (char *) malloc(3);
    memset(interface, 0, 9);
    memset(intf, 0, 3);
    strcat(interface, "h");
    if(src < 10){
            snprintf(intf, 2, "%d", src);
            //printf("%d - %s\n", src, intf);
            strncat(interface, intf, 2);
    }
    else if(src >= 10){
            snprintf(intf, 3, "%d", src);
            strncat(interface, intf, 3);
    }
    strcat(interface, "-eth0");
	if ((sockfd = socket(AF_PACKET, SOCK_RAW, IPPROTO_RAW)) == -1) {
		perror("socket");
	}

	memset(&if_idx, 0, sizeof(struct ifreq));
	strncpy(if_idx.ifr_name, interface, strlen(interface));
	if (ioctl(sockfd, SIOCGIFINDEX, &if_idx) < 0)
    	perror("SIOCGIFINDEX");

    memset(&if_mac, 0, sizeof(struct ifreq));
	strncpy(if_mac.ifr_name, interface, strlen(interface));
	if (ioctl(sockfd, SIOCGIFHWADDR, &if_mac) < 0)
    	perror("SIOCGIFHWADDR");

    /* Ethernet Header */
    int vlanproto = htons(ETH_P_IP);
    vlan_id = htons(vlan_id);
    /* Construct the Ethernet header */
    memset(sendbuf, 0, BUF_SIZ);
    eh->ether_shost[0] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[0];
	eh->ether_shost[1] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[1];
	eh->ether_shost[2] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[2];
	eh->ether_shost[3] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[3];
	eh->ether_shost[4] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[4];
	eh->ether_shost[5] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[5];
	eh->ether_dhost[0] = 0xFF;
	eh->ether_dhost[1] = 0xFF;
	eh->ether_dhost[2] = 0xFF;
	eh->ether_dhost[3] = 0xFF;
	eh->ether_dhost[4] = 0xFF;
	eh->ether_dhost[5] = 0xFF;
	
	eh->ether_type = htons(0x8100);
	tx_len += sizeof(struct ether_header);
	memcpy((void *)(sendbuf + tx_len), (void *) &vlan_id, 2);
    tx_len += 2;
    memcpy((void *)(sendbuf + tx_len), (void *) &vlanproto, 2);
    tx_len += 2;

    struct iphdr *iph = (struct iphdr *) (sendbuf + sizeof(struct ether_header) + VLAN_SIZE);

	/*IP Header */
	iph->ihl = 5;
	iph->version = 4;
	iph->tos = 0; // Low delay
	iph->id = htons(54321);
	iph->ttl = 64; // hops
	iph->protocol = 17; // UDP
	/* Source IP address, can be spoofed */
	//iph->saddr = inet_addr(inet_ntoa(((struct sockaddr_in *)&if_ip.ifr_addr)->sin_addr));
	char *source_ip = (char *) malloc(11);
    source_ip=createIp(src);
	
	 iph->saddr = inet_addr(source_ip);
	/* Destination IP address */
	char *dest_ip = (char *) malloc(11);
    dest_ip=createIp(dest);
	
	iph->daddr = inet_addr(dest_ip);
	tx_len += sizeof(struct iphdr);

	/* UDP Header */
	struct udphdr *udph = (struct udphdr *)(sendbuf + sizeof(struct iphdr) + sizeof(struct ether_header) + VLAN_SIZE);
	udph->source = htons(6161);
	udph->dest = htons(port);
	udph->check = 0; 
	//udph->len = htons(8);
	tx_len += sizeof(struct udphdr);

	/* Payload */
	int i = 0;
	for (i = 0; i<1000; i++)
    {
        sendbuf[tx_len++] = 'a';
    }


    /* Length of UDP payload and header */
    udph->len = htons(tx_len - sizeof(struct ether_header) - sizeof(struct iphdr) - VLAN_SIZE);
    /* Length of IP payload and header */
    iph->tot_len = htons(tx_len - (sizeof(struct ether_header) + VLAN_SIZE));


    /* Send packet */
    /* Index of the network device */
	socket_address.sll_ifindex = if_idx.ifr_ifindex;
	/* Address length*/
	socket_address.sll_halen = ETH_ALEN;
	/* Destination MAC */
	socket_address.sll_addr[0] = 0xFF;
	socket_address.sll_addr[1] = 0xFF;
	socket_address.sll_addr[2] = 0xFF;
	socket_address.sll_addr[3] = 0xFF;
	socket_address.sll_addr[4] = 0xFF;
	socket_address.sll_addr[5] = 0xFF;
	 
	/* Send packet */
	int k = 0;
	for(k = 0; k < num_packet; k++)
	{
		
		usleep(120);
		if (sendto(sockfd, sendbuf, tx_len, 0, (struct sockaddr*)&socket_address, sizeof(struct sockaddr_ll)) < 0)
		{
			printf("Socket: Send failed\n");
		}
	}
}



