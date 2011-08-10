Apache Config
==============

http://matt.might.net/articles/how-to-emergency-web-scaling/

<IfModule mpm_worker_module>
    StartServers          4
    MinSpareThreads      50
    MaxSpareThreads      150
    ThreadLimit          64
    ThreadsPerChild      25
    MaxClients          400 
    MaxRequestsPerChild   0
</IfModule>
