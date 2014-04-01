root = exports ? this

# this class will be for controlling what's happening on replay canvas
class ReplayPlayer
    constructor: (@replay) ->
        # pass
        @canvas = $("#replayCanvas").get(0)
        @ctx = @canvas.getContext("2d")
        @canvas.width = @replay.width*@replay.resolution
        @canvas.height = @replay.height*@replay.resolution
        @fps = 10
        @step=0

    initControls: =>
        $(".playButton").parent().bind("click", @start)
        $(".pauseButton").parent().bind("click", @pause)
        $(".stopButton").parent().bind("click", @stop)
        $(".forwardButton").parent().bind("click", @forward)
        $(".fastForwardButton").parent().bind("click", @fastForward)
        $(".backwardButton").parent().bind("click", @backward)
        $(".fastBackwardButton").parent().bind("click", @fastBackward)

        $(".speedUp").parent().bind("click", @speedUp)
        $(".slowDown").parent().bind("click", @slowDown)

    speedUp: =>
        @fps += 2
        @updateStats()

    slowDown: =>
        @fps -= 2 unless @fps <= 2
        @updateStats()

    loop: =>
        return unless @running
        @clear()
        @update()
        #@draw()
        @queue()

    queue: =>
        nextFrame = =>
            window.requestAnimationFrame(@loop)
        drawTimeout = 1000 / @fps
        window.setTimeout(nextFrame, drawTimeout)

    clear: =>
        @ctx.clearRect(0,0,@canvas.width, @canvas.height)

    map_state_to_color: (state) =>
        if "rgb" of state
            return state.rgb
        else if "grayscale" of state
            return [state.grayscale, state.grayscale, state.grayscale]

    draw: (replay) =>
        for state,idx in @replay.data[@step]
            rgb = @map_state_to_color(state)
            @ctx.fillStyle = "rgb(#{rgb[0]},#{rgb[1]},#{rgb[2]})"
            x = (idx % @replay.width)*@replay.resolution
            y = Math.floor(idx / @replay.height)*@replay.resolution
            @ctx.fillRect(x, y, @replay.resolution, @replay.resolution)

    clearStats: =>
        $('.frame').text("0/0")

    updateStats: =>
        $('.frame').text("#{@step}/#{@replay.data.length}")
        $('.fps').text("#{@fps}")

    update: =>
        if @step >= @replay.data.length
            @stop()
            return
        @draw(@replay)
        @updateStats()
        @step++

    pause: =>
        console.log "pause"
        if @running
            @running = false

    backward: =>
        @pause()
        @step--
        @draw(@replay)
        @updateStats()

    fastBackward: =>
        @pause()
        @step = 0
        @draw(@replay)
        @updateStats()

    forward: =>
        @pause()
        @step++
        @draw(@replay)
        @updateStats()

    fastForward: =>
        @pause()
        @step = @replay.data.length-1
        @draw(@replay)
        @updateStats()

    stop: =>
        @clear()
        @running = false
        @step = 0
        @updateStats()

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
        player.updateStats()
        player.draw()
        $(".ui.dimmable").dimmer("show")
        hideDimmer = ->
            $(".ui.dimmable").dimmer("hide")
        window.setTimeout( hideDimmer, 1000)

    foo = (event) ->
        console.log "getting data from server"
        replayName = $(@).attr("data-name")
        jsonData = loadReplayData replayName, otherFoo

    hmm = $('a.load.replay').bind('click', foo)

recordReplay = (event) ->
    $.ajax
        type: "POST"
        data:
            "replay": "true"
        url: "."
        success: (response) ->
            console.log response


$(document).ready ->
    $('.recordReplay').bind('click', recordReplay)
