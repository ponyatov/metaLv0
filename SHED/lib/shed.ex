#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
require Logger
# / <section:top>
defmodule SHED do
end

defmodule SHED.Web.Handler do
  def init({:tcp, :http}, req, router) do
    {:ok, req, router}
  end

  def handle(req, router) do
    {path, req} = :cowboy_req.path(req)

    # Logger.info(path: path)

    {headers, data} =
      case router.call(path, req) do
        {ct, extra, data} -> {[{"Content-Type", ct}] ++ extra, data}
        {ct, data} -> {[{"Content-Type", ct}], data}
        data -> {[{"Content-Type", "text/html"}], data}
      end

    {:ok, resp} = :cowboy_req.reply(200, headers, data, req)

    # Logger.info(headers: headers, size: "#{(:erlang.byte_size(data) / 1024) |> Float.round(1)}K")

    {:ok, resp, router}
  end

  def terminate(_reason, _req, _router) do
    :ok
  end
end

defmodule SHED.Web.Router do
  def call(path, req) do
    route(path, req)
  end

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

  defp route("/favicon.ico", req), do: route("/static/logo.png", req)

  defp route("/static/logo.png", _req) do
    {
      "image/png",
      [{"Content-Disposition", ~s|attachment; filename="bzzlogogo.png";|}],
      File.read!("static/logo.png")
    }
  end

  defp route("/", _req) do
    """
      #{style()}
      #{Earmark.as_html!(File.read!("README.md"))}
    """
  end

  defp route("/hello", _req) do
    {
      "text/html",
      [{"Refresh", "1;"}],
      """
        #{style()}
        <STYLE>.metaL { font-size:6mm; }</STYLE>
        <PRE>#{inspect(:calendar.local_time())}</PRE>
        <HR>
        <PRE class=metaL>
        #{inspect(%M.Number{val: 12.34})}
        </PRE>
      """
    }
  end

  defp route(path, req) do
    """
      #{style()}
      <PRE>#{DateTime.utc_now()} UTC / #{inspect(:calendar.local_time())}</PRE>
      <PRE>#{
      inspect([Application.fetch_env!(:shed, :host), Application.fetch_env!(:shed, :port)])
    }</PRE>
      <H1>[#{path}]</H1>
      <PRE>
        #{inspect(req)}
      </PRE>
    """
  end
end
