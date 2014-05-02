root = exports ? this

root.displayValues = false

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

    unbindAll: =>
        console.log "unbinding"
        $(".playButton").parent().unbind("click", @start)
        $(".pauseButton").parent().unbind("click", @pause)
        $(".stopButton").parent().unbind("click", @stop)
        $(".forwardButton").parent().unbind("click", @forward)
        $(".fastForwardButton").parent().unbind("click", @fastForward)
        $(".backwardButton").parent().unbind("click", @backward)
        $(".fastBackwardButton").parent().unbind("click", @fastBackward)

        $(".speedUp").parent().unbind("click", @speedUp)
        $(".slowDown").parent().unbind("click", @slowDown)


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

            if root.displayValues
                @ctx.font = "#{@replay.resolution/2}px courier new"
                @ctx.fillStyle = "black"
                if (rgb[0]+rgb[1]+rgb[2])/3 < 128
                    @ctx.fillStyle = "white"

                text = "#{Math.round(state["state"] * 10) / 10}"
                l = text.length*@replay.resolution/2
                r = @replay.resolution/2
                @ctx.fillText(text, x+r-l/3,y+r*1.5)

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

recordReplay = (event) ->
    $.ajax
        type: "POST"
        data:
            "replay": "true"
        url: "."
        success: (response) ->
            console.log response

$(document).ready ->
    $(".ui.dimmable").dimmer({
            duration:
                show: 300
                hide: 700
        })

    $('.ui.checkbox').checkbox().on('click', () ->
        root.displayValues = !root.displayValues
        root.player.draw()
    )

    loadReplayData= (replayName, callback) ->
        $.ajax
            type: "GET"
            url: "../replay/#{replayName}/"
            success: callback

    otherFoo= (replayData) ->
        replayData = JSON.parse replayData
        root.player = new ReplayPlayer(replayData)
        root.player.initControls()
        root.player.updateStats()
        root.player.draw()
        $(".ui.dimmable").dimmer("hide")

    foo = (event) ->
        if root.player?
            root.player.stop()
            root.player.unbindAll()
        $(".ui.dimmable").dimmer("show")
        replayName = $(@).attr("data-name")
        loadReplayData replayName, otherFoo

    hmm = $('a.load.replay').bind('click', foo)
    $('.recordReplay').bind('click', recordReplay)
