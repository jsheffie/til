# How to treat Insecure origins treated as secure ( in a development env )

When working on your desktop/dev env, it is quite common to be running `http` vice `https`. 
Thus you are running in insecure mode. Modern browsers don't allow access to many of their 
API's when running in insecure mode. Because the web is a dangerous place to be.
Here is what that error might look like:

GeolocationPositionError {code: 1, message: 'Only secure origins are allowed (see: [https://goo.gl/Y0ZkNV](https://goo.gl/Y0ZkNV)).'}

So as a developer, who is just trying to make/test the geolocation code how can we work around this fact?


1. Open Chrome and navigate to chrome://flags.
2. Search for "insecure origins" or "geolocation".
   There are a few ways to enable this.
   I used "Insecure origins treated as secure"
3. added `http://jds.local.me:3000/` and change the flag setting to "Enabled" (restart Chrome if prompted).



