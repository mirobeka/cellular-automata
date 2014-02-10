root = exports ? this

# this class will be for controlling what's happening on replay canvas
class ReplayPlayer
  constructor: (@replay) ->
    @canvas = oCanvas.create({ canvas: "#replayCanvas", background: "#eee"})
    @cells = []
    @stepIndex = 0

  initCells: =>
    @addCell idx for idx in [0..(@replay.width*@replay.height)-1]

  addCell: (idx) =>
    x = idx % @replay.width
    y = idx / @replay.height
    cell = new Cell(@canvas, idx, @replay.resolution, x, y)
    @cells.push(cell)
    cell.rectangle.bind("click", => @loop())

  start: (speed=30) =>
    @canvas.settings.fps = speed
    @canvas.setLoop(@loop).start()

  loop: () =>
    @stepIndex++
    return false unless @stepIndex < @replay.length
    for cell in @cells
      @setState @stepIndex, cell
      @canvas.draw.redraw()

  setState: (stepIndex, cell) =>
    gray = Math.round(255*@replay.data[stepIndex][cell.idx])
    rgb = "rgb(#{gray},#{gray},#{gray})"
    cell.rectangle.fill = rgb

class Cell
  constructor: (@canvas, @idx, @size, @x, @y) ->
    @rectangle = @canvas.display.rectangle({
      x: Math.floor(@x)*@size
      y: Math.floor(@y)*@size
      origin: { x: "left", y: "top" }
      width: @size
      height: @size
      stroke: "#999"
      fill: "#aaa"
    }).add()


$(document).ready ->
  new FormSubmitter(".ui.update.form", "PUT", ".", (response) -> window.location.assign response)
  new FormSubmitter(".ui.delete.form", "DELETE", ".", (response) -> window.location.assign response)

  ## example data
  jsonReplay=
    width: 2
    height: 2
    resolution: 200
    length: 10
    data:[
      [0.0, 0.0, 0.0, 0.1]
      [0.1, 0.1, 0.2, 0.1]
      [0.2, 0.1, 0.4, 0.1]
      [0.3, 0.1, 0.6, 0.1]
      [0.4, 0.1, 0.8, 0.1]
      [0.5, 0.3, 0.8, 0.1]
      [0.6, 0.6, 0.6, 0.1]
      [0.7, 0.9, 0.4, 0.1]
      [0.8, 0.9, 0.2, 0.1]
      [0.9, 0.9, 0.0, 0.1]
    ]

  root.player = new ReplayPlayer(jsonReplay)
  root.player.initCells()
