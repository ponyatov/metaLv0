![](static/logo.png)
#  `SHED`
## Task Manager and Scheduler

* stand-alone device-hosted architecture
  * no servers, only message dispatch hub
  * web backend is optional and can be isolated per client
* supported platforms:
  * Web Cloud, personal VPS
  * Linux
  * Android
* powered by Erlang/Elixir
* powered by `metaL`

(c) Dmitry Ponyatov <<dponyatov@gmail.com>> 2020 MIT License

github: https://github.com/ponyatov/metaL/tree/master/SHED

## Install


```
	~$ git clone --depth 1 -o gh https://github.com/ponyatov/metaL ~/metaL
	~$ cd ~/metaL/SHED
	~/metaL/SHED$ make install
```


## Tutorial

* Cowboy web server
	* [Building Alchemist.Camp](https://www.youtube.com/playlist?list=PLFhQVxlaKQEn5pqhwqdxItvv80ZnoLqMA)
		* [AC1: Making a site with just the Cowboy web server](https://www.youtube.com/watch?v=LDLzqLl0aeU&list=PLFhQVxlaKQEn5pqhwqdxItvv80ZnoLqMA&index=1)
		* [AC3: Building a router and handling static assets](https://www.youtube.com/watch?v=iiFQVGmHhbU&list=PLFhQVxlaKQEn5pqhwqdxItvv80ZnoLqMA&index=3)
