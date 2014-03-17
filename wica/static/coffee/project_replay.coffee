root = exports ? this

# this class will be for controlling what's happening on replay canvas
class ReplayPlayer
    constructor: (@replay) ->
        # pass
        @canvas = $("#replayCanvas").get(0)
        @ctx = @canvas.getContext("2d")
        @canvas.width = @replay.width*@replay.resolution
        @canvas.height = @replay.height*@replay.resolution
        @step=0

    initControls: =>
        $(".play.icon").parent().bind("click", @start)
        $(".pause.icon").parent().bind("click", @pause)
        $(".stop.icon").parent().bind("click", @stop)

    loop: =>
        return unless @running
        @clear()
        @update()
        #@draw()
        @queue()

    clear: =>
        @ctx.clearRect(0,0,@canvas.width, @canvas.height)

    update: =>
        if @step >= @replay.length
            @stop()
            return

        for state,idx in @replay.data[@step]

            # this data are just white cells -> add some random just to see
            # some changes...

            r = Math.random()
            gray = Math.floor(state*r)

            @ctx.fillStyle = "rgb(#{gray},#{gray},#{gray})"
            x = (idx % @replay.width)*@replay.resolution
            y = Math.floor(idx / @replay.height)*@replay.resolution
            @ctx.fillRect(x, y, @replay.resolution, @replay.resolution)
        @step++

    queue: =>
        nextFrame = =>
            window.requestAnimationFrame(@loop)
        window.setTimeout(nextFrame, 100)

    pause: =>
        console.log "pause"
        if @running
            @running = false
        else
            @running = true
            window.requestAnimationFrame(@loop)

    stop: =>
        @clear()
        @running = false
        @step = 0

    start: =>
        console.log "start"
        @running = true
        window.requestAnimationFrame(@loop)

$(document).ready ->
    $(".ui.dimmable").dimmer({
            duration:
                show: 300
                hide: 700
        })

    loadReplayData= (replayName, callback) ->
        $.ajax
            type: "GET"
            url: "../replay/#{replayName}/"
            success: callback

    otherFoo= (replayData) ->
        console.log "callback with data from server"
        console.log replayData
        console.log "parsing data"
        replayData = JSON.parse replayData
        console.log "parsed data"
        console.log replayData

        console.log "Creating new ReplayPlayer"
        player = new ReplayPlayer(replayData)
        console.log player
        console.log "initializing controls"
        player.initControls()
        $(".ui.dimmable").dimmer("show")
        hideDimmer = ->
            $(".ui.dimmable").dimmer("hide")
        window.setTimeout( hideDimmer, 1000)



    foo = (event) ->
        console.log "getting data from server"
        replayName = $(@).attr("data-name")
        jsonData = loadReplayData replayName, otherFoo

    hmm = $('a.load.replay').bind('click', foo)
