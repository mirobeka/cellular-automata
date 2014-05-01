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

        @ctx.font = "9px curier new"
        for row,ridx in neuron
            for val,cidx in row
                @ctx.fillStyle = scale(val)
                @ctx.fillRect(33*cidx,33*ridx,33,33)
                @ctx.fillStyle = "#000"
                @ctx.fillText("#{Math.round(val * 100) / 100}",33*cidx+5,33*ridx+18)

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
        console.log layer
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
        if name == "layer1" or name == "layer2"
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

            <div class="ui middle aligned two column grid">
                <div class="row">
                    <div class="column">
                        <div class="ui layer1 vertical fluid menu">
                        </div>
                    </div>
                    <div class="column">
                        <div class="ui layer2 vertical fluid menu">
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
            <canvas id="#{layer}_neuron#{idx}"></canvas>
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

    addLayer2Neuron(weight, 0)

getData = (weightName, callback) ->
    $.ajax
        type: "GET"
        url: "../weight/#{weightName}/"
        success: callback

parseData = (data) ->
    data = JSON.parse data
    displayWeightData data
    $(".ui.dimmable").dimmer("hide")

loadWeight = (event) ->
    $(".ui.dimmable").dimmer("show")
    replayName = $(@).attr("data-name")
    getData replayName, parseData

$(document).ready ->
    $(".ui.dimmable").dimmer({
            duration:
                show: 300
                hide: 700
        })
    $('.load.weight').bind('click', loadWeight)
