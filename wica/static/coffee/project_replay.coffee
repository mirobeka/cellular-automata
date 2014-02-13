root = exports ? this

# this class will be for controlling what's happening on replay canvas
class ReplayPlayer
  constructor: (@replay) ->
    for c in oCanvas.canvasList
      c.destroy() unless c is null
      oCanvas.canvasList = []

    @canvas = oCanvas.create({ canvas: "#replayCanvas", background: "#eee"})
    @cells = []
    @stepIndex = 0

  initControls: =>
    $(".play.icon").parent().bind("click", @start)
    $(".pause.icon").parent().bind("click", @pause)
    $(".stop.icon").parent().bind("click", @stop)

  initCells: =>
    @addCell(idx) for idx in [0..(@replay.width*@replay.height)-1]

  addCell: (idx) =>
    x = idx % @replay.width
    y = idx / @replay.height
    cell = new Cell(@canvas, idx, @replay.resolution, x, y)
    @cells.push(cell)

  removeCell: (cell) =>
    @canvas.removeChild cell.rectangle

  start: (speed=1) =>
    @canvas.settings.fps = speed
    @canvas.setLoop(@loop).start()

  pause: =>
    @canvas.timeline.stop()

  stop: =>
    @canvas.timeline.stop()
    @stepIndex = 0
    @clearCanvas()
    @initCells()

  clearCanvas: =>
    @removeCell cell for cell in @cells
    @cells = []

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

  loadReplayData= (replayName, callback) ->
    $.ajax
      type: "GET"
      url: "../replay/#{replayName}/"
      success: callback

  otherFoo= (replayData) ->
    replayData = JSON.parse replayData
    player = new ReplayPlayer(replayData)
    player.initControls()
    player.initCells()


  foo = (event) ->
    replayName = $(@).attr("data-name")
    jsonData = loadReplayData replayName, otherFoo

  hmm = $('a.load.replay').bind('click', foo)
