### Convert iptables-save format to pstree-like view

iptables-tree is used to convert the output of iptables-save into an easily readable 
rules tree to STDOUT. Use I/O-redirection provided by your shell to write to a file.

#### Example:
```
% ssh core@worker-node-0 sudo iptables-save -t nat | python3 ./iptables-tree.py                
*nat
:PREROUTING ACCEPT [22:1340]
:INPUT ACCEPT [5:320]
:OUTPUT ACCEPT [469:28396]
:POSTROUTING ACCEPT [486:29416]
-A PREROUTING
   └─-j KUBE-SERVICES
        ├─-d 10.254.0.1/32 -p tcp  -m tcp --dport 443 -j KUBE-SVC-NPX46M4PTMTKRN6Y
        │                                                ├─! -s 10.100.0.0/16 -d 10.254.0.1/32 -p tcp  -m tcp --dport 443 -j KUBE-MARK-MASQ
        │                                                │                                                                   └─-j MARK --set-xmark 0x4000/0x4000
        │                                                ├─ -m statistic --mode random --probability 0.33333333349 -j KUBE-SEP-KSYZFRVBAHO3UYKY
        │                                                │                                                            ├─-s 192.168.1.80/32  -j KUBE-MARK-MASQ
        │                                                │                                                            │                        └─-j MARK --set-xmark 0x4000/0x4000
        │                                                │                                                            └─-p tcp  -m tcp -j DNAT [unsupported revision]
        │                                                ├─ -m statistic --mode random --probability 0.50000000000 -j KUBE-SEP-4NXZOMPO3OIGIHOH
        │                                                │                                                            ├─-s 192.168.2.18/32  -j KUBE-MARK-MASQ
        │                                                │                                                            │                        └─-j MARK --set-xmark 0x4000/0x4000
        │                                                │                                                            └─-p tcp  -m tcp -j DNAT [unsupported revision]
        │                                                └─-j KUBE-SEP-53CZXCCEBWWNYZ7X
        │                                                     ├─-s 192.168.3.82/32  -j KUBE-MARK-MASQ
        │                                                     │                        └─-j MARK --set-xmark 0x4000/0x4000
        │                                                     └─-p tcp  -m tcp -j DNAT [unsupported revision]
        ├─-d 10.254.124.194/32 -p tcp  -m tcp --dport 12345 -j KUBE-SVC-GYUT6LJFX34TXRZB
        │                                                      ├─! -s 10.100.0.0/16 -d 10.254.124.194/32 -p tcp  -m tcp --dport 12345 -j KUBE-MARK-MASQ
        │                                                      │                                                                         └─-j MARK --set-xmark 0x4000/0x4000
        │                                                      └─-j KUBE-SEP-KANST5L7MCNDJ4PP
        │                                                           ├─-s 10.100.0.2/32  -j KUBE-MARK-MASQ
        │                                                           │                      └─-j MARK --set-xmark 0x4000/0x4000
        │                                                           └─-p tcp  -m tcp -j DNAT [unsupported revision]
        ├─-d 10.254.216.143/32 -p tcp  -m tcp --dport 443 -j KUBE-SVC-LUWOVUBMMENYS4C5
        │                                                    ├─! -s 10.100.0.0/16 -d 10.254.216.143/32 -p tcp  -m tcp --dport 443 -j KUBE-MARK-MASQ
        │                                                    │                                                                       └─-j MARK --set-xmark 0x4000/0x4000
        │                                                    └─-j KUBE-SEP-UDZ4WRQJYCIV757T
        │                                                         ├─-s 10.100.5.2/32  -j KUBE-MARK-MASQ
        │                                                         │                      └─-j MARK --set-xmark 0x4000/0x4000
        │                                                         └─-p tcp  -m tcp -j DNAT [unsupported revision]
        ├─-d 10.254.0.10/32 -p tcp  -m tcp --dport 53 -j KUBE-SVC-ERIFXISQEP7F7OF4
        │                                                ├─! -s 10.100.0.0/16 -d 10.254.0.10/32 -p tcp  -m tcp --dport 53 -j KUBE-MARK-MASQ
        │                                                │                                                                   └─-j MARK --set-xmark 0x4000/0x4000
        │                                                ├─ -m statistic --mode random --probability 0.50000000000 -j KUBE-SEP-4ABE7GWA3NUIFMZ3
        │                                                │                                                            ├─-s 10.100.2.2/32  -j KUBE-MARK-MASQ
        │                                                │                                                            │                      └─-j MARK --set-xmark 0x4000/0x4000
        │                                                │                                                            └─-p tcp  -m tcp -j DNAT [unsupported revision]
        │                                                └─-j KUBE-SEP-BVZHU4XEX7KSKFVE
        │                                                     ├─-s 10.100.5.5/32  -j KUBE-MARK-MASQ
        │                                                     │                      └─-j MARK --set-xmark 0x4000/0x4000
        │                                                     └─-p tcp  -m tcp -j DNAT [unsupported revision]
        ├─-d 10.254.0.10/32 -p tcp  -m tcp --dport 9153 -j KUBE-SVC-JD5MR3NA4I4DYORP
        │                                                  ├─! -s 10.100.0.0/16 -d 10.254.0.10/32 -p tcp  -m tcp --dport 9153 -j KUBE-MARK-MASQ
        │                                                  │                                                                     └─-j MARK --set-xmark 0x4000/0x4000
        │                                                  ├─ -m statistic --mode random --probability 0.50000000000 -j KUBE-SEP-JCKA4RWVBEU37RQG
        │                                                  │                                                            ├─-s 10.100.2.2/32  -j KUBE-MARK-MASQ
        │                                                  │                                                            │                      └─-j MARK --set-xmark 0x4000/0x4000
        │                                                  │                                                            └─-p tcp  -m tcp -j DNAT [unsupported revision]
        │                                                  └─-j KUBE-SEP-ACORHR333NBTL5O6
        │                                                       ├─-s 10.100.5.5/32  -j KUBE-MARK-MASQ
        │                                                       │                      └─-j MARK --set-xmark 0x4000/0x4000
        │                                                       └─-p tcp  -m tcp -j DNAT [unsupported revision]
        ├─-d 10.254.0.10/32 -p udp  -m udp --dport 53 -j KUBE-SVC-TCOU7JCQXEZGVUNU
        │                                                ├─! -s 10.100.0.0/16 -d 10.254.0.10/32 -p udp  -m udp --dport 53 -j KUBE-MARK-MASQ
        │                                                │                                                                   └─-j MARK --set-xmark 0x4000/0x4000
        │                                                ├─ -m statistic --mode random --probability 0.50000000000 -j KUBE-SEP-KVG3FTMRLVAZEEDA
        │                                                │                                                            ├─-s 10.100.2.2/32  -j KUBE-MARK-MASQ
        │                                                │                                                            │                      └─-j MARK --set-xmark 0x4000/0x4000
        │                                                │                                                            └─-p udp  -m udp -j DNAT [unsupported revision]
        │                                                └─-j KUBE-SEP-5ULIPHUUNKIYVF34
        │                                                     ├─-s 10.100.5.5/32  -j KUBE-MARK-MASQ
        │                                                     │                      └─-j MARK --set-xmark 0x4000/0x4000
        │                                                     └─-p udp  -m udp -j DNAT [unsupported revision]
        ├─-d 10.254.36.60/32 -p tcp  -m tcp --dport 443 -j KUBE-SVC-4HQ2X6RJ753IMQ2F
        │                                                  ├─! -s 10.100.0.0/16 -d 10.254.36.60/32 -p tcp  -m tcp --dport 443 -j KUBE-MARK-MASQ
        │                                                  │                                                                     └─-j MARK --set-xmark 0x4000/0x4000
        │                                                  └─-j KUBE-SEP-XNZKJJUVRF4YFPCQ
        │                                                       ├─-s 10.100.4.4/32  -j KUBE-MARK-MASQ
        │                                                       │                      └─-j MARK --set-xmark 0x4000/0x4000
        │                                                       └─-p tcp  -m tcp -j DNAT [unsupported revision]
        ├─-d 10.254.161.159/32 -p tcp  -m tcp --dport 8000 -j KUBE-SVC-4GCQP7GTYLI53KTV
        │                                                     ├─! -s 10.100.0.0/16 -d 10.254.161.159/32 -p tcp  -m tcp --dport 8000 -j KUBE-MARK-MASQ
        │                                                     │                                                                        └─-j MARK --set-xmark 0x4000/0x4000
        │                                                     └─-j KUBE-SEP-IVT2Y2NK23SUXR6O
        │                                                          ├─-s 10.100.4.3/32  -j KUBE-MARK-MASQ
        │                                                          │                      └─-j MARK --set-xmark 0x4000/0x4000
        │                                                          └─-p tcp  -m tcp -j DNAT [unsupported revision]
        ├─-d 10.254.53.246/32 -p tcp  -m tcp --dport 80 -j KUBE-SVC-OVTWZ4GROBJZO4C5
        │                                                  ├─! -s 10.100.0.0/16 -d 10.254.53.246/32 -p tcp  -m tcp --dport 80 -j KUBE-MARK-MASQ
        │                                                  │                                                                     └─-j MARK --set-xmark 0x4000/0x4000
        │                                                  └─-j KUBE-SEP-UKGAPEWCTNNMKZAR
        │                                                       ├─-s 10.100.3.16/32  -j KUBE-MARK-MASQ
        │                                                       │                       └─-j MARK --set-xmark 0x4000/0x4000
        │                                                       └─-p tcp  -m tcp -j DNAT [unsupported revision]
        └─ -m addrtype --dst-type LOCAL -j KUBE-NODEPORTS
                                           └─-p tcp  -m tcp --dport 31509 -j KUBE-EXT-OVTWZ4GROBJZO4C5
                                                                             ├─-j KUBE-MARK-MASQ
                                                                             │    └─-j MARK --set-xmark 0x4000/0x4000
                                                                             └─-j KUBE-SVC-OVTWZ4GROBJZO4C5
                                                                                  ├─! -s 10.100.0.0/16 -d 10.254.53.246/32 -p tcp  -m tcp --dport 80 -j KUBE-MARK-MASQ
                                                                                  │                                                                     └─-j MARK --set-xmark 0x4000/0x4000
                                                                                  └─-j KUBE-SEP-UKGAPEWCTNNMKZAR
                                                                                       ├─-s 10.100.3.16/32  -j KUBE-MARK-MASQ
                                                                                       │                       └─-j MARK --set-xmark 0x4000/0x4000
                                                                                       └─-p tcp  -m tcp -j DNAT [unsupported revision]
...
```

If STDOUT default encoding is not UTF-8, try to set it manually with PYTHONIOENCODING envvar.
```
$ iptables-save -t filter | PYTHONIOENCODING=utf-8 ./iptables-tree
```
