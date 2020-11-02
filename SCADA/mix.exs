#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
defmodule Scada.MixProject do
  use Mix.Project
  def project do
    [
      # \ <section:project>
      app: :scada,
      version: "0.0.1",
      description: "SCADA",
      source_url: "https://github.com/ponyatov/metaL/tree/master/SCADA",
      deps: deps()
      # / <section:project>
    ]
  end
  def application do
    [
      mod: {Scada.Application, []},
      applications: [
        # \ <section:apps>
        :cowboy,
        # / <section:apps>
      ],
      extra_applications: [
        # \ <section:extra>
        :logger,
        # / <section:extra>
      ]
    ]
  end
  defp deps do
    [
      # \ <section:deps>
      {:cowboy, "~> 1.0.0"},
      {:earmark, "~> 1.4"},
      {:modbus, "~> 0.3.7"},
      # / <section:deps>
      {:ex_doc, ">= 0.0.0", only: :dev, runtime: false}
    ]
  end
end
