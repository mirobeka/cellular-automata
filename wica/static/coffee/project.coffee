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

  foo = (event) ->
    replayName = $(@).attr("data-name")
    jsonData = loadReplayData replayName
    if

  hmm = $('a.load.replay').bind('click', foo)
