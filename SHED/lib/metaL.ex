defmodule M.Object do
  @frame type: :object, val: nil, nest: []
  def frame, do: @frame
  defstruct @frame
  # defmacro __using__(fields) do
  #   frame = @frame ++ fields
  #   quote do
  #     defstruct unquote(frame)
  #   end
  # end
  # defp nest(this), do: this.nest
  def push(this, that) do
    put_in(this.nest, this.nest ++ [that])
  end

  def x do
    hello = %M.Object{val: :hello}
    IO.puts(inspect(hello))
    world = %M.Object{val: :world}
    IO.puts(inspect(world))
    IO.puts(inspect(hello |> M.Object.push(world)))
    IO.puts(inspect(hello))
  end
end

defimpl Inspect, for: M.Object do
  def inspect(object, _options) do
    dump(object)
  end

  defp dump(object, depth \\ 0) do
    ret = pad(depth) <> "<#{object.val}>"

    ret =
      object.nest
      |> Enum.reduce(
        ret,
        fn i, acc -> acc <> dump(i, depth + 1) end
      )

    ret
  end

  defp pad(depth), do: "\n" <> String.duplicate("\t", depth)
end

defmodule M.String do
  # use M.Object
  defstruct M.Object.frame()
end

defmodule M.Number do
  # use M.Object
  defstruct M.Object.frame() |> Keyword.put(:val, 0)
end
