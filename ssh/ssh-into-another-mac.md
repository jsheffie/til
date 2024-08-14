
In this secnario ( which I have done more than a few times )
I want to copy some data from an old mac to a new one.


old-mac
- Enable sshd
- System Settings -> Sharing -> Enable Remote Login
- configure users you want `Administrators`
Now you can ssh in with:
$ ssh <username>@hostname 
can use hostname or ip address

to get the ip address use
`$ ifconfig en0`

ssh jeffsheffield@192.168.1.210

Should also be able to scp as well