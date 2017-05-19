http --pretty=all POST 172.16.78.17:9803 data:='{"reserved0":"/home/ubuntu","reserved2":"/home/lucent_peng/.ssh/","reserved5":"id_rsa.pub","reserved6":"1"}'
#http --pretty=all POST 172.16.78.17:9803 data:='{"reserved0":"/home/ubuntu","reserved1":"","reserved6":"0"}'
http --pretty=all GET 172.16.78.17:9803/command
