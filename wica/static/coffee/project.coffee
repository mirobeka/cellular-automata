# this class will be for controlling what's happening on replay canvas
class ReplayPlayer
  constructor: (@width, @height, @resolution) ->
    console.log("ReplayPlayer constructor")

$(document).ready ->
  new FormSubmitter(".ui.update.form", "PUT", ".", (response) -> window.location.assign response)
  new FormSubmitter(".ui.delete.form", "DELETE", ".", (response) -> window.location.assign response)

  new ReplayPlayer(20, 100, 100)
