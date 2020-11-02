#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
require Logger
# / <section:top>
defmodule SHED.Application do
  # \ <section:module>
  use Application

  def start(_type, _args) do
    # \ <section:start>
    cowboy()
    # / <section:start>
    children = [
      # Starts a worker by calling: Camp.Worker.start_link(arg)
      # {SHED.Worker, arg}
    ]

    opts = [strategy: :one_for_one, name: SHED.Supervisor]
    Supervisor.start_link(children, opts)
  end

  @procs 0x11
  defp cowboy() do
    # \ <section:route>
    route_undef = {:_, SHED.Web.Handler, SHED.Web.Router}
    routes = [route_undef]
    # / <section:route>
    hostname = :_
    dispatch = :cowboy_router.compile([{hostname, routes}])
    host = Application.fetch_env!(:shed, :host)
    port = Application.fetch_env!(:shed, :port)
    opts = [port: port]
    env = [dispatch: dispatch]

    case :cowboy.start_http(:http, @procs, opts, env: env) do
      {:ok, _pid} -> Logger.info("#{__MODULE__} http://#{host}:#{port}")
      {reason, err} -> Logger.error("#{inspect([__MODULE__, reason, err])}")
    end
  end

  # / <section:module>
end
