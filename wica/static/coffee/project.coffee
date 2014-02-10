# this class will be for controlling what's happening on replay canvas
class ReplayPlayer
  constructor: (@width, @height, @resolution) ->
    @canvas = oCanvas.create({ canvas: "#replayCanvas", background: "#eee"})
    @cells = []
    @stepIndex = 0

  addCell: (size) =>
    cell = new Cell(@canvas, 10, 20, 20)
    @cells.push(cell)

  start: (speed=30) =>
    @canvas.settings.fps = speed
    @canvas.setLoop(@loop).start()

  loop: () =>
    for cell in @cells
      @stepIndex++
      @replay.state(@stepIndex, cell)

class Replay
  constructor: (@jsonData) ->
    console.log("Hello there! Replay reporting for duty")
    console.log("I have following data")
    console.log(@jsonData)

  setState: (stepIndex, cell) =>
    rgb = "rbg(#{@jsonData[strepIndex]}, #{@jsonData[strepIndex]}, #{@jsonData[strepIndex]}"
    cell.setColor(rgb)

class Cell
  constructor: (@parent, @size, @x, @y) ->
    @rectangle = @parent.display.rectange({
      x: @x
      y: @y
      origin: { x: "center", y: "center" }
      width: @size
      height: @size
      stroke: "#999"
      fill: "#aaa"
    }).add()

  setColor: (color) =>
    @rectangle.fill(color)


$(document).ready ->
  new FormSubmitter(".ui.update.form", "PUT", ".", (response) -> window.location.assign response)
  new FormSubmitter(".ui.delete.form", "DELETE", ".", (response) -> window.location.assign response)

  player = new ReplayPlayer(20, 100, 100)

  console.log("adding cell")
  player.addCell(100)
  player.start(100)
