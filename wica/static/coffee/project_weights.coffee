root = exports ? this

class Layer
    constructor: (selector, @data, @neuron) ->
        @canvas = $(selector).get(0)
        @ctx = @canvas.getContext("2d")
        @canvas.width = 99
        @canvas.height = 99

    draw: =>
        neuron = @getNeuron()

        flatten = [].concat.apply([], neuron)
        min_val = Math.min(0,Math.min.apply(null, flatten))
        max_val = Math.max.apply(null, flatten)
        mid_val = (min_val+max_val)/2

        scale = d3.scale.linear().range(["darkturquoise","white","orange"]).domain([min_val, 0, max_val])

        @ctx.font = "10px courier new"
        for row,ridx in neuron
            for val,cidx in row
                @ctx.fillStyle = scale(val)
                @ctx.fillRect(33*cidx,33*ridx,33,33)

                @ctx.fillStyle = "#000"
                text = "#{Math.round(val * 100) / 100}"
                l = text.length*9

                @ctx.fillText(text,33*cidx+16-l/3,33*ridx+20)

    removeBias: (matrix) =>
        return (row[1..] for row in matrix)

    normalize: (matrix) =>
        flatten = [].concat.apply([],matrix)
        min_val = Math.min.apply(null, flatten)
        max_val = Math.max.apply(null, flatten)

        for row,ridx in matrix
            for val,cidx in row
                matrix[ridx][cidx] = (val-min_val)/(max_val-min_val)
        return matrix

    mapNetworkToNeigh: (neuron, neighType) =>
        if neighType == "vonneumann"
            [st,n,e,s,w] = neuron
            return [ [0,n ,0], [w,st,e], [0,s ,0] ]
        else if neighType == "ediemoore"
            [st,n,ne,e,se,s,sw,w,nw] = neuron
            return [ [nw ,n ,ne], [w,st,e], [sw,s ,se] ]

class Layer1 extends Layer
    constructor: (data, neuron)->
        super("#layer1_neuron#{neuron}", data, neuron)
        @layer1 = data["layer1"]

    getNeuron: =>
        layer = @removeBias(@layer1)
        #layer = @normalize(layer)
        neuron = @mapNetworkToNeigh(layer[@neuron], @data["neigh"])


class Layer2 extends Layer
    constructor: (data, neuron)->
        super("#layer2_neuron#{neuron}",data, neuron)
        @layer1 = data["layer1"]
        @layer2 = data["layer2"]

    multMatrix: (matrix, y) ->
        return ((y*x for x in row) for row in matrix)

    sumMatrices: (m1, m2) ->
        result = []
        for r,ri in m1
            result.push []
            for c,ci in r
                result[ri].push(m1[ri][ci] + m2[ri][ci])
        return result

    getNeuron: =>
        layer2 = @removeBias(@layer2)[@neuron]
        layer1 = @removeBias(@layer1)
        sum = [[0,0,0],[0,0,0],[0,0,0]]

        for neuron,idx in layer1
            x = @mapNetworkToNeigh(neuron, @data["neigh"])
            x = @multMatrix(x,layer2[idx])
            sum = @sumMatrices(sum, x)

        return sum

class Progress
    constructor: (@selector, @data) ->
        @fokinData = @parseData(@data)
        console.log @fokinData

    options: ->
        opts =
            title: "progress of error"
            axesDefaults:
                labelRenderer: $.jqplot.CanvasAxisLabelRenderer
            axes:
                xaxis:
                    label: "generations"
                    min: 0
                    max: 200

                yaxis:
                    label: "error"
                    min: 0.0
                    max: 1.0


    show: () =>
        $.jqplot @selector, @fokinData, @options()

    parseData: (data) ->
        parsed = [[]]
        lastGen = 0
        lastErr = 1
        for prog in data
            if prog[0] > lastGen
                lastGen = prog[0]
                lastErr = prog[1]
                parsed[0].push([prog[0], prog[1]])
            else if prog[0] == lastGen and prog[1] < lastErr
                lastGen = prog[0]
                lastErr = prog[1]
                parsed[0].pop()
                parsed[0].push([prog[0], prog[1]])
        parsed[0].push([200, lastErr])

        return parsed
                


replaceHtml = (newHtml) ->
    $("#contentContainer").html newHtml
    
getHtml = (weight) ->
    html = """
            <table class="ui table left aligned segment">
                <thead>
                    <tr>
                        <th>Property</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
           """
    for name,value of weight
        if name == "layer1" or name == "layer2" or name == "progress"
            continue
        if name == "weights"
            xx = 0
            breaklines = "["
            for x in value
                if xx == 4
                    xx = 0
                    breaklines += "\n"
                breaklines += " #{x},"
                xx += 1
            value = breaklines.substring 0,breaklines.length-1
            value += " ]"
        html += """
                <tr>
                    <td>#{name}</td>
                    <td>#{value}</td>
                </tr>
                """

    html += """
                </tbody>
            </table>
            <div id="progress" class="jqplot-target">
            </div>
            <div class="ui middle aligned four column grid">
                <div class="row">
                    <div class="column">
                        <div class="ui input vertical fluid menu">
                            <table id="input">
                                <tr>
                                    <td><span data-var="nw" data-format="%.2f" data-min="-1" data-max="1" data-step="0.1" class="TKAdjustableNumber"></span></td>
                                    <td><span data-var="n" data-format="%.2f" data-min="-1" data-max="1" data-step="0.1" class="TKAdjustableNumber"></span></td>
                                    <td><span data-var="ne" data-format="%.2f" data-min="-1" data-max="1" data-step="0.1" class="TKAdjustableNumber"></span></td>
                                </tr>
                                <tr>
                                    <td><span data-var="w" data-format="%.2f" data-min="-1" data-max="1" data-step="0.1" class="TKAdjustableNumber"></span></td>
                                    <td><span data-var="st" data-format="%.2f" data-min="-1" data-max="1" data-step="0.1" class="TKAdjustableNumber"></span></td>
                                    <td><span data-var="e" data-format="%.2f" data-min="-1" data-max="1" data-step="0.1" class="TKAdjustableNumber"></span></td>
                                </tr>
                                <tr>
                                    <td><span data-var="sw" data-format="%.2f" data-min="-1" data-max="1" data-step="0.1" class="TKAdjustableNumber"></span></td>
                                    <td><span data-var="s" data-format="%.2f" data-min="-1" data-max="1" data-step="0.1" class="TKAdjustableNumber"></span></td>
                                    <td><span data-var="se" data-format="%.2f" data-min="-1" data-max="1" data-step="0.1" class="TKAdjustableNumber"></span></td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    <div class="column">
                        <div class="ui layer1 vertical fluid menu">
                        </div>
                    </div>
                    <div class="column">
                        <div class="ui layer2 vertical fluid menu">
                        </div>
                    </div>
                    <div class="column">
                        <div class="ui vertical fluid menu">
                            <canvas id="output" class="border" width="50" height="50"></canvas>
                        </div>
                    </div>
                </div>
            </div>

            """
    return html

addLayer1Neuron = (w,idx) ->
    addNeuron(Layer1, ".layer1", "layer1", w, idx)

addLayer2Neuron = (w,idx) ->
    addNeuron(Layer2, ".layer2", "layer2", w, idx)

addNeuron = (klass, selector, layer, w, idx) ->
    html = """
        <div class="item">
            <canvas id="#{layer}_neuron#{idx}" class="border"></canvas>
        </div>
    """
    $(selector).append(html)
    l = new klass(w, idx)
    l.draw()

displayWeightData = (weight) ->
    html = getHtml weight
    replaceHtml html

    for idx in [0..weight["layer1"].length-1]
        addLayer1Neuron(weight,idx)

    for idx in [0..weight["layer2"].length-1]
        addLayer2Neuron(weight,idx)

displayProgress = (data) ->
    prog = new Progress "progress", data["progress"]
    prog.show()

getData = (weightName, callback) ->
    $.ajax
        type: "GET"
        url: "../weight/#{weightName}/"
        success: callback

parseData = (data) ->
    data = JSON.parse data
    root.data = data
    
    displayWeightData data
    displayProgress data
    initializeInputCells()
    $(".ui.dimmable").dimmer("hide")

loadWeight = (event) ->
    $(".ui.dimmable").dimmer("show")
    replayName = $(@).attr("data-name")
    getData replayName, parseData

getCellValue = (name) ->
    parseFloat($("span[data-var='#{name}'] span").text())

inputCellsValues = (neigh) ->
    if neigh == "vonneumann"
        return [getCellValue(direction) for direction in ["st","n", "e", "s", "w"]]
    else if neigh == "ediemoore"
        return [getCellValue(direction) for direction in ["st","n", "ne", "e", "se", "s", "sw", "w", "nw"]]


tanh = (arg) ->
    for x,idx in arg
        arg[idx] = (Math.exp(x) - Math.exp(-x)) / (Math.exp(x) + Math.exp(-x))
    return arg

activateNetwork = (input) ->
    theta1 = root.data["layer1"]
    theta2 = root.data["layer2"]

    input.unshift(1)

    hidden_layer = tanh(numeric.dot(theta1, input))

    # get output layer
    hidden_layer.unshift(1)

    out_vector = tanh(numeric.dot(theta2, hidden_layer))

    # set new internal state of cell
    internal_state = out_vector[0]
    grayscale = 255*(internal_state+1)/2.0
    grayscale = Math.max(Math.min(Math.round(grayscale), 255), 0)
    return [internal_state, grayscale]

displayOutput = ([state,color])->
    canvas = $("#output").get(0)
    ctx = canvas.getContext("2d")

    ctx.fillStyle = "rgb(#{color},#{color},#{color})"
    ctx.fillRect(0,0,canvas.width, canvas.height)

    ctx.font = "12px courier new"
    ctx.fillStyle = "black"
    if color <= 128
        ctx.fillStyle = "white"
    text = "#{Math.round(state * 100) / 100}"
    l = text.length*12
    ctx.fillText(text,23-l/4,28)

checkInputVector = (vec) ->
    for x in vec
        return false if isNaN(x)
    return true

updateNetwork = () ->
    input = inputCellsValues(root.data["neigh"])[0]
    if !checkInputVector(input)
        return
    output = activateNetwork(input)
    displayOutput(output)

initializeInputCells = () ->
    $("#input span").each (idx, elem) ->
        name = $(elem).attr("data-var")
        new Tangle(document, {
                initialize: () ->
                    @[name] = 1
                update: () ->
                    updateNetwork()
                    color = Math.round(255*((1+@[name])/2))
                    font_color = "black"
                    if color < 128
                        font_color = "white"
                    $(elem).css({"background-color": "rgb(#{color},#{color},#{color}", "color": font_color})
        })

$(document).ready ->
    $(".ui.dimmable").dimmer({
            duration:
                show: 300
                hide: 700
        })
    $('.load.weight').bind('click', loadWeight)
    if $(".load.weight").length > 0
        $(".load.weight").first().trigger("click")
