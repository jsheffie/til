


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


## Chrome inverted filter's that I use to squash noise.
gtag/js && react-refresh && vite/client && materialiconsoutlined && g/collect && src && node_modules && google-analytics && identity && ingest && googleapi

huvr
-node_modules -url:https://fonts.googleapis.com -url:https://analytics.google.com -url:https://fonts.googleapis.com -url:https://fonts.gstatic.com -url:https://identitytoolkit.googleapis.com -url:src/store -url:src/route  -url:src/theme  -url:src/utilities -url:src/hooks -url:src/config -url:src/components -url:https://maps.googleapis.com -url:https://o269624.ingest.sentry.io
