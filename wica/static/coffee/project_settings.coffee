addOption = (event) ->
    section = $(event.target).attr('data-section')

    # get input tag with name of new option
    inputTag = $(event.target).siblings('input[name="optionName"]').get(0)


    # get option name
    option = $(inputTag).val()
    if option is ""
        return

    console.log "Adding option #{option} in section #{section}"

    # clear value in input tag
    $(inputTag).val("")

    opt = optionHtml(section, option)
    insertOption(section, opt)

addSection = (event) ->
    inputTag = $(event.target).siblings('input[name="sectionName"]').get(0)

    console.log inputTag
    section = $(inputTag).val()
    if section is ""
        return

    console.log "adding section #{section}"
    sct = sectionHtml(section)
    # clear input field for section
    $(inputTag).val("")
    insertSection(sct)

removeOption = (event) ->
    section = $(event.target).attr('data-section')
    option = $(event.target).attr('data-option')
    console.log "removing #{section}.#{option}"
    $(".#{section} > .#{option}").fadeOut(250, -> $(".#{section} > .#{option}").remove())

    $.ajax
        type: "DELETE"
        url: "."
        data:
            "section": "#{section}"
            "option": "#{option}"
        success: (response) -> console.log response

removeSection = (event) ->
    section = $(event.target).attr('data-section')
    console.log "removing whole section #{section}"
    $(".#{section}").fadeOut(250, ->
        $(".#{section}").next('.ui.horizontal.icon.divider').remove()
        $(".#{section}").remove()
    )
    $(".#{section}").next('.ui.horizontal.icon.divider').fadeOut(250)


    $.ajax
        type: "DELETE"
        url: "."
        data:
            "section": "#{section}"
        success: (response) -> console.log response


# function for generating option in specified section of project
# configuration
optionHtml = (section, option) ->
    """<div class="field #{option}">
    <label>#{option}</label>
    <div class="ui action input">
        <input type="text" name="#{section}.#{option}" placeholder="Enter value">
        <div class="ui removeOption tiny red button" data-option="#{option}" data-section="#{section}">
            <i class="ui minus icon"></i>
        </div>
    </div>
    </div>"""

# function for generating whole section for project configuration
sectionHtml = (section) ->
    """
    <div class="ui horizontal icon divider">
      <i class="ellipsis horizontal icon"></i>
    </div>
    <div class="#{section} section">

        <h3>#{section} <i class="ui remove removeSection icon" data-section="#{section}"></i></h3>

          <div class="ui three column grid">
            <div class="column">
              <div class="ui action input">
                <input type="text" name="optionName" placeholder="Option name">
                <div class="ui addOption button" data-section="#{section}">
                    <i class="ui plus icon"></i>
                </div>
              </div>
            </div>

          </div>"""

insertOption = (section, htmlToInsert) ->
    section = $(".#{section}")

    newOption = $(htmlToInsert)
    newOption.find(".ui.addOption.button").bind("click", addOption)
    newOption.find(".ui.removeOption.button").bind("click", removeOption)
    newOption.attr("hidden", "true")
    newOption.insertBefore(section.find(".ui.three.column.grid"))
    newOption.fadeIn()

insertSection = (htmlToInsert) ->
    lastSection = $(".section").last()

    newSection = $(htmlToInsert)

    lastSection.after(newSection)
    newSection.fadeIn()
    newSection.find(".ui.addOption.button").bind("click", addOption)
    newSection.find(".ui.removeOption.button").bind("click", removeOption)
    newSection.find(".ui.icon.removeSection").bind("click", removeSection)

$(document).ready ->
    # creates form submitters for deleting configuration and updating configuration
    new FormSubmitter(".ui.update.form", "PUT", ".", (response) -> window.location.assign response)

    # button for adding fields
    $('.addSection').bind('click', addSection)
    $('.addOption').bind('click', addOption)
    $('.removeOption').bind('click', removeOption)
    $('.removeSection').bind('click', removeSection)

