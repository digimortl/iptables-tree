### Convert iptables-save format to pstree-like view

iptables-tree is used to convert the output of iptables-save into an easily readable 
rules tree to STDOUT. Use I/O-redirection provided by your shell to write to a file.

#### Example:
```
$ iptables-save -t filter | ./iptables-tree
*filter
:INPUT ACCEPT [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT
   ├─-j MY_IN
   │    ├─-i bond2.478 -j MY_IN_521a2e1b
   │    │                 ├─-i bond2.478 -j MY_IN_521a2e1b_fbd7c0f4
   │    │                 │                 ├─-i bond2.478 -p tcp -m tcp --dport 14700:15800 -j MY_IN_521a2e1b_fbd7c0f4_F
   │    │                 │                 │                                                   └─-i bond2.478 -j MY_IN_521a2e1b_F
   │    │                 │                 │                                                                     └─-i bond2.478 -j ACCEPT
   │    │                 │                 ├─-i bond2.478 -p tcp -m tcp --dport 4200:5060 -j MY_IN_521a2e1b_fbd7c0f4_F
   │    │                 │                 │                                                 └─-i bond2.478 -j MY_IN_521a2e1b_F
   │    │                 │                 │                                                                   └─-i bond2.478 -j ACCEPT
   │    │                 │                 └─-i bond2.478 -p udp -m udp --dport 5496 -j MY_IN_521a2e1b_fbd7c0f4_F
   │    │                 │                                                              └─-i bond2.478 -j MY_IN_521a2e1b_F
   │    │                 │                                                                                └─-i bond2.478 -j ACCEPT
   │    │                 └─-i bond2.478 -j MY_IN_521a2e1b_1373d0cb
   │    │                                   └─-i bond2.478 -p tcp -m tcp --dport 38200:57428 -j MY_IN_521a2e1b_1373d0cb_F
   │    │                                                                                       └─-i bond2.478 -j MY_IN_521a2e1b_F
   │    │                                                                                                         └─-i bond2.478 -j ACCEPT
   │    └─-i bond2.362 -j MY_IN_733d7567a
   │                      ├─-i bond2.362 -j MY_IN_733d7567a_1787d764
   │                      │                 └─-i bond2.362 -p tcp -m tcp --dport 22 -j MY_IN_733d7567a_1787d764_F
   │                      │                                                            └─-i bond2.362 -j MY_IN_733d7567a_F
   │                      │                                                                              └─-i bond2.362 -j ACCEPT
   │                      ├─-i bond2.362 -j MY_IN_733d7567a_d10af457
   │                      │                 ├─-i bond2.362 -p tcp -m tcp --dport 53 -j MY_IN_733d7567a_d10af457_F
   │                      │                 │                                          └─-i bond2.362 -j MY_IN_733d7567a_F
   │                      │                 │                                                            └─-i bond2.362 -j ACCEPT
   │                      │                 └─-i bond2.362 -p udp -m udp --dport 53 -j MY_IN_733d7567a_d10af457_F
   │                      │                                                            └─-i bond2.362 -j MY_IN_733d7567a_F
   │                      │                                                                              └─-i bond2.362 -j ACCEPT
   │                      ├─-i bond2.362 -j MY_IN_733d7567a_58af8740
   │                      │                 └─-d 224.0.0.251/32 -i bond2.362 -p udp -m udp --dport 4267 -j MY_IN_733d7567a_58af8740_F
   │                      │                                                                                └─-i bond2.362 -j MY_IN_733d7567a_F
   │                      │                                                                                                  └─-i bond2.362 -j ACCEPT
   │                      └─-i bond2.362 -j MY_IN_733d7567a_42fc1d83
   │                                        └─-s 192.168.9.0/24 -i bond2.362 -j MY_IN_733d7567a_42fc1d83_F
   │                                                                            └─-i bond2.362 -j MY_IN_733d7567a_F
   │                                                                                              └─-i bond2.362 -j ACCEPT
   └─-j MY_IN_TAIL
        ├─-m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
        ├─-i lo -j ACCEPT
        ├─-p icmp -j ACCEPT
        ├─-m conntrack --ctstate INVALID -j DROP
        └─-j REJECT --reject-with icmp-host-prohibited
...
```

If STDOUT default encoding is not UTF-8, try to set it manually with PYTHONIOENCODING envvar.
```
$ iptables-save -t filter | PYTHONIOENCODING=utf-8 ./iptables-tree
```
