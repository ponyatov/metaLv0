#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
require Logger
# / <section:top>
defmodule Scada do
end
defmodule Scada.Web.Handler do
  def init({:tcp,:http}, req, router) do
    {:ok, req, router}
  end
  def handle(req, router) do
    {path, req} = :cowboy_req.path(req)
    Logger.info [path: path]
    
        {headers, data} =
            case router.call(path,req) do
            {ct,extra,data} -> { [{"Content-Type",ct         }] ++ extra , data }
            {ct,      data} -> { [{"Content-Type",ct         }]          , data }
                      data  -> { [{"Content-Type","text/html"}]          , data }
            end
                  
    {:ok, resp} = :cowboy_req.reply(200, headers, data, req)
    Logger.info [headers: headers, size: "#{:erlang.byte_size(data)/1024 |> Float.round(1)}K"]
    {:ok, resp, router}
  end
  def terminate(_reason, _req, _router) do
    :ok
  end
end
defmodule Scada.Web.Router do
  def call(path,req) do
    route(path,req)
  end
  # \ <section:style>
  defp style() do
    """
      <STYLE>
        * {
          background: #222;
          color: lightgreen;
        }
        pre {
          white-space: pre-wrap;
          word-wrap: break-word;
        }
        a {
          color: #0A8;
          text-decoration: none;
        }
        a:hover {
          color: #08A;
        }
      </STYLE>
    """
  end
  defp manifest(), do: ~S|<link rel="manifest" href="/manifest">|
  # / <section:style>
  # \ <section:logo>
  defp route("/favicon.ico",req), do:
    route("/static/logo.png",req)
  defp route("/static/logo.png",_req) do
    {
                  "image/png",
                  # [{"Content-Disposition",~s|attachment; filename="bzzlogogo.png";|}],
                  File.read!("static/logo.png")
                }
  end
  # / <section:logo>
  # \ <section:about>
  defp route("/README",req), do: route("/about",req)
  defp route("/README.md",req), do: route("/about",req)
  defp route("/about",_req) do
    """
      #{style()}
      #{Earmark.as_html!(File.read!("README.md"))}
    """
  end
  # / <section:about>
  # \ <section:manifest>
  @doc " https://developer.mozilla.org/ru/docs/Web/Manifest "
  defp route("/manifest",_req) do
    {
      "application/manifest+json",
      """
      {
        "name": "SCADA",
        "short_name": "SCADA",
        "start_url": ".",
        "display": "standalone",
        "background_color": "#222",
        "theme_color": "#222",
        "orientation": "portrait-primary",
        "icons": [{
          "src": "/static/logo.png",
          "sizes": "256x256",
          "type": "image/png"
        }]
      }
      """
    }
  end
  # / <section:manifest>
  # \ <section:index>
  defp route("/",_req) do
    
                """
                #{manifest()}
                #{style()}
                <img src="/static/logo.png" height=3ex> <a href="/about">about</a>
                <hr>
                """
                
  end
  # / <section:index>
  # \ <section:unknown>
  defp route(path,req) do
    """
      #{style()}
      <PRE>#{DateTime.utc_now} UTC / #{inspect :calendar.local_time}</PRE>
      <PRE>#{inspect [Application.fetch_env!(:scada,:host),Application.fetch_env!(:scada,:port)]}</PRE>
      <H1>[#{path}]</H1>
      <PRE>
        #{inspect req}
      </PRE>
    """
  end
  # / <section:unknown>
end
