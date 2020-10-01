#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
defmodule Melixir.MixProject do
  use Mix.Project

  def project do
    [
      app: :melixir,
      version: "0.0.1",
      elixir: "~> 1.7",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [
      extra_applications: [:logger]
    ]
  end

  defp deps do
    []
  end
end
