class Useless
  constructor: ->
   $('#content').bind 'click', @do_stuff

  do_stuff: =>
    alert("stuff")
    

$(document).ready ->
  new Useless
