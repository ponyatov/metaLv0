![](static/logo.png)
#  `SCADA`
## SCADA MetaProgramming Template

* targeted for IoT applications

* https://www.youtube.com/watch?v=g8gjWuzTwh0
* http://automate.courses/
* https://xod.io/
  * https://github.com/xodio/xod

* [Elixir для интернета вещей](https://www.youtube.com/watch?v=L4Yqwlhxq1E)

* Platform manuals:
  * Phoenix/Rack/Cowboy
    * https://www.youtube.com/watch?v=LDLzqLl0aeU
  * `n2o`
    * https://n2o.dev/books/n2o.pdf
    * [1.1 Erlang in Web with N2O](https://www.youtube.com/watch?v=uMg9n-gLCYM)
    * [1.2 Erlang in Web with N2O](https://www.youtube.com/watch?v=i79-gOI-DZI)
    * [Эрланг для веб-разработки (1) -> Знакомство;](https://habr.com/ru/post/273979/)
    * [Эрланг для веб-разработки (2) -> БД и деплой;](https://habr.com/ru/post/274107/)

  * `MQTT`
    * https://medium.com/@svengehring/implementing-mqtt-in-elixir-part-1-99257a81f182
  * BERT/ETF
    * [BERT and BERT-RPC 1.0 Specification](http://bert-rpc.org/)
    * [Serialization series — Do you speak Erlang ETF or BERT? (part 1)](https://medium.com/@niamtokik/serialization-series-do-you-speak-erlang-etf-or-bert-part-1-ff70096b50c0)
    * [Introducing BERT and BERT-RPC](https://github.blog/2009-10-20-introducing-bert-and-bert-rpc/)

* SCADA design tutorials:
  * [1210- 1235: Making everybody comfortable with Erlang: a SCADA system for thermal control](https://github.com/ocamllabs/icfp2016-blog/issues/146)
    * [video](https://www.youtube.com/embed/wyzdtIuz2ko)
  * Ямолдинов Дмитрий Николаевич, Кангин Михаил Владимирович<br>
    [Разработка SCADA-систем. Учебное пособие](https://www.ozon.ru/context/detail/id/149522472/)

* core in Erlang/Elixir
* Phoenix web interface
* powered by `metaL`

(c) Dmitry Ponyatov <<dponyatov@gmail.com>> 2020 MIT License

github: https://github.com/ponyatov/metaL/tree/master/SCADA

## Install


```
	~$ git clone --depth 1 -o gh https://github.com/ponyatov/metaL ~/metaL
	~$ cd ~/metaL/SCADA
	~/metaL/SCADA$ make install
```


## Tutorial

* Cowboy web server
	* [Building Alchemist.Camp](https://www.youtube.com/playlist?list=PLFhQVxlaKQEn5pqhwqdxItvv80ZnoLqMA)
		* [AC1: Making a site with just the Cowboy web server](https://www.youtube.com/watch?v=LDLzqLl0aeU&list=PLFhQVxlaKQEn5pqhwqdxItvv80ZnoLqMA&index=1)
		* [AC3: Building a router and handling static assets](https://www.youtube.com/watch?v=iiFQVGmHhbU&list=PLFhQVxlaKQEn5pqhwqdxItvv80ZnoLqMA&index=3)
