


### Filtering pre-flight request
When working in my development env. I see lots of annoying extra traffic.
We have sentry configured so I see lots of `/api` traffic to places I don't care
about watching. So the first part of the filter below, filters out those requests.
Then to the meet of this TIL.
I want to get rid of the OPTIONS (pre-flight) calls.
Chrome dev tools allows you to filter those ( and many other requests )
using the `-<name>:<value>` construct. 
Just type `-` in the Network tab filter and it will pop-up auto complete options
on the things you can use.
What I needed in this case was 

```
http://jds.local.me:8000/api/ -method:OPTIONS
```

[source](https://stackoverflow.com/questions/35567580/how-to-filter-hide-pre-flight-requests-on-my-dev-tools-network)