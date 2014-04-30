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
        if name == "weights"
            console.log value
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
            """
    console.log html
    return html

displayWeightData = (weight) ->
    html = getHtml weight
    replaceHtml html

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
